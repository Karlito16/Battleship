#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: window

import pygame
from packages.player.point import Point


class Window(object):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    BGCOLOR = WHITE

    FONT_NAME_1 = "freesansbold.ttf"
    FONT_SIZE_1 = 72
    FONT_SIZE_2 = 36
    FONT_SIZE_3 = 24

    FPS = 30
    FPS_CLOCK = pygame.time.Clock()

    WELCOME_SCREEN_SLEEP_TIME = 2    # seconds
    CONNECTION_FAILED_SLEEP_TIME = 2    # seconds

    def __init__(self, width, height, margin):
        """
        Constructor. Width and height are parameters for window size.
        Margin is size of x and y margins of the window.
        Constructor then defines other important attributes
        for our window.
        :param width: int
        :param height: int
        :param margin: int
        """
        self._width = width
        self._height = height
        self._margin = margin

        # init the window
        pygame.init()
        self._main_surface = pygame.display.set_mode((self._width, self._height))
        self._main_surface.fill(Window.BGCOLOR)
        pygame.display.set_caption("Battleship")
        self._display_surface = self._main_surface.copy()       # surface for showing the current screen
        self._window_rect = (0, 0, self._width, self._height)

        # Rectangles sizes, will be created later
        self._player_grid_size = self._width - self._height
        self._opponent_grid_size = self._height - 3 * self._margin
        self._fleet_table_size = 2 * self._height - self._width - 3.5 * self._margin

        # These points are on the top left corner of each rectangle that will be
        # created later
        self._player_grid_point = Point(x=self._margin,
                                        y=2 * self._margin)
        self._opponent_grid_point = Point(x=2 * self._margin + self._player_grid_size,
                                          y=2 * self._margin)
        self._fleet_table_point = Point(x=self._margin,
                                        y=2.5 * self._margin + self._player_grid_size)

        # Rectangles
        self._player_grid_rect = pygame.Rect(self._player_grid_point.x,
                                             self._player_grid_point.y,
                                             self._player_grid_size,
                                             self._player_grid_size)
        self._opponent_grid_rect = pygame.Rect(self._opponent_grid_point.x,
                                               self._opponent_grid_point.y,
                                               self._opponent_grid_size,
                                               self._opponent_grid_size)
        self._fleet_table_rect = pygame.Rect(self._fleet_table_point.x,
                                             self._fleet_table_point.y,
                                             self._fleet_table_size,
                                             self._fleet_table_size)

    @property
    def width(self):
        """
        Getter for attribute witdh.
        :return: int
        """
        return self._width

    @property
    def height(self):
        """
        Getter for attribute height.
        :return: int
        """
        return self._height

    @property
    def margin(self):
        """
        Getter for attribute margin.
        :return: int
        """
        return self._margin

    @property
    def main_surface(self):
        """
        Getter for attribute main_surface.
        :return: <class Surface>
        """
        return self._main_surface

    @property
    def display_surface(self):
        """
        Getter for attribute display_surface.
        :return: <class Surface>
        """
        return self._display_surface

    @property
    def window_rect(self):
        """
        Getter for attribute window_rect.
        :return: <class Rect>
        """
        return self._window_rect

    @property
    def player_grid_rect(self):
        """
        Getter.
        :return: <class Rect>
        """
        return self._player_grid_rect

    @property
    def opponent_grid_rect(self):
        """
        Getter.
        :return: <class Rect>
        """
        return self._opponent_grid_rect

    @property
    def fleet_table_rect(self):
        """
        Getter.
        :return: <class Rect>
        """
        return self._fleet_table_rect

    # ...

    def show_welcome_screen(self, animation=False):
        """
        Sets the welcome screen as currently displayed screen.
        Animation can be added as effect.
        Method returns surface and rectangule for this screen.
        :param animation: bool
        :return: None
        """
        if animation:
            pass

        self._main_surface.fill(Window.BGCOLOR)     # clear surface

        caption_surf, caption_rect = Window._create_text(Window.FONT_NAME_1, Window.FONT_SIZE_1,
                                                         "BATTLESHIP", Window.BLACK, Window.WHITE)
        caption_rect.midtop = (self._width / 2, self._height / 4)

        message_surf, message_rect = Window._create_text(Window.FONT_NAME_1, Window.FONT_SIZE_2,
                                                         "Connecting to the server...", Window.BLACK, Window.WHITE)
        message_rect.midbottom = (self._width / 2, self._height * 0.75)

        self._display_surface.blit(caption_surf, caption_rect)
        self._display_surface.blit(message_surf, message_rect)
        return None

    def show_connection_failed_screen(self, animation=False):
        """
        Sets the connection failed screen as currently displayed screen.
        This happens when connecting with server fails, or connection
        breaks during the game.
        :param animation: bool
        :return: None
        """
        if animation:
            pass

        self._main_surface.fill(Window.BGCOLOR)  # clear surface

        caption_surf, caption_rect = Window._create_text(Window.FONT_NAME_1, Window.FONT_SIZE_1,
                                                         "ERROR", Window.BLACK, Window.BLACK)
        caption_rect.midtop = (self._width / 2, self._height / 4)

        message_surf, message_rect = Window._create_text(Window.FONT_NAME_1, Window.FONT_SIZE_1,
                                                         "Connecting to the server has failed!", Window.WHITE, Window.BLACK)
        message_rect.midbottom = (self._width / 2, self._height * 0.75)

        self._display_surface.blit(caption_surf, caption_rect)
        self._display_surface.blit(message_surf, message_rect)
        return None

    @staticmethod
    def _create_text(font_name, font_size, text, fg, bg):
        """
        Private method, just to better organize our code, as we will
        need to create a text many times.
        Method returns text surface and text rectangle.
        :param font_name: str
        :param font_size: int
        :param text: str
        :param fg: str
        :param bg: str
        :return: tuple :: (<class Surface>, <class Rect>)
        """
        font = pygame.font.Font(font_name, font_size)
        surf = font.render(text, True, fg, bg)
        rect = surf.get_rect()
        return surf, rect

    def freeze(self, time, func):
        """
        Freezes the currently displayed screen for a given time (seconds).
        Method needs to perform given function during the freeze,
        so we will not just pause the program on given time,
        instead there is a for loop which ensures enough function
        calls. In our example, we will need to check if user wants
        to close the app during the freeze.
        :param time: int
        :param func: function
        :return: None
        """
        number_of_iterations = time * Window.FPS
        for _ in range(number_of_iterations):
            func()
            self._main_surface.blit(self._display_surface, self._window_rect)
            pygame.display.update()
            Window.FPS_CLOCK.tick(Window.FPS)
        return
