#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: command

import functools
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
        Timer.wait(t=Commands.each_command_time_offset)
        return func(*args, **kwargs)

    return time_offset_wrapper


class Commands(object):
    _each_command_time_offset = 1e-3
    _username_waiting_time = 10  # seconds

    def __init__(self, server):
        """
        Constructor. Each server has defined commands that he needs to perform.
        :param server: <class Server>
        """
        self._server = server

    @_time_offset
    def client_left(self, client):
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
            self._server.send(connection=client.game.get_opponent(client=client).connection,
                              message=f"-left;")
            client.game.kill()
        self._server.clients.remove_client(client=client)
        return True

    @staticmethod
    def clients_ready(client):
        """
        Checks if both clients are now ready.
        Returns True if they are.
        Server will then send command 'start' to them.
        :param client: <class Client>
        :return: bool
        """
        client.ready = True
        return client.game.get_opponent(client=client).ready

    def client_stay(self, client):
        """
        If client wants to stay, server moves him to the back of the queue.
        :param client: <class Client>
        :return: None
        """
        self._server.clients.remove_client(client=client)
        self._server.clients.add_client(client=client)
        return

    @property
    def each_command_time_offset(self):
        """
        Getter.
        :return: float
        """
        return Commands._each_command_time_offset

    @_time_offset
    def game_start(self, game):
        """
        Informs clients that both of them are ready to start with game.
        Game starts.
        :param game: <class Game>
        :return: bool
        """
        self._server.send_to_all(sequence=game.clients, message=f"-start;")
        game.start()    # new Thread!
        game.join()
        for client in game.clients:
            # we will use this attribute later for each turn, clients will send ready before the start of each turn
            client.ready = False
        return True

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
            timer = Timer(t=Commands._username_waiting_time)
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
    def new_game(self, client):
        """
        Informs client about newly created game in which he will be.
        :param client: <class Client>
        :return: None
        """
        self._server.send(connection=client.connection, message=f"-game;{client.game.get_opponent(client=client).username}")
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
            self._server.send(connection=client.connection, message="-strike;")
        elif len(args) == 1:
            value = args[0]
            if value == "all":      # client lost, opponent won
                self._server.send(connection=opponent.connection, message="-strike;all")
                self._server.games.end_game(game=client.game)
            elif isinstance(value, int):    # informs opponent about attack
                self._server.send(connection=opponent.connection, message=f"-strike;{value}")
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
                self._server.send(connection=opponent.connection, message=f"-strike;{str(i)}|{str(j)}")
        else:
            Logger.print(message=f"[Error 116]\t\tInvalid args: {args}")
            return False
        return True
