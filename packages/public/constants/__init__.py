#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: constants

import pygame


class Constants:
    # Commands
    CMD_GAME = "-game"
    CMD_READY = "-ready"
    CMD_STRIKE = "-strike"
    CMD_LEFT = "-left"
    CMD_STAY = "-stay"
    CMD_DEFEND = "-defend"
    COMMAND_TIME_OFFSET = 1e-3
    USERNAME_WAITING_TIME = 10  # seconds

    # Game
    GAME_LOOP_TIME_OFFSET = 1e-9

    # Battleship
    # SERVER_HOSTNAME = "Karlito"
    # SERVER_HOSTNAME = "192.168.1.14"
    SERVER_HOSTNAME = "192.168.5.120"

    # Window
    GAME_CAPTION = "Battleship"
    WIN_WIDTH = 1080  # px
    WIN_HEIGHT = 720  # px
    WIN_MARGIN = 70  # px
    GRID_SIZE = 10
    GRID_BORDER_WIDTH = 4  # px
    GRID_HIGHLIGHT_BORDER_WIDTH = 1  # px
    TABLE_MARGIN = 10  # px
    TABLE_ROW_MARGIN = 4  # px
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    ORANGE = (255, 165, 0)
    PINK = (255, 192, 203)
    BGCOLOR = WHITE
    FONT_NAME_1 = "freesansbold.ttf"
    FONT_SIZE_1 = 72
    FONT_SIZE_2 = 36
    FONT_SIZE_3 = 24
    FONT_SIZE_4 = 18
    FPS = 30
    FPS_CLOCK = pygame.time.Clock()
    WELCOME_SCREEN_SLEEP_TIME = 2  # seconds
    CONNECTION_FAILED_SLEEP_TIME = 2  # seconds

    # Grid
    SEPARATOR_WIDTH = 2  # px

    # Boat
    BOAT_NAMES = ["Aircraft Carrier", "Battleship", "Cruiser", "Destroyer", "Submarine"]
    BOAT_QUANTITY = [1, 1, 1, 2, 2]
    # BOAT_QUANTITY = [0, 0, 0, 0, 1]  # temp, for testing
    BOAT_SIZES = [5, 4, 3, 2, 1]
    BOAT_COLORS = [RED, BLUE, GREEN, YELLOW, ORANGE]
    assert len(BOAT_NAMES) == len(BOAT_QUANTITY) == len(BOAT_SIZES) == len(BOAT_COLORS), \
        "Invalid data for boat names, their quantity, size and color values!"

    # Box
    BOX_MARGIN = 2  # px
    # box type
    EMPTY = -1
    MISSED = -2
    HIT = -3

