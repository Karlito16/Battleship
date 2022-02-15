#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: timer

import time
from packages.threads.raising_thread import RaisingThread


class Timer(RaisingThread):
    _second = 1
    _stop_time = 1e-3

    def __init__(self, t=None):
        """
        Constructor. Parameter t is time which will be counted down.
        :param t: int
        """
        if t is None:
            super().__init__(target=self.stopwatch)
        elif t > 0:
            super().__init__(target=self.countdown)
            self._t = t
        else:
            raise AttributeError("Parameter t must be greather than zero!")
        self._pause = False
        self._end = False

    def countdown(self):
        """
        Counts down the given time (in seconds).
        Raises RuntimeError when finished with counting.
        :return: None
        """
        if self._end:
            return
        if self._pause:
            time.sleep(Timer._stop_time)
            self.countdown()
        if self._t == 0:
            raise RuntimeError("Time Is Up!")
        time.sleep(Timer._second)
        self._t -= Timer._second
        self.countdown()

    def end(self):
        """
        Ends the countdown.
        :return: None
        """
        self._end = True

    def pause(self):
        """
        Stops the countdown.
        :return: None
        """
        self._pause = True

    def resume(self):
        """
        Resumes the countdown.
        :return: None
        """
        self._pause = False

    def stopwatch(self):
        """
        Measure the time until parameter end is set to True.
        :return: None
        """
        if self._end:
            raise RuntimeError("Stopwatch ends.")
        time.sleep(Timer._second)
        self.stopwatch()

    @staticmethod
    def wait(t):
        """
        Sleeps for given time t (in seconds).
        Same effect as countdown, but this method does not use
        new thread, as it should be used for short amount of time
        (t shoud be < 1e-3, 1 milisecond).
        :param t: float
        :return: None
        """
        time.sleep(t)
        return
