#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 10.01.2021
# network-probe

import threading
import time
import os
from logger import Logger
logger = Logger(__name__)


class Ping(threading.Thread):
    '''A thread to send the ping analytics.'''

    def __init__(self, ip, interval, out_queue, daemon=True):

        threading.Thread.__init__(self)
        self.ip = ip
        self.interval = interval
        self.out_queue = out_queue

    def run(self):
        '''Thread main function'''
        logger.debug("Ping thread STARTED")
        while True:
            result = self.ping()
            # PUT RESULT TO QUEUE

            #####################
            time.sleep(self.interval)
        logger.debug("Ping thread CLOSED")


    def ping(self):
        """
        Pings the IP, returns:
        {"target": IP, "up": 1 or 0, "time": POSIX(µs)}
        """

        posix = round( time.time() * 1000 )
        response = os.popen("ping -n {} {}".format(self.ping_count, self.ip)).read()
        if ("Received = {}".format(self.ping_count)) in response:
            up = 1
        else:
            up = 0

        result = {
            "target": self.ip,
            "value": up,
            "time": posix
        }

        return result

