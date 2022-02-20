#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame
from pygame.locals import *
from packages.public.communication import Communication
from packages.player import Player
from packages.player.window import Window
from packages.player.commands import Commands
from packages.player.grid import Grid
from packages.player.table import Table
from packages.player.boat import Boat
from packages.public.logger import Logger


class Battleship(Communication):
    SERVER_HOSTNAME = "Karlito"
    TABLE_TITLE = "Fleet"
    TABLE_HEADER = ["#", "ship", "size"]
    GRID_SIZE = 10

    def __init__(self):
        """
        Constructor. Extends the Communication class.
        Connects the player with server.
        """
        super().__init__()
        self._window = Window(width=1080, height=720, margin=70)
        self._player = Player(connection=self, username="")     # TODO: add username
        self._player.connected = self.connect_to_server(hostname=Battleship.SERVER_HOSTNAME)
        self._commands = Commands(connection=self._player.connection)
        self._player_grid = Grid(rectangle=self._window.player_grid_rect, size=Battleship.GRID_SIZE)
        self._opponent_grid = Grid(rectangle=self._window.opponent_grid_rect, size=Battleship.GRID_SIZE)
        self._fleet_table = Table(rect=self._window.fleet_table_rect)   # we probably do not need these rect objects for Grids and Table!!!
        self._fill_table_data()

    def game_loop(self):
        """
        Main game loop.
        :return: None
        """
        self._commands.trace()  # starts the new thread
        self._window.show_welcome_screen()
        self._window.freeze(time=Window.WELCOME_SCREEN_SLEEP_TIME, func=self._check_for_quit)

        if not self._player.connected:  # Connecting with the server failed!
            self._window.show_connection_failed_screen()
            self._window.freeze(time=Window.CONNECTION_FAILED_SLEEP_TIME, func=self._check_for_quit)
            self._terminate()   # closes the game automatically

        while self._player.connected:
            # check server communication
            key, parameters = self._commands.get()
            if key is not None and parameters is not None:  # we have at least one unread message
                # handle the command
                pass

            # handle the game events
            self._check_for_quit()
            for event in pygame.event.get():
                pass

            # update the game stats

            # update the screen
            self._window.main_surface.blit(self._window.display_surface, self._window.window_rect)
            pygame.display.update()
            Window.FPS_CLOCK.tick(Window.FPS)

    def _check_for_quit(self):
        """
        Checks if user wants to close the game.
        Game can be closed either by mouse click on X
        or pressing the ESCAPE key.
        :return: None
        """
        for _ in pygame.event.get(QUIT):    # mouse press
            self._terminate()
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:   # ESCAPE keyup
                self._terminate()
            pygame.event.post(event)

    def _terminate(self):
        """
        Terminates the game.
        :return: None
        """
        # handle other threads, game loop, etc.
        Logger.print(message="Terminating...", type_=Logger.INFO)
        self._commands.end_tracing()    # ends trace tread
        self._commands.left()           # server command, closing the connection
        self._player.connected = False  # ends game loop
        self._commands.join()           # ensures program do not finish before trace thread is ended

        Logger.print(message="Terminated!", type_=Logger.INFO)
        pygame.quit()
        sys.exit()

    def _fill_table_data(self):
        """
        Method fills the table with
        appropriate data.
        :return: None
        """
        self._fleet_table.add_row(Battleship.TABLE_TITLE)
        self._fleet_table.add_row(*Battleship.TABLE_HEADER)
        for boat_index in range(len(Boat.NAMES)):
            self._fleet_table.add_row(Boat.QUANTITY[boat_index], Boat.NAMES[boat_index], Boat.SIZES[boat_index])
        self._fleet_table.fill()
        return


def main():
    battleship = Battleship()
    battleship.game_loop()


if __name__ == "__main__":
    main()
