#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: area


class Area(object):

    def __init__(self, area):
        """
        Construcotr.
        This class defines any on screen object, which
        has its own area on the screen.
        That area is defined with parameter area,
        object from class pygame.Rect.
        :param area: <class Rect>
        """
        self._area = area

    @property
    def area(self):
        """
        Getter.
        :return: <class Rect>
        """
        return self._area

    @property
    def x(self):
        """
        Getter.
        :return: int
        """
        return self._area[0]

    @property
    def y(self):
        """
        Getter.
        :return: int
        """
        return self._area[1]

    @property
    def width(self):
        """
        Getter.
        :return: int
        """
        return self._area[2]

    @property
    def height(self):
        """
        Getter.
        :return: int
        """
        return self._area[3]
