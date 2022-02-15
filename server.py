#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading

from packages.server.clients import Clients
from packages.server.commands import Commands
from packages.public.communication import Communication
from packages.public.logger import Logger
from packages.server.games import Games


class Server(Communication):

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self._clients = Clients()
        self._games = Games()
        self._commands = Commands(server=self)

    @property
    def clients(self):
        """
        Getter. Returns clients queue.
        :return: <class Clients>
        """
        return self._clients

    @property
    def games(self):
        """
        Getter. Returns games list.
        :return: <class Games>
        """
        return self._games
    
    @property
    def commands(self):
        """
        Getter. Returns the commands object.
        :return: <class Commands>
        """
        return self._commands

    def running(self):
        """
        Main server loop.
        Waits and accepts new clients.
        Starts new games when ready.
        :return: None
        """
        while True:
            connection, address = self.wait()
            thread = threading.Thread(target=self.trace, args=(connection, ))
            thread.start()

            clients = self._clients.in_lobby().peek(n=2)
            if clients != [] and self._games.available():
                self._games.new_game(server=self, clients=clients)

    def trace(self, connection):
        """
        Thread for each client. Thread is active while client is
        connected to the server.
        :param connection: <class socket>
        :return: None
        """
        client = Commands.get_username(connection=connection)
        if client:
            client.connected = True
            self._clients.add_client(client=client)
        else:
            return
        # runs this loop while client is connected to the server
        while client.connected:
            cmd_key, value = self.receive(connection=connection)

            if cmd_key == "-left":
                self._commands.client_left(client=client)

            elif cmd_key == "-ready":
                if Commands.clients_ready(client=client):
                    if client.in_game:  # this means both of them are in the game
                        client.game.next_turn = True
                    else:
                        self._commands.game_start(game=client.game)

            elif cmd_key == "-stay":
                self._commands.client_stay(client=client)

            elif cmd_key == "-strike":
                if value == "":
                    self._commands.strike(client=client)
                elif '|' in value:
                    self._commands.strike(*value.split('|'), client=client)
                else:
                    self._commands.strike(value, client=client)

            else:
                Logger.print(message=f"[Warning 101]\t\tInvalid command: {cmd_key} from {client}")
        return


def main():
    server = Server()
    server.start_server(func=server.running)


if __name__ == '__main__':
    main()
