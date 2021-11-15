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
        message[0]["fields"]["value"] = item["value"]
        message[0]["time"] = round(item["time"])

        return message


    def send(self, message):
        message = json.dump(message) #, indent=4, sort_keys=True)
        f=open("out.txt",'w')
        f.write(json.dumps(json.loads(message), indent=4, sort_keys=True))
        f.close()
        logger.debug(message)

        # message = [
        #     {
        #         "fields": {
        #             "value": 0
        #         },
        #         "measurement": "ping",
        #         "tags": {
        #             "id": "0",
        #             "name": "Test",
        #             "target": "62.78.117.7"
        #         },
        #         "time": 1636991937272528
        #     }
        # ]

        # message2 = [
        #     {
        #         "measurement": "cpu_load_short",
        #         "tags": {
        #             "host": "server01",
        #             "region": "us-west"
        #         },
        #         "time": "2009-11-10T23:00:00Z",
        #         "fields": {
        #             "value": 0.64
        #         }
        #     }
        # ]

        logger.debug(f"Message: {message}")
        client = InfluxDBClient(self.host, self.port, self.db_user, self.db_password, database=self.db_name, ssl=True)
        client.write_points(message)
        client.close()
