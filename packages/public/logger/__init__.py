#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: logger

import functools


class Logger(object):
    INFO = "[INFO]\t\t"

    _logger = True   # hardcoding

    def __str__(self):
        """
        Creates the output value.
        :return: str
        """
        return f"Logger: {self._logger}"

    @staticmethod
    def print(message, type_=None):
        """
        Prints the message if it is allowed.
        :param message: str
        :param type_: str
        :return: None
        """
        if Logger._logger:
            if type_ is None:
                print(message)
            else:
                print(f"{type_}{message}")
        return

    @staticmethod
    def receive_info(func):
        """
        Logger.
        :param func: function
        :return: function
        """
        functools.wraps(func)

        def receive_info_wrapper(*args, **kwargs):
            if 'command_key' in kwargs.keys():
                value = func(*args, **kwargs)
                items = kwargs.items()
                for cmd_key, value_ in items:
                    if value_ == value:
                        # print(f"[Received]\t\t\tMessage: {cmd_key}:{value}")
                        Logger.print(message=f"[Received]\t\t\tMessage: {cmd_key};{value}")
                return value
            else:
                try:
                    cmd_key, value = func(*args, **kwargs)
                except TypeError as e:
                    # this happens when client disconnects, then socket method "recv" returns None,
                    # which cannot be unpacked
                    return None, None
                else:
                    Logger.print(message=f"[Received]\t\tMessage: {cmd_key};{value}")
                    return cmd_key, value

        return receive_info_wrapper

    @staticmethod
    def sending_info(func):
        """
        Logger.
        :param func: function
        :return: function
        """
        functools.wraps(func)

        def sending_info_wrapper(*args, **kwargs):
            # print(f"[Sending...]\t\tMessage: {kwargs['message']}")
            Logger.print(message=f"[Sending...]\t\tMessage: {kwargs['message']}")
            return func(*args, **kwargs)

        return sending_info_wrapper

    @staticmethod
    def wait_info(func):
        """
        Logger.
        :param func: function
        :return: function
        """
        functools.wraps(func)

        def wait_info_wrapper(*args, **kwargs):
            Logger.print(message="[Waiting...]")
            conn, addr = func(*args, **kwargs)
            Logger.print(message=f"[Connected]\t\tClient {addr} is connected.")
            return conn, addr

        return wait_info_wrapper


def main():
    logger = Logger()
    print(logger)


if __name__ == '__main__':
    main()
