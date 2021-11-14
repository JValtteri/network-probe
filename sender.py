#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 12.11.2021
# network-probe

import time
import json
import threading
from influxdb import InfluxDBClient
from logger import Logger
logger = Logger(__name__)


class Sender(threading.Thread):
    '''A thread to send the ping analytics.'''

    def __init__(self, event_queue, body, db_name, db_user, db_password, db_host, db_port, daemon=True):

        threading.Thread.__init__(self)
        self.event_queue = event_queue
        self.body = body

        self.host = db_host
        self.port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password


    def run(self):
        logger.debug("Sender thread STARTED")
        size = self.event_queue.qsize()
        logger.debug(f"Queue size: {size}")
        item = self.event_queue.get()

        sent = False
        while sent is False:
            # try:
            message = self.message_map(item)
            self.send( json.dumps(message) )
            logger.info(f"Sent: {item}")
            # except Error:
            #     timee.sleep(1)
            # else:
            sent = True

        logger.debug("Sentder thread CLOSED")


    def message_map(self, item):
        message = self.body
        message[0]["tags"]["target"] = item["target"]
        message[0]["fields"]["up"] = item["up"]
        message[0]["time"] = round(item["time"])

        return message


    def send(self, message):
        logger.debug(f"Message: {message}")
        # client = InfluxDBClient(self.host, self.port, self.db_user, self.db_password, database=self.db_name, ssl=True)
        # client.write_points(message)
        # client.close()
