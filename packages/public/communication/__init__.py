#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: communication

import time
import socket
from packages.public.logger import Logger


class Communication(socket.socket):
    _coding = "UTF-8"
    _buffer = 1024  # TODO: can be reduced! chech this later! optimize!
    _send_sleep = 0.1
    _recv_sleep = 0.0001
    _port = 10000
    _listen = 5

    def __init__(self):
        """
        Constructor.
        """
        super().__init__()
        self._hostname = socket.gethostname()

    def start_server(self, func, *args, **kwargs):
        """
        Connects the computer with network. Starts server function.
        Returns True if server is successfully started, otherwise False.
        :param func: function
        :param args: tuple
        :param kwargs: dict
        :return: bool
        """
        try:
            self.bind((self._hostname, Communication._port))
            self.listen(Communication._listen)
        except Exception as e:
            Logger.print(f"[Error 38]\t\t{e}")
            return False
        else:
            func(*args, **kwargs)
            return True

    @Logger.wait_info
    def wait(self):
        """
        Waits for new clients.
        :return: <class socket>
        """
        return self.accept()

    @staticmethod
    @Logger.sending_info
    def send(connection, message):
        """
        Sending the message.
        :param connection: <socket>
        :param message: string
        :return: bool
        """
        try:
            connection.send(message.encode(Communication._coding))
            time.sleep(Communication._send_sleep)
        except Exception as exception:
            # print(f"[Error 37]\t{exception}\nFailed to send the message.")
            Logger.print(message=f"[Error 37]\t{exception}\nFailed to send the message.")
            return False
        else:
            return True

    @staticmethod
    def send_to_all(sequence, message):
        """
        Sending the message to the all members of the sequence.
        :param sequence: list :: [<class Client>]
        :param message: str
        :return: None
        """
        for client in sequence:
            Communication.send(connection=client.connection, message=message)

    @staticmethod
    @Logger.receive_info
    def receive(connection, command_key=None):
        """
        Gets the message from the connection object according to command key.
        If command key is None, function returns full message. Otherwise,
        for example, if client sends his username, server wants to read it.
        Then, command key is "-username". If he succeedes to read it,
        returns value, otherwise "" (False).
        :param connection: <class socket>
        :param command_key: string (default is None)
        :return: str or list :: [str, str]
        """
        try:
            message = connection.recv(Communication._buffer).decode(Communication._coding)
        except Exception as exception:
            # print(f"[Error 79]\t{exception}\nFailed to receive a message.")
            Logger.print(message=f"[Error 79]\t{exception}\nFailed to receive a message.")
            return
        else:
            if command_key is None:
                # if "-result" in message or "-leaderboard" in message or "-end" in message:
                #     return message.split(";")   # because dictionary has ':' in his syntax
                # else:
                return message.split(";")
            else:
                cmd_key, value = message.split(";")
                if cmd_key == command_key:
                    return value
                return ""
