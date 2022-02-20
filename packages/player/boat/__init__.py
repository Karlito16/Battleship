#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: boat

from packages.player.shape import Shape


class Boat(Shape):
    NAMES = ["Aircraft Carrier", "Battleship", "Cruiser", "Destroyer", "Submarine"]
    QUANTITY = [1, 1, 1, 2, 2]
    SIZES = [5, 4, 3, 2, 1]
    assert len(NAMES) == len(QUANTITY) == len(SIZES), "Invalid data for boat names, their quantity and size values!"

    def __init__(self):
        super().__init__()
