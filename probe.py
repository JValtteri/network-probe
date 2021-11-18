#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 12.11.2021
# network-probe

import json
from logging import log
import os
import queue
import time
from queue import Queue, Empty
from sender import Sender
import platform


# LOGGING
filename = 'probe.log'
open(filename, 'a').close()     # Create/Open log file in 'append' mode
from logger import Logger
logger = Logger(__name__)

class Probe():

    def __init__(self):

        # Loads the config
        self.settings = self.load_config(0)
        self.body = [self.load_config(1)]

        # Stores the values in the object
        self.id = self.settings["id"]
        self.name = self.settings["name"]
        self.ip_list = self.settings["targets"]
        self.ping_count = self.settings["ping_count"]
        self.time_interval = self.settings["time_interval"]
        self.detection_depth = self.settings["detection_depth"]
        self.queue_depth = self.settings["event_queue"]
        self.event_queue = Queue(self.queue_depth)

        # DB configuration
        self.db_name = self.settings["db_name"]
        self.db_user = self.settings["db_user"]
        self.db_password = self.settings["db_password"]
        self.host = self.settings["db_host"]
        self.port = self.settings["db_port"]

        # Updates the body static values
        self.body[0]["tags"]["name"] = self.name
        self.body[0]["tags"]["id"] = self.id

        # Creates the sender_thread
        self.sender_thread = Sender(self.event_queue, self.body, self.db_name, self.db_user, self.db_password, self.host, self.port)
        self.sender_thread.daemon=True

        # LOG THE CONFIGURATION
        logger.info("Loaded configuration")
        logger.info("ID: {}".format(self.id))
        logger.info("Name: {}".format(self.name))
        logger.info("IP list: {}".format(self.ip_list))
        logger.info("Ping count: {}".format(self.ping_count))
        logger.info("Time interval {} s".format(self.time_interval))
        logger.info("Detection depth: {}".format(self.detection_depth))
        logger.info("Queue depth: {}".format(self.queue_depth))
        logger.info("DB Host: {}".format(self.host))
        logger.info("DB port: {}".format(self.port))

        if platform.system() == 'Linux':
            self.ping = self.linux_ping
            self.detect_network = self.linux_detect_network


    def load_config(self, index=0):
        """
        Reads the config file and returns the dict of
        all settings.
        """

        filename = "config.json"

        try:
            configfile = open(filename, 'r')
            config = configfile.read()
            configfile.close()

        except FileNotFoundError:
            self.logger.critical("Error: Could not find %s" % filename)
            exit()

        # Loads the config.json
        json_file = json.loads(config)
        # Returns the part that is selected
        # 0: User config
        # 1: Message body template
        settings = json_file[index]

        return settings

    def run_probes(self):
        """Run ping for each adress in ip_list"""
        for ip in self.ip_list:
            result = self.ping(ip)

            # Put result to queue
            try:
                self.event_queue.put(result)
            except queue.Full:
                logger.error("queue.FULL")

            # If no thread is actibe, restart the thread
            if not self.sender_thread.is_alive():
                self.sender_thread = Sender(self.event_queue, self.body, self.db_name, self.db_user, self.db_password, self.host, self.port)
                self.sender_thread.daemon=True
                self.sender_thread.start()

        time.sleep(self.time_interval)


    def ping(self, ip):
        """
        Pings the IP, returns:
        {"target": IP, "up": 1 or 0, "time": POSIX(µs)}
        """

        posix = round( time.time() * 1000 )
        response = os.popen("ping -n {} {}".format(self.ping_count, ip)).read()
        if ("Received = {}".format(self.ping_count)) in response:
            up = 1
        else:
            up = 0

        result = {
            "target": ip,
            "value": up,
            "time": posix
        }
        return result


    def linux_ping(self, ip):
        """
        returns:
        {"target": IP, "up": 1 or 0, "time": POSIX(µs)}
        """

        posix = round( time.time() * 1000 )  # ms
        response = os.popen("ping -c {} {}".format(self.ping_count, ip)).read()
        if ("{} received".format(self.ping_count)) in response:
            up = 1
        else:
            up = 0

        result = {
            "target": ip,
            "value": up,
            "time": posix
        }
        return result


    def detect_network(self):
        "Trace the first nodes of the network"
        trace_ips = []
        str_range = self.str_range( range( 1, self.detection_depth + 1 ) )
        response = os.popen("pathping -q 1 -h {} 1.1.1.1".format(self.detection_depth)).readlines()
        for line in response:

            # Get the first X IPs on the trace and put them in a LIST: trace_ips
            if len(line) > 3 and line[2] in str_range:
                try:
                    trace_ip = line.rsplit("[")[1][0:-3]
                    trace_ips.append(trace_ip)

                    if line[2] == str(self.detection_depth):
                        break
                except IndexError:
                    return trace_ips
        return trace_ips


    def linux_detect_network(self):
        "Trace the first nodes of the network"
        trace_ips = []
        str_range = self.str_range( range( 1, self.detection_depth + 1 ) )
        response = os.popen("traceroute -q 1 1.1.1.1").readlines()
        for line in response:

            # Get the first X IPs on the trace and put them in a LIST: trace_ips
            if len(line) > 3 and line[1] in str_range:
                try:
                    trace_ip = line.rsplit("(")[1].rsplit(")")[0]
                    trace_ips.append(trace_ip)

                    if line[1] == str(self.detection_depth):
                        break
                except IndexError:
                    return trace_ips
        return trace_ips


    def add_ips(self, ip_list):
        'add an IP LIST to the probe ip list'
        for ip in ip_list:
            self.ip_list.append(ip)
        # Remove duplicaes
        self.ip_list = set(self.ip_list)


    @staticmethod
    def str_range(the_range):
        'conver range() to STR'
        str_list = []

        for i in the_range:
            str_list.append( str(i) )

        return str_list


def test():
    probe = Probe()

    # Runs a network discovery
    ips = probe.detect_network()

    # Adds discovered nodes to IP list to be pinged
    logger.info("Probe will ping the selected IPs")
    probe.add_ips(ips)

    for ip in probe.ip_list:
        logger.info(ip)
    print("\n")

    # Starts pinging target IPs
    for i in range(1):
        probe.run_probes()
    probe.sender_thread.join()


def run():
    probe = Probe()

    # Runs a network discovery
    ips = probe.detect_network()

    # Adds discovered nodes to IP list to be pinged
    logger.info("Probe will ping the selected IPs")
    probe.add_ips(ips)

    # Logs the IPs
    for ip in probe.ip_list:
        logger.info(ip)
    print("\n")

    # Starts pinging target IPs
    try:
        while True:
            probe.run_probes()
    except KeyboardInterrupt:
        timeout = 15 # seconds
        logger.info("Keyboard interrupt detected, waiting for threads ({} s).".format(timeout))
        probe.sender_thread.join(timeout)
        logger.info("Threads closed, terminating.")


if __name__ == "__main__":
    # test()
    run()
