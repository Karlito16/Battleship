#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: iterable


class Iterable(object):

    def __init__(self):
        """
        Constructor.
        """
        self._head = None

    def begin(self):
        """
        Begins the iterator. Virtual method. Must be overrided.
        :return: None
        """
        pass

    def next(self):
        """
        Returns the next iteration.
        :return: <class Queue.QueueElement>
        """
        if self._head:
            self._head = self._head.next()
            return self._head
        return None

    def end(self):
        """
        Returns if iteration is finished.
        :return: bool
        """
        return self._head is None
