#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: window

import pygame
from packages.public.constants import Constants


class Window(object):

    def __init__(self, caption, width, height, margin):
        """
        Constructor. Width and height are parameters for window size.
        Margin is size of x and y margins of the window.
        Constructor then defines other important attributes
        for our window.
        :param caption: str
        :param width: int
        :param height: int
        :param margin: int
        """
        self._caption = caption
        self._width = width
        self._height = height
        self._margin = margin

        self._message = ""

        # init the window
        pygame.init()
        self._display_surf = pygame.display.set_mode((self._width, self._height))    # constant, display surface for our window
        self.DISPLAYSURF.fill(Constants.BGCOLOR)
        pygame.display.set_caption(self._caption)

    @property
    def caption(self):
        """
        Getter.
        :return: str
        """
        return self._caption

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
    def DISPLAYSURF(self):  # constant
        """
        Getter for constant attribute _display_surf.
        :return: <class Surface>
        """
        return self._display_surf

    @property
    def message(self):
        """
        Getter for attribute message.
        :return: str
        """
        return self._message

    @message.setter
    def message(self, value):
        """
        Setter for atribute message.
        :param value: str
        :return: None
        """
        self._message = value
        return

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
        self._show_caption_message_screen(caption=self._caption, message="Connecting to the server...")
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
        self._show_caption_message_screen(caption="ERROR", message="Connecting to the server has failed!")
        return None

    def show_waiting_for_player_screen(self, animation=False):
        """
        Sets the waiting for player screen as currently displayed screen.
        This happens when player joins an empty lobby.
        :param animation: bool
        :return: None
        """
        if animation:
            pass
        self._show_caption_message_screen(caption=self._caption, message="Waiting for another player...")
        return None

    def show_game_screen(self, player, animation=False):
        """
        Sets the game screen as currently displayed screen.
        This happens when player joins the game.
        :param player: <class Player>
        :param animation: bool
        :return: None
        """
        if animation:
            pass
        self.clear()    # refresh the screen (that is, clear) so we can see changes

        # show title
        font_size = self._margin * 0.9
        surf, rect = self.create_text(font_name=Constants.FONT_NAME_1, font_size=int(font_size), text=self._caption,
                                      fg=Constants.BLACK, bg=Constants.BGCOLOR)
        rect.midtop = (self._width // 2, (self._margin - font_size) // 2)
        self.DISPLAYSURF.blit(surf, rect)

        # show grid names
        font_size = self._margin * 0.25
        for x, y, name, color in (
                (player.his_grid.x + player.his_grid.width / 2, player.his_grid.y - 5, "You", Constants.BLUE),
                (player.opponent_grid.x + player.opponent_grid.width / 2, player.opponent_grid.y - 5, "Enemy", Constants.RED)
        ):
            surf, rect = self.create_text(font_name=Constants.FONT_NAME_1, font_size=int(font_size), text=name,
                                          fg=color, bg=Constants.BGCOLOR)
            rect.midbottom = (x, y)
            self.DISPLAYSURF.blit(surf, rect)

        # draw grids
        player.his_grid.draw(surface=self.DISPLAYSURF, color1=Constants.BLACK, color2=Constants.BLUE, color3=Constants.GREY)
        player.opponent_grid.draw(surface=self.DISPLAYSURF, color1=Constants.BLACK, color2=Constants.RED, color3=Constants.GREY)

        # draw table
        player.fleet_table.draw(surface=self.DISPLAYSURF)

        # show message
        font_size = self._margin * 0.2
        surf, rect = self.create_text(font_name=Constants.FONT_NAME_1, font_size=int(font_size), text=self._message,
                                      fg=Constants.GREY, bg=Constants.BGCOLOR)
        # rect.midbottom = (self._width // 2, self._height - (self._margin - font_size) // 2)
        rect.midbottom = (player.opponent_grid.area.midbottom[0], self._height - (self._margin - font_size) // 2)
        self.DISPLAYSURF.blit(surf, rect)

        # --- Changeable elements ---
        # redraw boats - the players' ones
        for boat_ in player.boats:  # this will update existing boats, and created newly ones
            boat_.draw(self.DISPLAYSURF)
        # redraw strikes - the opponents' grid
        for box_ in player.strikes:
            if box_.is_hit:  # hit
                box_.reveal(self.DISPLAYSURF)
            else:  # miss
                box_.miss(self.DISPLAYSURF)
        return

    def show_game_over_screen(self, win, animation=False):
        """
        Sets the game over screen as currently displayed screen.
        This happens when game is finished.
        :param win: bool
        :param animation: bool
        :return: None
        """
        if animation:
            pass

        if win:
            caption = "YOU WON!!!"
        else:
            caption = "YOU LOST!"
        self._show_caption_message_screen(caption=caption, message="Thank you for playing the game with me! :)")
        return

    def show_game_over_screen_alpha(self, win, animation=False):
        """
        Sets the game over cover on top of the game screen.
        This happens when game is finished.
        :param win: bool
        :param animation: bool
        :return: None
        """
        if animation:
            pass

        alpha_value = 128
        if win:
            caption = "YOU WON!!!"
            bgcolor = Constants.BLUE + (alpha_value, )
        else:
            caption = "YOU LOST!"
            bgcolor = Constants.RED + (alpha_value, )

        transparent_surface = pygame.Surface((self._width, self._height))
        transparent_surface = transparent_surface.convert_alpha()
        transparent_surface.fill(bgcolor)
        self.DISPLAYSURF.blit(transparent_surface, (0, 0))

        surf, rect = self.create_text(font_name=Constants.FONT_NAME_1, font_size=Constants.FONT_SIZE_2, text=caption,
                                      fg=Constants.BLACK)
        rect.center = self._width // 2, self._height // 2

        self.DISPLAYSURF.blit(surf, rect)
        return

    def _show_caption_message_screen(self, caption, message):
        """
        Private method, just for better organizing our code.
        We have few screens that contains some caption and
        appropriate message, so this method gets those
        parameters and creates named screen.
        :param caption: str
        :param message: str
        :return: None
        """
        caption_surf, caption_rect = Window.create_text(Constants.FONT_NAME_1, Constants.FONT_SIZE_1,
                                                        caption, Constants.BLACK, Constants.WHITE)
        caption_rect.midtop = (self._width / 2, self._height / 4)

        message_surf, message_rect = Window.create_text(Constants.FONT_NAME_1, Constants.FONT_SIZE_2,
                                                        message, Constants.BLACK, Constants.WHITE)
        message_rect.midbottom = (self._width / 2, self._height * 0.75)

        self.DISPLAYSURF.blit(caption_surf, caption_rect)
        self.DISPLAYSURF.blit(message_surf, message_rect)
        return

    @staticmethod
    def create_text(font_name, font_size, text, fg, bg=None):
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
        number_of_iterations = time * Constants.FPS
        for _ in range(number_of_iterations):
            func()
            self.update()
        return

    def update(self, clear=False):
        """
        Updates the window screen.
        Syntatic sugar.
        If clear, window is filled with background color
        to delete any drawing that was before on it.
        :return: None
        """
        if clear:
            self.clear()
        pygame.display.update()
        Constants.FPS_CLOCK.tick(Constants.FPS)
        return

    def clear(self):
        """
        Clears the display surface.
        :return: None
        """
        self.DISPLAYSURF.fill(Constants.BGCOLOR)
        return
