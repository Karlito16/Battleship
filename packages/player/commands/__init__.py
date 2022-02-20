#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: commands

import threading
from packages.structures.queue import Queue
from packages.public.communication import Communication
from packages.public.logger import Logger


class Commands(Queue):
    GAME = "-game"
    READY = "-ready"
    STRIKE = "-strike"
    LEFT = "-left"
    STAY = "-stay"

    def __init__(self, connection):
        """
        Constructor. Extends the Queue class.
        Parameter connection represends connection
        between server and client (that is, player).
        Class Commands takes care of commands
        that server sends to the player.
        Then, for each command,
        calls appropriate method.
        :param connection: <class socket>
        """
        self._connection = connection
        super().__init__()
        self._thread = threading.Thread(target=self.trace)  # our thread
        self._running = False

    def trace(self):        # TODO: Be careful with program exit, and terminating this thread
        """
        Constantly receives the messages from the server.
        Method starts thread, first call is only
        for start, second is then the thread.
        :return: None
        """
        if not self._running:
            self._running = True
            self._thread.start()
        else:
            while self._running:
                key, parameters = Communication.receive(connection=self._connection)
                self.enqueue((key, parameters))
                # sleep?
            Logger.print(message="Tracing ended.", type_=Logger.INFO)

    def end_tracing(self):
        """
        Ends the trace thread.
        :return: None
        """
        self._running = False
        return

    def join(self):
        """
        Joins the thread.
        :return: None
        """
        self._thread.join()
        return

    def get(self):
        """
        Returns the latest received command.
        If there is no unread commands, returns a tuple
        (None, None).
        :return: tuple :: (str, str)
        """
        if self.size > 0:
            return self.dequeue()
        return None, None

    def left(self):
        """
        Client (that is, player) closed the game.
        Connection with server is closing.
        Informs server about leaving.
        :return: None
        """
        Communication.send_(connection=self._connection, message=f"{Commands.LEFT};")
        self._connection.close()
