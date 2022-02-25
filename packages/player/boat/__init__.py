#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: boat

from packages.player.window import Window


class Boat(object):
    NAMES = ["Aircraft Carrier", "Battleship", "Cruiser", "Destroyer", "Submarine"]
    # QUANTITY = [1, 1, 1, 2, 2]
    QUANTITY = [1, 1, 1, 2, 2]  # temp, for testing
    SIZES = [5, 4, 3, 2, 1]
    BOAT_COLORS = [Window.RED, Window.BLUE, Window.GREEN, Window.YELLOW, Window.ORANGE]
    assert len(NAMES) == len(QUANTITY) == len(SIZES), \
        "Invalid data for boat names, their quantity, size and color values!"

    def __init__(self, shape):
        """
        Constructor.
        Shape contains boat's pieces, as well as
        size and orientation (that is, direction).
        :param shape: <class Shape>
        """
        self._shape = shape
        for box in self.shape:
            box.type = Boat.SIZES.index(self._shape.size)
            box.color = Boat.BOAT_COLORS[box.type]

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
        piece.fill(surface=surface, color=Boat.BOAT_COLORS[Boat.SIZES.index(piece.type)])
        return
