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
    GAME_CAPTION = "Battleship"
    WIN_WIDTH = 1080   # px
    WIN_HEIGHT = 720   # px
    WIN_MARGIN = 70    # px
    GRID_SIZE = 10
    GRID_BORDER_WIDTH = 4   # px
    GRID_HIGHLIGHT_BORDER_WIDTH = 1  # px
    TABLE_MARGIN = 10   # px
    TABLE_ROW_MARGIN = 4    # px

    def __init__(self):
        """
        Constructor. Extends the Communication class.
        Connects the player with server.
        """
        super().__init__()
        self._init_surf_areas()
        self._window = Window(caption=Battleship.GAME_CAPTION, width=Battleship.WIN_WIDTH,
                              height=Battleship.WIN_HEIGHT, margin=Battleship.WIN_MARGIN)
        self._player_grid = Grid(rect=self._player_grid_rect, size=Battleship.GRID_SIZE,
                                 border_width=Battleship.GRID_BORDER_WIDTH,
                                 highlight_border_width=Battleship.GRID_HIGHLIGHT_BORDER_WIDTH)
        self._opponent_grid = Grid(rect=self._opponent_grid_rect, size=Battleship.GRID_SIZE,
                                   border_width=Battleship.GRID_BORDER_WIDTH,
                                   highlight_border_width=Battleship.GRID_HIGHLIGHT_BORDER_WIDTH)
        self._fleet_table = Table(rect=self._fleet_table_rect, margin=Battleship.TABLE_MARGIN,
                                  row_margin=Battleship.TABLE_ROW_MARGIN)
        self._fill_table_data()
        self._player = Player(window=self._window, his_grid=self._player_grid, opponent_grid=self._opponent_grid,
                              fleet_table=self._fleet_table, connection=self, username="")     # TODO: add username
        self._player.connected = self.connect_to_server(hostname=Battleship.SERVER_HOSTNAME)
        self._commands = Commands(player=self._player)

    def _init_surf_areas(self):
        """
        Method initiales rectangles, areas
        for our display surfaces.
        :return: None
        """
        # easier variable names
        win_w = Battleship.WIN_WIDTH
        win_h = Battleship.WIN_HEIGHT
        margin = Battleship.WIN_MARGIN
        self._player_grid_rect = pygame.Rect(margin, 2 * margin, win_w - win_h, win_w - win_h)
        self._opponent_grid_rect = pygame.Rect(2 * margin + win_w - win_h, 2 * margin, win_h - 3 * margin, win_h - 3 * margin)
        self._fleet_table_rect = pygame.Rect(margin, 2.5 * margin + win_w - win_h, win_w - win_h, 2 * win_h - win_w - 3.5 * margin)
        return

    def _fill_table_data(self):
        """
        Method fills the table with
        appropriate data.
        :return: None
        """
        self._fleet_table.add_row("Fleet")
        self._fleet_table.add_row('#', "Name", "Size")
        for boat_index in range(len(Boat.NAMES)):
            if Boat.QUANTITY[boat_index] > 0:   # only useful for testing
                self._fleet_table.add_row(str(Boat.QUANTITY[boat_index]),
                                          Boat.NAMES[boat_index],
                                          str(Boat.SIZES[boat_index]))
        return

    @property
    def window(self):
        """
        Getter.
        :return: <class Window>
        """
        return self._window

    @property
    def player(self):
        """
        Getter.
        :return: <class Player>
        """
        return self._player

    @property
    def commands(self):
        """
        Getter.
        :return: <class Commands>
        """
        return self._commands

    @property
    def player_grid(self):
        """
        Getter.
        :return: <class Grid>
        """
        return self._player_grid

    @property
    def opponent_grid(self):
        """
        Getter.
        :return: <class Grid>
        """
        return self._opponent_grid

    @property
    def fleet_table(self):
        """
        Getter.
        :return: <class Table>
        """
        return self._fleet_table

    def lobby_loop(self):
        """
        Main lobby loop.
        :return: None
        """
        if self._player.connected:
            self._commands.trace()  # starts the new thread
        self._window.show_welcome_screen()
        self._window.freeze(time=Window.WELCOME_SCREEN_SLEEP_TIME, func=self.check_for_quit)

        if not self._player.connected:  # Connecting with the server failed!
            self._window.clear()
            self._window.show_connection_failed_screen()
            self._window.freeze(time=Window.CONNECTION_FAILED_SLEEP_TIME, func=self.check_for_quit)
            self._terminate()   # closes the game automatically

        self._window.show_waiting_for_player_screen()
        while self._player.connected:
            # check server communication
            self._commands.check()

            # handle the game events
            self.check_for_quit()

            # update the game stats
            if self._player.in_game:    # command check received "-game;" message from the server
                self.game_loop()  # here the game loop starts
                self._window.clear()
                self._window.show_game_over_screen(win=self._player.won)

            # update the screen
            self._window.update()

    def game_loop(self):
        """
        Main game loop.
        :return: None
        """
        # self._window.show_game_screen(self._player_grid, self._opponent_grid, self._fleet_table)
        self._player.create_fleet()
        while self._player.in_game:
            # start of the game!
            # refresh the screen (that is, clear) so we can see changes
            self._window.clear()
            self._window.show_game_screen(self._player)  # redraw

            # check server communication
            self._commands.check()

            # handle the game events
            self.check_for_quit()

            # update the game stats
            if self._player.attack:
                self._player.strike()

            # update the screen
            # ### we need to clear up display surface, as highlighted boxes and shapes are constantly changing
            # self.connection.window.display_surface.fill(Window.BGCOLOR)  # clear
            self._window.update()
        return

    @staticmethod
    def check_mouse_events():
        """
        Checks mouse events.
        Returns mousex, mousey, clicked.
        :return: tuple
        """
        clicked = False
        mousex, mousey = (0, 0)     # if no movement had happend
        for event in pygame.event.get(MOUSEMOTION):
            mousex, mousey = event.pos
        for event in pygame.event.get(MOUSEBUTTONUP):
            mousex, mousey = event.pos
            clicked = True
        # Logger.print(message=f"Mouse: ({mousex}, {mousey}, {clicked})", type_=Logger.INFO)
        return mousex, mousey, clicked

    def check_for_quit(self):
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
        if self._player.connected:
            self._commands.end_tracing()  # ends trace tread
            self._commands.left()           # server command, closing the connection
            self._player.connected = False  # ends game loop
            self._commands.join()           # ensures program do not finish before trace thread is ended

        Logger.print(message="Terminated!", type_=Logger.INFO)
        pygame.quit()
        sys.exit()


def main():
    battleship = Battleship()
    battleship.lobby_loop()


if __name__ == "__main__":
    main()
