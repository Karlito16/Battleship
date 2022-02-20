#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: point


class Point(object):

    def __init__(self, x, y):
        """
        Constructor. Creates a point with x and y coordinates.
        :param x: int
        :param y: int
        """
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        Getter for attribute x.
        :return: int
        """
        return self._x

    @property
    def y(self):
        """
        Getter for attribute y.
        :return: int
        """
        return self._y
