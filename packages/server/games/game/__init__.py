#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: game

import threading
from packages.public.timer import Timer
from packages.public.logger import Logger


class Game(threading.Thread):
    _game_loop_time_offset = 1e-9

    def __init__(self, server, client1, client2):
        """
        Constructor.
        :param server: <class Server>
        :param client1: <class Client>
        :param client2: <class Client>
        """
        self._server = server
        self._client1 = client1
        self._client2 = client2
        super().__init__(target=self._run)
        self._running = False
        self._next_turn = True
        self._stopwatch = Timer()

    def __str__(self):
        """
        To string method.
        :return: str
        """
        return f"Game({self._server.__str__()}, {', '.join(map(lambda c: c.__str__(), self.clients))})"

    @property
    def clients(self):
        """
        Returns tuple object with clients.
        :return: tuple
        """
        return self._client1, self._client2

    def end(self):
        """
        Ends the game loop.
        :return: None
        """
        self._running = False
        self._stopwatch.end()
        return

    def get_opponent(self, client):
        """
        Returns the other client.
        :param client: <class Client>
        :return: <class Client>
        """
        if client == self._client1:
            return self._client1
        return self._client2

    def kill(self):
        """
        Kills the game. This is not an ordinary end of game.
        Caused by client disconnection, etc.
        :return: None
        """
        self._stopwatch.end()
        return

    @property
    def next_turn(self):
        """
        Getter. Returns the next turn status.
        :return: bool
        """
        return self._next_turn

    @next_turn.setter
    def next_turn(self, value):
        """
        Setter.
        :param value: bool
        :return: None
        """
        self._next_turn = value
        return

    @property
    def running(self):
        """
        Property. Returns if game is running.
        :return: bool
        """
        return self._running

    def _run(self):
        """
        Thread. Main game loop.
        Game can be either killed or ended.
        Only difference is that when killed,
        atribute running will not be changed.
        :return: None
        """
        self._running = True
        try:
            self._stopwatch.start()
            self._stopwatch.join()
            while self._running:
                for client in self.clients:
                    self._server.commands.strike(client=client)
                    self._next_turn = False
                    while not self._next_turn:
                        Timer.wait(t=Game._game_loop_time_offset)
        except RuntimeError:
            if self._running:
                # breaks the game loop, probably because one of players lost connection etc.
                Logger.print(f"[Warning 108]\t\tGame {self} has been killed.")
            else:
                # regular break of the loop
                Logger.print(f"Game {self.__str__()} has finished!")
        return

    @property
    def server(self):
        """
        Getter. Returns the game server.
        :return: <class Server>
        """
        return self._server
