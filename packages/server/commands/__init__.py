#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: command

import functools
from packages.public.constants import Constants
from packages.public.logger import Logger
from packages.public.timer import Timer
from packages.server.clients.client import Client


def _time_offset(func):
    """
    Decorator. Sleeps before each command to ensure right communication.
    # TODO: Is this the best solution?
    :param func: function
    :return: function
    """
    functools.wraps(func)

    def time_offset_wrapper(*args, **kwargs):
        Timer.wait(t=Constants.COMMAND_TIME_OFFSET)
        return func(*args, **kwargs)

    return time_offset_wrapper


class Commands(object):

    def __init__(self, server):
        """
        Constructor. Each server has defined commands that he needs to perform.
        :param server: <class Server>
        """
        self._server = server

    @_time_offset
    def left(self, client):
        """
        This command is called when one of the clients exits
        during the game.
        Disconnects client, kills the game (if he was in the game),
        removes client from clients queue, informs opponent about
        action.
        :param client: <class Client>
        :return: bool
        """
        client.connected = False  # ends 'client trace' while loop in server.py
        if client.in_game:
            self._server.send_(connection=client.game.get_opponent(client=client).connection,
                               message=f"{Constants.CMD_LEFT};")
            client.game.end()
        self._server.clients.remove_client(client=client)
        return True

    @staticmethod
    def ready(client):
        """
        Checks if both clients are now ready.
        Returns True if they are.
        Server will then send command 'start' to them.
        :param client: <class Client>
        :return: bool
        """
        client.ready = True
        return client.game.get_opponent(client=client).ready

    def stay(self, client):
        """
        If client wants to stay, server moves him to the back of the queue.
        :param client: <class Client>
        :return: None
        """
        self._server.clients.remove_client(client=client)
        self._server.clients.add_client(client=client)
        return

    @_time_offset
    def get_username(self, connection):
        """
        Waits for client to send his username.
        Returns Client object if server received client's username succesfully.
        :param connection: <class socket>
        :return: <class Client>
        """
        username = ""
        try:
            timer = Timer(t=Constants.USERNAME_WAITING_TIME)
            timer.start()
            timer.join()
            while username == "":  # waits for username
                username = self._server.receive(connection=connection, command_key="-username")
        except RuntimeError as e:
            Logger.print(message=f"[RuntimeError]\t\t{e}")
            return None
        else:
            return Client(connection=connection, username=username)

    @_time_offset
    def game(self, client):
        """
        Informs client about newly created game in which he will be.
        :param client: <class Client>
        :return: None
        """
        try:
            self._server.send_(connection=client.connection, message=f"-game;{client.game.get_opponent(client=client).username}")
        except AttributeError:
            Logger.print(message=f"Game object: {type(client.game.get_opponent)}", type_=Logger.ERROR)
        return

    @_time_offset
    def strike(self, *args, **kwargs):
        """
        There are multiple sorts of this method.
        Server can send message "-strike;" to client that will
        be attacking. In that case (and all others), expected key arguments are:
            client: <class Client>
        Then, server can receive striking block position from attacker.
        Expected args are (i, j), where i and j are coordinates (int type).
        Third case is when defender sends message "-strike;[NUM]",
        where [NUM] stands for either miss or type of boat that has been hit.
        Expected arg is ([NUM]).
        Also, case where length of arg will be 1 is if defender is defeated.
        In that case, he will send "-strike;all".
        :param args: tuple
        :param kwargs: dict
        :return: bool
        """
        keys = kwargs.keys()
        if "client" not in keys:
            return False

        client = kwargs["client"]
        opponent = client.game.get_opponent(client=client)
        if len(args) == 0:  # informs client that it is now his turn for attack
            self._server.send_(connection=client.connection, message=f"{Constants.CMD_STRIKE};")  # informs attacker
            self._server.send_(connection=client.game.get_opponent(client=client).connection,    # informs defender
                               message=f"{Constants.CMD_DEFEND};")
        elif len(args) == 1:
            value = args[0]
            if value == "all":      # client lost, opponent won
                self._server.send_(connection=opponent.connection, message=f"{Constants.CMD_STRIKE};all")
                self._server.games.end_game(game_=client.game)
            elif value.strip('-').isdigit():  # informs opponent about attack
                self._server.send_(connection=opponent.connection, message=f"{Constants.CMD_STRIKE};{value}")
            else:
                Logger.print(message=f"[Error 117]\t\tInvalid args: {args}")
                return False
        elif len(args) == 2:
            try:
                i, j = map(int, args)
            except ValueError as e:
                Logger.print(message=f"[Error 104]\t\t{e}")
                return False
            else:   # forwards the attacker's choice to the opponent
                self._server.send_(connection=opponent.connection, message=f"{Constants.CMD_STRIKE};{str(i)}|{str(j)}")
        else:
            Logger.print(message=f"[Error 116]\t\tInvalid args: {args}")
            return False
        return True
