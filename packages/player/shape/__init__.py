#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: shape

from packages.player.box import Box
# from packages.public.logger import Logger


class Shape(object):
    # directions
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

    def __init__(self, grid, head, size, direction):
        """
        Constructor.
        Creates shape within given grid.
        Box represends the head of the shape.
        Lenght is given with parameter size.
        Direction is defined with parameter direction.
        :param grid: <class Grid>
        :param head: <class Box>
        :param size: int
        :param direction: str
        """
        self._grid = grid
        self._head = head     # we can assume that this box is not selected (that is, empty)
        self._size = size
        self._direction = direction
        # assert self._direction in [Shape.LEFT, Shape.RIGHT, Shape.UP, Shape.DOWN], "Invalid direction!"
        self._shape = list()

        # creates the shape
        self._valid = self._create()

    @property
    def head(self):
        """
        Returns the first box that has been added in shape list.
        :return: <class Box>
        """
        return self._head

    @property
    def size(self):
        """
        Getter.
        :return: int
        """
        return self._size

    @property
    def is_valid(self):
        """
        Getter.
        :return: bool
        """
        return self._valid

    @property
    def get(self):
        """
        Returns the shape list.
        :return: list
        """
        return self._shape

    def _create(self):
        """
        Creates the shape, if possible of course.
        Returns True if shape can be created, False otherwise.
        :return: bool
        """
        valid = True
        self._shape.append(self._head)
        # Shorter temp variable names
        x = self._head.x
        y = self._head.y
        width = self._head.width
        while len(self._shape) < self._size:
            try:
                if self._direction == Shape.LEFT:
                    box = self._grid.get_box_at_pixel(x=x - width * len(self._shape), y=y)
                elif self._direction == Shape.RIGHT:
                    box = self._grid.get_box_at_pixel(x=x + width * len(self._shape), y=y)
                elif self._direction == Shape.UP:
                    box = self._grid.get_box_at_pixel(x=x, y=y - width * len(self._shape))
                else:
                    box = self._grid.get_box_at_pixel(x=x, y=y + width * len(self._shape))
            except IndexError:  # too close to the grid border
                valid = False
                return valid
            else:
                if box is None:     # box will be None if it is out of the grid sizes
                    valid = False
                    return valid
                elif box.type != Box.EMPTY:
                    valid = False
                self._shape.append(box)
        return valid

    def change_orientation(self, direction):
        """
        Changes the orientation of the shape.
        :param direction: str
        :return: None
        """
        self._shape = []
        self._direction = direction
        self._valid = self._create()
        return

    def highlight(self, surface, color):
        """
        Highlights the shape with given color.
        :param surface: <class Surface>
        :param color: str
        :return: None
        """
        for box in self._shape:
            box.highlight(surface, color)
        return
