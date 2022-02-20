#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: box


class Box(object):
    BOX_MARGIN = 2  # px

    def __init__(self, rectangle):
        """
        Constructor.
        Rectangle is object that defines space (position)
        on screen for our box.
        Difference between total size and size is that total size
        includes both left and right box margins.
        :param rectangle: <class Rect>
        """
        self._rect = rectangle
        # self._x, self._y, self._total_size, _ = self._rect    # unnecesarry memory usage
        self._size = self.total_size - 2 * Box.BOX_MARGIN

        self._hit = False   # True if boat has been hit on that place
        self._type = -1     # boat type, -1 for empty box ("sea")

    @property
    def rect(self):
        """
        Getter for attribute rect.
        :return: <class Rect>
        """
        return self._rect

    @property
    def x(self):
        """
        Getter for attribute x.
        :return: int
        """
        return self._rect[0]

    @property
    def y(self):
        """
        Getter for attribute y.
        :return: int
        """
        return self._rect[1]

    @property
    def total_size(self):
        """
        Getter for attribute total size.
        :return: int
        """
        return self._rect[2]

    @property
    def size(self):
        """
        Getter for attribute size.
        :return: int
        """
        return self._size
