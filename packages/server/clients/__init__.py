#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: clients

from packages.structures.queue import Queue


class Clients(Queue):

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()

    def __str__(self):
        """
        To string.
        :return: str
        """
        return super().__str__()

    def add_client(self, client):
        """
        Adds client to queue.
        :param client: <class Client>
        :return: bool
        """
        self.enqueue(value=client)
        return True

    def remove_all(self):
        """
        Removes all clients.
        :return: bool
        """
        while not self == []:
            self.remove_client(client=self.dequeue())
        return True

    def remove_client(self, client):
        """
        Removes specific client from queue.
        :param client: <class Client>
        :return: bool
        """
        if client in self:
            self.remove(client)
            return True
        return False

    def _in_check(self, reverse):
        """
        Parameter reverse simply means what we want to check.
        If set to False, we check clients that are in game.
        Otherwise, we check clients that are in lobby.
        :param reverse: bool
        :return: <class Queue>
        """
        ret = Queue()
        for client in self:
            if not client.in_game == reverse:
                ret.enqueue(value=client)
        return ret

    def in_game(self):
        """
        Returns queue of clients that are currently in game.
        :return: <class Queue>
        """
        return self._in_check(reverse=False)

    def in_lobby(self):
        """
        Returns queue of clients that are currently in lobby.
        :return: <class Queue>
        """
        return self._in_check(reverse=True)
