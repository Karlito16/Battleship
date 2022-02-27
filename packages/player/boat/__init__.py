#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: boat

from packages.public.constants import Constants


class Boat(object):

    def __init__(self, shape):
        """
        Constructor.
        Shape contains boat's pieces, as well as
        size and orientation (that is, direction).
        :param shape: <class Shape>
        """
        self._shape = shape
        for box in self.shape:
            box.type = Constants.BOAT_SIZES.index(self._shape.size)
            box.color = Constants.BOAT_COLORS[box.type]

    @property
    def shape(self):
        """
        Getter.
        :return: list
        """
        return self._shape.get

    def draw(self, surface):
        """
        Draws the boat.
        :param surface: <class Surface>
        :return: None
        """
        for box in self._shape.get:     # TODO: make this and other object iterable etc.
            if box.is_hit:
                box.hit(surface)
            else:
                box.fill(surface)
        return

    @staticmethod
    def reveal(surface, piece):
        """
        Reveals the boat at given piece (that is, box).
        :param surface: <class Surface>
        :param piece: <class Box>
        :return: None
        """
        piece.fill(surface=surface, color=Constants.BOAT_COLORS[Constants.BOAT_SIZES.index(piece.type)])
        return
