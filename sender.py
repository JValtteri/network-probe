#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 12.11.2021
# network-probe

import time
import json
import threading
# from influxdb import InfluxDBClient
from logger import Logger
logger = Logger(__name__)


class Sender(threading.Thread):
    '''A thread to send the ping analytics.'''

    def __init__(self, event_queue, daemon=True):

        threading.Thread.__init__(self)
        self.event_queue = event_queue


    def run(self):
        logger.debug("Sender thread STARTED")
        size = self.event_queue.qsize()
        logger.debug(f"Queue size: {size}")
        item = self.event_queue.get()

        sent = False
        while sent is False:
            # try:
            self.send( json.dumps(item) )
            # except Error:
            #     timee.sleep(1)
            # else:
            sent = True

        logger.debug("Sentder thread CLOSED")

    @staticmethod
    def send(item):
        logger.info(f"Sent: {item}")
