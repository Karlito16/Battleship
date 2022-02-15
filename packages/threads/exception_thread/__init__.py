#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: exception_thread
# source from: https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread

import threading
import traceback
import logging


class ExceptionThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except Exception:
            logging.error(traceback.format_exc())
