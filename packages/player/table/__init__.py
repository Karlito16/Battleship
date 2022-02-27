#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: table

import pygame
from packages.public.constants import Constants
from packages.player.area import Area
from packages.player.window import Window


class Table(Area):

    def __init__(self, rect, margin, row_margin):
        """
        Constructor.
        Creates the table.
        Position is given with Rect object.
        :param rect: <class Rect>
        :param margin: int
        """
        super().__init__(area=rect)
        self._margin = margin
        self._row_margin = row_margin
        self._rows = 0
        self._cols = 0
        self._table = list(list())  # matrix
        self._col_widest = list()   # remembers the widest string length that is stored in each column
        self._cols_left_coord = list()  # used for drawing the table

    def __str__(self):
        """
        To string method.
        """
        output = ""
        i, j = 0, 0
        while i < self._rows:
            while j < self._cols:
                data = self._table[i][j]
                if data is not None:
                    if j == 0:
                        output += data + ' '
                    else:
                        offset = self._col_widest[j - 1] - len(self._table[i][j - 1])
                        output += ' ' * offset + data + ' '
                j += 1
            i += 1
            j = 0
            output += '\n'
        return output

    @property
    def margin(self):
        """
        Getter.
        :return: int
        """
        return self._margin

    @property
    def row_margin(self):
        """
        Getter.
        :return: int
        """
        return self._row_margin

    @property
    def rows(self):
        """
        Getter.
        :return: int
        """
        return self._rows

    @property
    def cols(self):
        """
        Getter.
        :return: int
        """
        return self._cols

    @property
    def get(self):
        """
        Returns the table.
        :return: list(list)
        """
        return self._table

    def get_row(self, index):
        """
        Returns the row with given index.
        :param index: int
        :return: list
        """
        if index < 0 or index > self._rows:
            return []
        return self._table[index]

    def get_column(self, index):
        """
        Returns the column with given index.
        :param index: int
        :return: list
        """
        if index < 0 or index > self._cols:
            return []
        col = []
        for row in self._table:
            col.append(row[index])
        return col

    def add_row(self, *args):
        """
        Adds the row to the table.
        Parameter args contains data that
        needs to be stored in the table.
        Method returns True if data is
        transfered into a table, False
        otherwise.
        :param args: tuple
        :return: bool
        """
        row = list()
        for i in range(len(args)):
            data = str(args[i])
            try:
                if self._col_widest[i] < len(data):
                    self._col_widest[i] = len(data)
            except IndexError:
                # new row has additional columns
                self._col_widest.append(len(data))
                self._cols += 1
            row.append(data)
        self._table.append(row)
        self._rows += 1
        # check previous and new rows and their number of columns
        for row in self._table[:self._rows]:
            while len(row) < self._cols:
                row.append(None)
        return True

    def draw(self, surface):
        """
        Method draws the table.
        Calculates it's own font sizes to fill the given space on screen.
        :param surface: <class Surface>
        :return: None
        """
        row_height = self.height // self._rows
        col_widths = list(map(lambda w: w / sum(self._col_widest) * self.width, self._col_widest))
        font_size = row_height - 2 * self._row_margin  # TODO: this 20 replace with some formula!
        x = self.x + self.margin
        y = self.y + self.margin
        for row in range(self._rows):
            for col in range(self._cols):
                text = self._table[row][col]
                if text is not None:
                    tmp_font_size = font_size
                    while True:
                        surf, rect = Window.create_text(font_name=Constants.FONT_NAME_1, font_size=tmp_font_size,
                                                        text=text, fg=Constants.BLACK, bg=Constants.BGCOLOR)
                        if rect.width <= col_widths[col]:
                            break
                        tmp_font_size -= 2 * self._row_margin
                    rect.topleft = (x, y)
                    surface.blit(surf, rect)
                x += col_widths[col]
            x = self.x + self._margin
            y += row_height + self._row_margin
        return

    def highlight_row(self, surface, index, color):
        """
        Method highlights the row with given index.
        Returns True if highlighted.
        :param surface: <class surface>
        :param index: int
        :param color: str
        :return: bool
        """
        if index < 0 or index > self._rows:
            return False

        highlight_width = int(self._row_margin * 0.5)
        row_height = self.height // self._rows
        x = self.x + self.margin - self._row_margin
        y = self.y + self.margin - self._row_margin // 2 + (row_height + self._row_margin) * index
        pygame.draw.rect(surface, color, pygame.Rect(x, y, self.width, row_height), highlight_width)
        return True
