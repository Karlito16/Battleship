#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: box

import pygame
from packages.public.constants import Constants
from packages.player.area import Area
from packages.player.window import Window


class Box(Area):

    def __init__(self, rect):
        """
        Constructor.
        Rect (that is, rectangle) is object that defines space (position)
        on screen for our box.
        Difference between total size and size is that total size
        includes both left and right box margins.
        :param rect: <class Rect>
        """
        super().__init__(area=rect)

        self._hit = False   # True if boat has been hit on that place
        self._type = Constants.EMPTY     # boat type, -1 for empty box ("sea")
        self._color = None  # color of the box

    @property
    def size(self):
        """
        Property.
        Returns the box size, without
        both left and right margins.
        :return: int
        """
        return self.width - 2 * Constants.BOX_MARGIN

    @property
    def is_hit(self):
        """
        Getter.
        :return: bool
        """
        return self._hit

    @property
    def type(self):
        """
        Getter.
        :return: int
        """
        return self._type

    @type.setter
    def type(self, value):
        """
        Setter.
        :return: None
        """
        self._type = value
        return

    @property
    def color(self):
        """
        Getter.
        :return: tuple
        """
        return self._color

    @color.setter
    def color(self, value):
        """
        Setter.
        :param value: tuple
        :return: None
        """
        self._color = value
        return

    def fill(self, surface):
        """
        Fills the box with given color.
        :param surface: <class Surface>
        :return: None
        """
        pygame.draw.rect(surface, self._color, (self.x + Constants.BOX_MARGIN, self.y + Constants.BOX_MARGIN, self.size, self.size))
        return

    def highlight(self, surface, color):
        """
        Highlights the box with given color.
        :param surface: <class Surface>
        :param color: str
        :return: None
        """
        pygame.draw.rect(surface, color, self.area, Constants.BOX_MARGIN)
        return

    def hit(self, surface):
        """
        Hits the box.
        This happens when opponent hits
        the box.
        :param surface: <class Surface>
        :return: None
        """
        self.fill(surface)
        font_size = int(self.size * 0.8)
        surf, rect = Window.create_text(font_name=Constants.FONT_NAME_1, font_size=font_size, text="X",
                                        fg=Constants.WHITE, bg=Constants.BLACK)
        rect.center = self.area.center
        surface.blit(surf, rect)
        self._hit = True
        return

    def reveal(self, surface):
        """
        Reveals the opponent's box.
        :param surface: <class Surface>
        :return: None
        """
        self._hit = True
        self.fill(surface=surface)

    def miss(self, surface):
        """
        This happens when attacker misses
        any of the opponents' boats.
        :param surface: <class Surface>
        :return: None
        """
        surf, rect = Window.create_text(font_name=Constants.FONT_NAME_1, font_size=Constants.FONT_SIZE_4, text="X",
                                        fg=Constants.BLACK, bg=Constants.BGCOLOR)
        rect.center = self.area.center
        surface.blit(surf, rect)
        return
