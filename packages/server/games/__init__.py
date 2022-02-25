#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: games

from packages.server.games.game import Game


class Games(list):
    _games_at_once_limit = 2  # only 2 games can be played at once

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self._size = 0

    def add_game(self, game_):
        """
        Adds game to games list.
        :param game_: <class Game>
        :return: None
        """
        self.append(game_)
        self._size += 1
        return

    def available(self):
        """
        Returns if new game can be created or not.
        Depends on number of currently active games.
        :return: bool
        """
        return self._size < Games._games_at_once_limit

    def end_game(self, game_):
        """
        Ends game.
        Returns clients to the lobby.
        :param game_: <class Game>
        :return: bool
        """
        game_.end()
        for client in game_.clients:
            client.in_game = False
            client.game = None
        self.remove_game(game_)
        return True

    def new_game(self, server, clients):
        """
        Creates the new game.
        Informs clients.
        :param server: <class Server>
        :param clients: list
        :return: bool
        """
        if len(clients) == 2:
            client1, client2 = clients
        else:
            return False
        game_ = Game(server=server, client1=client1, client2=client2)
        for client in game_.clients:
            client.game = game_
            client.in_game = True
            server.commands.new_game(client=client)
        self.add_game(game_)
        return True

    def remove_game(self, game_):
        """
        Removes game from games list.
        :param game_: <class Game>
        :return: <class Game>
        """
        self._size -= 1
        return self.pop(self.index(game_))

    @property
    def size(self):
        """
        Returns number of active games.
        :return: int
        """
        return self._size
