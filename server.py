#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

from packages.server.clients import Clients
from packages.server.clients.client import Client
from packages.server.commands import Commands
from packages.public.communication import Communication
from packages.public.logger import Logger
from packages.server.games import Games
from packages.public.constants import Constants


class Server(Communication):

    def __init__(self, ip_address):
        """
        Constructor.
        """
        super().__init__(ip_address=ip_address)
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
        # create and init client object
        client = Client(connection=connection, username="")
        client.connected = True
        self._clients.add_client(client=client)

        # runs this loop while client is connected to the server
        while client.connected:
            cmd_key, value = self.receive(connection=connection)

            if cmd_key == Constants.CMD_LEFT:
                self._commands.left(client=client)

            elif cmd_key == Constants.CMD_READY:
                if Commands.ready(client=client):
                    if value != "":
                        # value can be "fleet" - player has drawn the fleet and is now ready for the game start
                        client.game.start()
                    elif value == "":
                        client.game.next_turn = True

            elif cmd_key == Constants.CMD_STAY:
                self._commands.stay(client=client)

            elif cmd_key == Constants.CMD_STRIKE:
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
    # server = Server(ip_address=socket.gethostbyname(socket.gethostname()))
    server = Server(ip_address="192.168.5.120")
    # print(socket.gethostname())
    # print(socket.gethostbyname("KarlitoHome"))   # error?
    # print(socket.gethostbyaddr("192.168.5.120"))
    server.start_server(func=server.running)


if __name__ == '__main__':
    main()
