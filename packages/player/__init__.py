#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: player

from packages.server.clients.client import Client


class Player(Client):

    def __init__(self, connection, username):
        """
        Constructor. Class extends Client class.
        :param connection: <class socket>
        :param username: str
        """
        super().__init__(connection=connection, username=username)
