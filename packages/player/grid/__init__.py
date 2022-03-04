#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: grid

import pygame
from packages.player.box import Box
from packages.player.area import Area
from packages.public.constants import Constants


class Grid(Area):

    def __init__(self, rect, size, border_width, highlight_border_width):
        """
        Constructor.
        Rect (that is, rectangle) represents area
        where the grid should be on the screen.
        :param rect: <class Rect>
        :param size: int
        :param border_width: int
        :param highlight_border_width: int
        """
        # reshaping, because we want all boxes to have a int value for size, not float
        while (rect[2] - 2 * border_width - Constants.SEPARATOR_WIDTH * (size - 1)) % size != 0:
            rect = pygame.Rect(rect[0], rect[1], rect[2] - 1, rect[3] - 1)

        super().__init__(area=rect)
        self._size = size   # number of boxes in one row, and number of rows, so there will be n * n boxes in the grid
        self._border_width = border_width
        self._highlight_border_width = highlight_border_width

        self._grid = []   # matrix

        width = self.width - 2 * self._border_width    # width without border margins
        width -= Constants.SEPARATOR_WIDTH * (self._size - 1)   # width without separators (that is, grid lines)
        self._box_total_size = width / self._size   # size with box margins

        self._create()  # creates the grid (NO GUI, only data structure)

    def __getitem__(self, item):
        """
        get item special method
        :param item: any
        :return: any
        """
        return self._grid[item]

    @property
    def total_box_size(self):
        """
        Getter. This size includes boxes' both left and right margins.
        :return: int
        """
        return self._box_total_size

    @property
    def size(self):
        """
        Getter.
        :return: int
        """
        return self._size

    @property
    def get(self):
        """
        Getter.
        :return: list
        """
        return self._grid

    def row(self, index):
        """
        Returns the row with given index.
        Index must be grater than 0 and less than grid width.
        :param index: int
        :return: list
        """
        if index < 0 or index > self.width:
            return []
        return self._grid[index]

    def column(self, index):
        """
        Returns the column with given index.
        Index must be grater than 0 and less than grid width.
        :param index: int
        :return: list
        """
        if index < 0 or index >= self.width:
            return []
        col = []
        for row in self._grid:
            col.append(row[index])
        return col

    def _create(self):
        """
        Creates the grid.
        This method only fills the grid data structure.
        No GUI has been created or updated here.
        :return: None
        """
        # calculate the offset, starting point for our boxes to fill up, ignoring the grid borders and margins
        offset_x = self.x + self._border_width
        offset_y = self.y + self._border_width
        for i in range(self._size):
            row = []
            for j in range(self._size):
                rect = pygame.Rect(offset_x + j * (self._box_total_size + Constants.SEPARATOR_WIDTH),
                                   offset_y + i * (self._box_total_size + Constants.SEPARATOR_WIDTH),
                                   self._box_total_size,
                                   self._box_total_size)
                row.append(Box(rect))
            self._grid.append(row)

    def get_box_at_pixel(self, x, y):
        """
        Returns the box that contains (x, y) pixel.
        If none of them contains, returns None
        :param x: int
        :param y: int
        :return: <class Box> or None
        """
        for row in self._grid:
            for box in row:
                if box.area.collidepoint(x, y):
                    return box
        return None

    def draw(self, surface, color1, color2, color3):
        """
        Method draws the grid.
        Color1 is the main border color.
        Parameter color2 is color of the inside border
        (that is, either players' or opponents' color).
        Color3 is the separator color.
        :param surface: <class Surface>
        :param color1: str
        :param color2: str
        :param color3: str
        :return: None
        """
        # draw lines
        line_lenght = self.width - 2 * self._border_width
        line_width = Constants.SEPARATOR_WIDTH
        for box in self.row(0)[1:]:     # vertical
            pygame.draw.line(surface, color3, (box.x - line_width, box.y), (box.x - line_width, box.y + line_lenght), line_width)
        for box in self.column(0)[1:]:  # parallel
            pygame.draw.line(surface, color3, (box.x, box.y - line_width), (box.x + line_lenght, box.y - line_width), line_width)

        # draw borders
        pygame.draw.rect(surface, color1, self.area, self._border_width)
        pygame.draw.rect(surface, color2, self.area, self._highlight_border_width)
        return

    def get_index_of(self, box):
        """
        Returns i and j values (that is, row and column for given box).
        If not found, return (None, None)

        :param box: <class Box>
        :return: tuple :: (int, int)
        """
        for i in range(self._size):
            for j in range(self._size):
                box_ = self._grid[i][j]
                if box_ == box:
                    return i, j
        return None, None