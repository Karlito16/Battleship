#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: raising_thread
# source from: https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread

import threading


class RaisingThread(threading.Thread):
    def run(self):
        self._exc = None
        try:
            super().run()
        except Exception as e:
            self._exc = e

    def join(self):
        super().join()
        if self._exc:
            raise self._exc
