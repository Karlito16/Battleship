#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: queue

from packages.structures.iterable import Iterable


class Queue(list):

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()

    def enqueue(self, value):
        """
        Adds new element in queue.
        :param value: <class object>
        :return: bool
        """
        self.append(value)

    def dequeue(self):
        """
        Removes the first of remaining elements
        that has been added in the queue.
        :return: <class object>
        """
        if len(self) > 0:
            return self.pop(0)
        return None

    def peek(self, n=1):
        """
        Returns the first n elements of the queue.
        If n > size, returns emptly list.
        :param n: int
        :return: list
        """
        if n > len(self):
            return []
        return self[0], self[1]


class QueueC(Iterable):

    class QueueElement(object):
        """
        Class for each queue element.
        """

        def __init__(self, value):
            """
            Constructor. Gets the object value which will be element.
            :param value: <class object>
            """
            self._value = value
            self._next = None

        def get_value(self):
            """
            Getter. Returns the element value.
            :return: <class object>
            """
            return self._value

        @property
        def next(self):
            """
            Property. Returns the next element in queue.
            :return: <class object>
            """
            return self._next

        @next.setter
        def next(self, value):
            """
            Setter.
            :param value: <class object>
            :return: None
            """
            self._next = value
            return

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self._read = None
        self._write = None
        self._iterator = Iterable()
        self._size = 0

    def __str__(self):
        """
        To string method.
        :return: str
        """
        head = self._iterator.begin()
        output = "["
        while not self._iterator.end():
            output += head.get_value().__str__() + ", "
            head = self._iterator.next()
        output = output.strip(",") + "]"
        return output

    def begin(self):
        """
        Begins the iterator.
        :return: None
        """
        self._head = self._read
        return self._head

    @property
    def iterator(self):
        """
        Property. Returns the iterator.
        :return: <class Iterable>
        """
        return self._iterator

    def enqueue(self, value):
        """
        Adds new element in queue.
        :param value: <class object>
        :return: bool
        """
        element = Queue.QueueElement(value=value)
        # if we have queue that is empty
        if self._read is None and self._write is None:
            self._read = self._write = element
        # not empty queue
        else:
            prev_element = self._write
            self._write = element
            # element.next = self._write
            prev_element.next = element
        self._size += 1
        return True

    def dequeue(self):
        """
        Removes the first of remaining elements
        that has been added in the queue.
        :return: <class object>
        """
        # queue is empty, nothing to remove
        if self._read == self._write is None:
            return None
        element = self._read
        # if queue contains only 1 element, which will now be removed
        if self._read == self._write:
            self._read = self._write = None
        else:
            self._read = element.next
            # if self._read is None:
            #     self._write = None
        self._size -= 1
        return element.get_value()

    def peek(self, n=1):
        """
        Returns the first n elements of the queue.
        If n > size, returns emptly list.
        :param n: int
        :return: list
        """
        if n > self._size:
            return []
        element = self._read
        ret = []
        while n > 0:
            ret.append(element.get_value())
            element = element.next
            n -= 1
        return ret

    @property
    def size(self):
        """
        Property. Returns the size of queue.
        :return: int
        """
        return self._size
