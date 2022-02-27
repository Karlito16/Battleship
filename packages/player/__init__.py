#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# package name: player

import pygame
from pygame.locals import *
from packages.server.clients.client import Client
from packages.player.shape import Shape
from packages.player.boat import Boat
from packages.public.constants import Constants


class Player(Client):

    def __init__(self, window, his_grid, opponent_grid, fleet_table, connection, username):
        """
        Constructor. Class extends Client class.
        :param window: <class Window>
        :param his_grid: <class Grid>
        :param opponent_grid: <class Grid>
        :param fleet_table: <class Table>
        :param connection: <class socket>
        :param username: str
        """
        super().__init__(connection=connection, username=username)
        self._window = window
        self._his_grid = his_grid
        self._opponent_grid = opponent_grid
        self._fleet_table = fleet_table

        self._boats = list()
        self._won = False
        self._strikes = list()  # contains all of the strikes that player did - important for updating the screen
        # IMPORTANT: boxes from this list are from the opponents' grid
        self._striking_box = None  # <class Box>, remembers the box that player strikes - striking box
        self._attack = False    # True when server sends command "-strike;", False when server sends command "-defend;"

    @property
    def won(self):
        """
        Getter.
        :return: bool
        """
        return self._won

    @won.setter
    def won(self, value):
        """
        Setter.
        :param value: bool
        :return: None
        """
        self._won = value
        return

    @property
    def attack(self):
        """
        Getter.
        :return: bool
        """
        return self._attack

    @attack.setter
    def attack(self, value):
        """
        Setter.
        :param value: bool
        :return: None
        """
        self._attack = value
        return

    @property
    def his_grid(self):
        """
        Getter.
        :return: <class Grid>
        """
        return self._his_grid

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

    @property
    def boats(self):
        """
        Getter.
        :return: list
        """
        return self._boats

    @property
    def strikes(self):
        """
        Getter.
        :return: list
        """
        return self._strikes

    def create_fleet(self):
        """
        While loop for creating a fleet.
        :return: None
        """
        boat_order = _get_all_boats_sizes()
        created_boats = 0
        boat_size = boat_order[created_boats]
        direction = Constants.DIR_RIGHT
        create_boat = False
        highlighted_box = None
        highlighted_shape = None
        self._window.message = "Use ARROWS to rotate the shape. Press ENTER to create a boat."
        while self.in_game and created_boats < len(boat_order):
            # refresh the screen (that is, clear) so we can see changes
            self._window.clear()
            self._window.show_game_screen(player=self)  # redraw

            # check server communication
            self.connection.commands.check()

            # handle the game events
            self.connection.check_for_quit()
            mousex, mousey, mouse_clicked = self.connection.check_mouse_events()
            movement = mousex != 0 and mousey != 0
            key_pressed = False
            for event in pygame.event.get(KEYDOWN):
                key_pressed = True
                if event.key == K_LEFT:
                    direction = Constants.DIR_LEFT
                elif event.key == K_RIGHT:
                    direction = Constants.DIR_RIGHT
                elif event.key == K_UP:
                    direction = Constants.DIR_UP
                elif event.key == K_DOWN:
                    direction = Constants.DIR_DOWN
                elif event.key == K_RETURN:
                    create_boat = True
                else:
                    key_pressed = False
                    pygame.event.post(event)

            # update the game stats
            covered_box, highlighted_box = _on_mouse_motion(movement=movement, mousex=mousex, mousey=mousey,
                                                            highlighted_box=highlighted_box, grid_=self._his_grid)
            # highlight the box
            if highlighted_box:
                highlighted_box.highlight(self._window.DISPLAYSURF, Constants.BLUE)

                # create shape
            if mouse_clicked and covered_box and (highlighted_shape is None or covered_box != highlighted_shape.head):
                # player can click on the same box, then we don't need to draw new shape
                highlighted_shape = Shape(grid=self.connection.player_grid, head=covered_box,
                                          size=boat_size, direction=direction)
                # highlight the shape
            if highlighted_shape and key_pressed and not create_boat:  # player changed the orientation of the shape
                highlighted_shape.change_orientation(direction=direction)
            if highlighted_shape:
                color = {True: Constants.BLUE, False: Constants.RED}[highlighted_shape.is_valid]
                highlighted_shape.highlight(self._window.DISPLAYSURF, color)

                # create a boat
            if create_boat:     # player can press ENTER without marking the shape
                if highlighted_shape and highlighted_shape.is_valid:
                    new_boat = Boat(shape=highlighted_shape)
                    self._boats.append(new_boat)
                    created_boats += 1
                    if created_boats < len(boat_order):
                        boat_size = boat_order[created_boats]
                    highlighted_shape = None
                create_boat = False
                # show boats
            for boat_ in self._boats:  # this will update existing boats, and created newly ones
                boat_.draw(self._window.DISPLAYSURF)

                # highlight the row in the fleet table
            self._fleet_table.highlight_row(surface=self._window.DISPLAYSURF,
                                            index=Constants.BOAT_SIZES.index(boat_size) + 2,
                                            color=Constants.GREEN)

            # update the screen
            self._window.update()

        if self.in_game:
            # inform server that player is ready for the start of the game
            self.connection.commands.ready("fleet")
            self._window.message = "Waiting for other player to complete his fleet..."
        return None

    def strike(self):
        """
        While loop for attack.
        Loop ends when player picks the box
        which he want's to attack.
        :return: None
        """
        highlighted_box = None
        self._window.message = "ATTACK!!!"
        while self.connected and self.in_game:
            # refresh the screen (that is, clear) so we can see changes
            self._window.clear()
            self._window.show_game_screen(player=self)  # redraw

            # check server communication
            self.connection.commands.check()

            # handle the game events
            self.connection.check_for_quit()
            mousex, mousey, mouse_clicked = self.connection.check_mouse_events()
            movement = mousex != 0 and mousey != 0

            # update the game stat
            covered_box, highlighted_box = _on_mouse_motion(movement=movement, mousex=mousex, mousey=mousey,
                                                            highlighted_box=highlighted_box, grid_=self._opponent_grid)
            # highlight the box
            if highlighted_box and highlighted_box not in self._strikes:
                highlighted_box.highlight(surface=self._window.DISPLAYSURF, color=Constants.RED)

            # if mouse_clicked and highlighted_box is not None and not highlighted_box.is_hit:
            if mouse_clicked and highlighted_box is not None and highlighted_box not in self._strikes:
                # attack
                self.connection.commands.strike(highlighted_box.x, highlighted_box.y, send=True)
                self._striking_box = highlighted_box
                self._strikes.append(self._striking_box)
                # self._striking_box.hit = True   # this will be done in 'mark_box_type' method
                # can be a miss too, but this ensures that player cannot strike at the same box more than once
                break

            # update the screen
            self._window.update()
        self._attack = False    # player is done with attacking
        return

    def check_strike(self, x, y):  # defender
        """
        Player checks if attacker has hit
        any of his boats.
        Parameters x and y are coords
        of pixel.
        Returns -1 for False, or
        Boat Type for True.
        :param x: int
        :param y: int
        :return: int
        """
        # translate the box from opponents' grid to the players' one
        box_ = self._opponent_grid.get_box_at_pixel(x, y)  # box object from the opponents' grid
        i, j = self._opponent_grid.get_index_of(box=box_)  # i and j values are same for both of the grids
        if i is not None and j is not None:
            box_ = self._his_grid[i][j]  # box object from the players' grid
        else:
            raise ValueError("Invalid strike coordinates!")
        # check box type
        if box_.type != Constants.EMPTY:  # hit!
            box_.color = Constants.BLACK
            box_.hit(self._window.DISPLAYSURF)
        return box_.type

    def mark_box_type(self, type_):  # attacker
        """
        Player marks type of the striking box.
        :param type_: int
        :return: None
        """
        self._striking_box.type = type_
        # update the visual part
        from packages.public.logger import Logger
        Logger.print(message=f"Checking box type...{type_}", type_=Logger.INFO)
        if type_ == Constants.EMPTY:  # miss
            # it's not a hit really, but for attacker, this will be his miss ("X") - marks the miss on the opponent_grid
            self._striking_box.miss(self._window.DISPLAYSURF)
        else:
            # hit!
            self._striking_box.color = Constants.BOAT_COLORS[type_]
            self._striking_box.reveal(surface=self._window.DISPLAYSURF)
        return

    def defend(self):
        """
        While loop for defend.
        :return: None
        """
        self._window.message = "DEFEND!!!"
        return

    def is_defeated(self):
        """
        Method checks if player is defeated.
        :return: bool
        """
        for boat_ in self._boats:
            for box_ in boat_.shape:
                if not box_.is_hit:
                    return False
        return True


def _get_all_boats_sizes():
    """
    Function returns a list dimension of total number of boats that needs to be created.
    Each element is size of that boat.
    :return: list
    """
    list_ = []
    for i in range(len(Constants.BOAT_NAMES)):
        list_ += [Constants.BOAT_SIZES[i]] * Constants.BOAT_QUANTITY[i]
    return list_


def _on_mouse_motion(movement, mousex, mousey, highlighted_box, grid_):
    """
    Function handles the mouse motion event.
    Updates the game stats.
    Returns currently covered box as well as
    the box that should be highlighted.
    :param movement: bool
    :param mousex: int
    :param mousey: int
    :param highlighted_box: <class Box>
    :param grid_: <class Grid>
    :return: tuple :: (<class Box>, <class Box>)
    """
    if movement:  # if mouse has been moved
        covered_box = grid_.get_box_at_pixel(mousex, mousey)
        if covered_box and covered_box != highlighted_box and covered_box.type == Constants.EMPTY:
            # in order to highlight the box, it needs to be empty and not already highlighted
            highlighted_box = covered_box
        elif covered_box is None and not grid_.area.collidepoint(mousex, mousey):
            highlighted_box = None
    else:  # no mouse motion
        covered_box = highlighted_box
    return covered_box, highlighted_box
