#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 12.11.2021
# network-probe

import time
import threading

class Sender(threading.Thread):
    '''A thread to send the ping analytics.'''

    def __init__(self, event_queue, daemon=True):

        threading.Thread.__init__(self)
        self.event_queue = event_queue


    def run(self):

        item = self.event_queue.get()
        sent = False

        while sent is False:

            # try:
            self.send(item)
            # except Error:
            #     timee.sleep(1)
            # else:
            sent = True

    def send(item):
        print(item)

