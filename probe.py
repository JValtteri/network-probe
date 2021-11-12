#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 12.11.2021
# network-probe

import os
import time
from queue import Queue, Empty
import sender


class Probe():

    def __init__(self):

        self.id = 0
        self.name = "probe"
        self.ip_list = ['1.1.1.1', '1.0.0.1']
        self.count = 1
        self.time_interval = 2
        self.detection_debth = 3
        self.event_queue = Queue(4000)

    def run_probes(self):
        for ip in self.ip_list:
            result = self.ping(ip)
            # print(result)

        time.sleep(self.time_interval)

    def ping(self, ip):
        """
        returns:
        {"target": IP, "up": 1 or 0, "timestamp": POSIX(ms)}
        """

        posix = time.time() * 1000
        response = os.popen(f"ping -n {self.count} {ip}").read()
        if (f"Received = {self.count}") in response:
            up = 1
        else:
            up = 0

        result = {
            "target": ip,
            "up": up,
            "timestamp": posix
        }
        return result

    def detect_network(self):
        "Trace the first nodes of the network"
        trace_ips = []
        str_range = self.str_range( range( 1, self.detection_debth + 1 ) )
        response = os.popen(f"pathping -q 1 -h {self.detection_debth} 1.1.1.1").readlines()
        for line in response:
            # Get the first X IPs on the trace and put them in a LIST: trace_ips
            if len(line) > 3 and line[2] in str_range:
                trace_ip = line.rsplit("[")[1][0:-3]
                trace_ips.append(trace_ip)
                # print(trace_ip)
                if line[2] == str(self.detection_debth):
                    return trace_ips

    def add_ips(self, ip_list):
        'add an IP LIST to the probe ip list'
        for ip in ip_list:
            self.ip_list.append(ip)

    @staticmethod
    def str_range(the_range):
        'conver range() to STR'
        str_list = []
        for i in the_range:
            str_list.append( str(i) )
        return str_list



def test():
    probe = Probe()

    # Creates the sender thread and gices it access to the event queue
    sende_thread = sender.Sender(probe.event_queue)
    sende_thread.daemon=True

    # Runs a network discovery
    ips = probe.detect_network()

    # Adds discovered nodes to IP list to be pinged
    print("Probe will ping the selected IPs")
    probe.add_ips(ips)
    for ip in ips:
        print(ip)
    print("\n")

    # Starts pinging target IPs
    for i in range(3):
        probe.run_probes()

if __name__ == "__main__":
    test()
