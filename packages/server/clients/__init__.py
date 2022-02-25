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
        # tmp_queue = Queue()
        # removed = False
        # while True:
        #     element_value = self.dequeue()
        #     # queue if empty
        #     if element_value is None:
        #         break
        #     if element_value != client:
        #         tmp_queue.enqueue(element_value)
        #     else:
        #         removed = True
        # while True:
        #     element_value = tmp_queue.dequeue()
        #     if element_value is None:
        #         break
        #     self.enqueue(element_value)
        # return removed
        if client in self:
            self.remove(client)
            return True
        return False

    def in_game(self, reverse=False):
        """
        Returns queue of clients that are currently in game.
        Parameter reverse simply means what we want to check.
        If set to False, we check clients that are in game.
        Otherwise, we check clients that are in lobby.
        :param reverse: bool
        :return: <class Queue>
        """
        # ret = Queue()
        # element = self.iterator.begin()
        # while not self.iterator.end():
        #     client = element.get_value()
        #     if not client.in_game == reverse:
        #         ret.enqueue(value=client)
        #     element = self.iterator.next()
        # return ret
        ret = Queue()
        for client in self:
            if not client.in_game == reverse:
                ret.enqueue(value=client)
        return ret

    def in_lobby(self):
        """
        Returns queue of clients that are currently in lobby.
        :return: <class Queue>
        """
        return self.in_game(reverse=True)
