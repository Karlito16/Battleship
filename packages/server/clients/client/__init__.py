#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: client

from packages.public.logger import Logger


class Client(object):

    def __init__(self, connection, username):
        """
        Constructor.
        :param username: str
        :param connection: <class socket>
        """
        self._connection = connection
        self._username = username
        self._connected = False
        self._in_game = False
        self._in_lobby = True
        self._game = None
        self._ready = False

    def __str__(self):
        """
        To string method.
        :return: str
        """
        return f"Client({self._username}, {self._connection})"

    @property
    def connected(self):
        """
        Property. Returns if client is connected.
        :return: bool
        """
        return self._connected

    @connected.setter
    def connected(self, value):
        """
        Setter.
        :param value: bool
        :return: None
        """
        self._connected = value
        return

    @property
    def game(self):
        """
        Property. Returns game in which the client is.
        :return: <class Game>
        """
        return self._game

    @game.setter
    def game(self, value):
        """
        Setter. Sets the game.
        :return: None
        """
        self._game = value

    @property
    def connection(self):
        """
        Getter. Returns the connection.
        :return: <class socket>
        """
        return self._connection

    @property
    def username(self):
        """
        Getter. Returns the username.
        :return: str
        """
        return self._username

    @property
    def in_game(self):
        """
        Property. Returns if client is in the game.
        :return: bool
        """
        return self._in_game

    @in_game.setter
    def in_game(self, value):
        """
        Setter.
        :return: None
        """
        if isinstance(value, bool):
            self._in_game = value
            self._in_lobby = not value
        return

    @property
    def in_lobby(self):
        """
        Getter.
        :return: bool
        """
        return self._in_lobby

    @property
    def ready(self):
        """
        Getter. Returns if client is ready for game start.
        :return: bool
        """
        return self._ready

    @ready.setter
    def ready(self, value):
        """
        Setter.
        :param value: bool
        :return: None
        """
        if isinstance(value, bool):
            self._ready = value
        return
