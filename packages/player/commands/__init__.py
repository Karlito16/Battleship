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
    DEFEND = "-defend"

    def __init__(self, player):
        """
        Constructor. Extends the Queue class.
        Parameter player represends the player.
        Class Commands takes care of commands
        that server sends to the player.
        Then, for each command,
        calls appropriate method.
        :param player: <class player>
        """
        self._player = player
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
                key, parameters = Communication.receive(connection=self._player.connection)
                self.enqueue((key, parameters))
                # sleep?
            Logger.print(message="Tracing ended.", type_=Logger.INFO)
        return

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
        if len(self) > 0:
            return self.dequeue()
        return None, None

    def check(self):
        """
        Checks the newly received messages from the server.
        If some, method then calls the appropriate command method.
        :return: None
        """
        # check server communication
        key, parameters = self.get()
        if not isinstance(parameters, str):
            return
        if key is not None and parameters is not None:  # we have at least one unread message
            # handle the command
            if key == Commands.GAME and self._player.in_lobby:
                # self._player.in_game = True
                self.game()
            elif key == Commands.LEFT:  # opponent left the game
                # self._player.in_game = False  # this will stop the game and return player to the lobby, if connected
                self.left()
            elif key == Commands.STRIKE:
                if parameters == "":    # we are attacker
                    self.strike()
                elif '|' in parameters:     # we are attacked
                    self.strike(*parameters.split('|'))
                elif parameters == "all" or parameters.strip('-').isdigit():
                    # opponent is defeated or informs us about our strike
                    self.strike(parameters)
            elif key == Commands.DEFEND:
                # we are defender
                self.defend()
        return

    def left(self):
        """
        Client (that is, player) closed the game.
        Connection with server is closing.
        Informs server about leaving.
        :return: None
        """
        Communication.send_(connection=self._player.connection, message=f"{Commands.LEFT};")
        self._player.in_game = False
        self._player.connection.close()
        return

    def game(self):
        """
        Player joins the game.
        Game screen must be shown.
        Starts with fleet drawing.
        When finished, sends ready to server.
        :return: None
        """
        self._player.in_game = True
        return

    def ready(self, *args):
        """
        Player is ready for the game or
        player received striking box coords /
        striking box type, depending on
        who is attacker, and who is defender.
        Args can contain additional parameters,
        such as "fleet" for specifing for what
        is client ready.
        :return: None
        """
        parameters = ""
        if args != ():
            parameters = '|'.join(args)
        Communication.send_(connection=self._player.connection, message=f"{Commands.READY};{parameters}")

    def strike(self, *args, **kwargs):
        """
        Several options for this command.
        Player can receive an empty command
        (no parameters). That means he is
        attacking.
        Then, player can either send or
        receive this command with box coords
        parameters. Keyword send=True means
        player needs to send that command
        (that is, he is attacker), otherwise
        he receives that command from attacker.
        Then, other implementation of this command
        is when player (attacker) receives
        box type (-1, 0, 1, ...). But just as
        before, this same message defender needs
        to send. So we will also use keyword
        'send=True', but 'send=False', respectively.
        If player is defeated, he sends "-strike;all".
        Other player receives this same message.
        We know keyword that we need here, too.
        :param args: tuple
        :param kwargs: dict
        :return: None
        """
        send = False
        if "send" in kwargs.keys():
            send = kwargs["send"]
            if not isinstance(send, bool):
                raise TypeError(f"Send must be bool type, got {type(send)} instead.")

        # case 1: player will be attacker
        if args == ():
            self._player.attack = True  # this will end while loop in defend method
            # self._player.strike()
        elif len(args) == 1:    # case 2 and 3: -strike;type (send, receive) or -strike;all (send, receive)
            if send:    # defender
                Communication.send_(connection=self._player.connection,
                                    message=f"{Commands.STRIKE};{str(args[0])}")
            else:   # attacker
                value = args[0]
                if value.strip('-').isdigit():  # box type
                    self._player.mark_box_type(int(value))
                    # inform server that you are ready for the next round - attacker
                    self.ready()
                else:   # all - win!
                    # end of the game
                    self._player.won = True
                    self._player.in_game = False
        elif len(args) == 2:    # case 4: -strike;i|j (send, receive)
            if send:    # attacker
                Communication.send_(connection=self._player.connection,
                                    message=f"{Commands.STRIKE};{str(args[0])}|{str(args[1])}")
            else:   # defender
                box_type = self._player.check_strike(int(args[0]), int(args[1]))
                self.strike(box_type, send=True)
                # check if player lost
                if self._player.is_defeated():
                    self.strike("all", send=True)  # game over
                    self._player.in_game = False
                else:
                    # defender is still alive, informs server that he is ready for next round
                    self.ready()

    def defend(self):
        """
        Client receives this message when opponent is attacking him.
        This is also indicator of the game start as well as the new turn.
        :return: None
        """
        self._player.attack = False
        self._player.defend()
        return
