#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: table


class Table(object):

    def __init__(self, rect):
        """
        Constructor.
        Creates the table.
        Position is given with Rect object.
        :param rect: <class Rect>
        """
        self._rect = rect
        self._rows = 0
        self._cols = 0
        self._table = list(list())  # matrix

    def __str__(self):
        """
        To string method.
        """
        output = ""
        for row in self._table:
            output += row.__str__() + "\n"
        return output.strip()

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
        for data in args:
            row.append(data)
        self._table.append(row)
        self._rows += 1
        if self._cols < len(args):
            self._cols = len(args)
        return True

    def fill(self):
        """
        Fills the rows of the table with None type
        if some of them have less columns than the
        max number of columns.
        :return: None
        """
        for row in self._table:
            cols = len(row)
            while cols < self._cols:
                row.append(None)
                cols += 1
        return None
