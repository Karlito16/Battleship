#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: grid
import pygame

from packages.player.box import Box


class Grid(object):
    MAIN_BORDER_WIDTH = 4   # px
    HIGHLIGHT_BORDER_WIDTH = 1  # px
    SEPARATOR_WIDTH = 2     # px

    def __init__(self, rectangle, size):
        """
        Constructor.
        Rectangle represents area where the grid should be on the screen.
        :param rectangle: <class Rect>
        :param size: int
        """
        self._rectangle = rectangle
        self._size = size   # number of boxes in one row, and number of rows, so there will be n * n boxes in the grid
        self._grid = []   # matrix

        self._x, self._y, self._width, _ = self._rectangle   # self._width == self._height
        width = self._width - 2 * (Grid.MAIN_BORDER_WIDTH + Grid.HIGHLIGHT_BORDER_WIDTH)    # width without border margins
        self._box_total_size = width // self._size   # size with box margins
        # this is margin between borders and first row/column of the grid
        # this can either be 0 if width mod self._size is equal to zero (that is, there is no remainder)
        self._inside_grid_margin = (width % self._size) // 2
        self._create()  # creates the grid (NO GUI, only data structure)

    def _create(self):
        """
        Creates the grid.
        This method only fills the grid data structure.
        No GUI has been created or updated here.
        :return: None
        """
        # calculate the offset, starting point for our boxes to fill up, ignoring the grid borders and margins
        offset = self._x + Grid.MAIN_BORDER_WIDTH + Grid.HIGHLIGHT_BORDER_WIDTH + self._inside_grid_margin
        for i in range(self._size):
            row = []
            for j in range(self._size):
                rect = pygame.Rect(offset + i * self._box_total_size,
                                   offset + j * self._box_total_size,
                                   self._box_total_size,
                                   self._box_total_size)
                row.append(Box(rect))
            self._grid.append(row)
