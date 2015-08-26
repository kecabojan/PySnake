"""
Defines snake class
"""
__author__ = 'Bojan Keca'

import sys
sys.path.append(r'c:\pydev')

import pygame as pg
from constants import *


class Snake(object):
    """ Represents snake which eats mice and crawls through maze
    """

    def __init__(self, screen, width):
        """
        :return: Initializer
        """
        self.direction = DIR_RIGHT                      # keep snake's current direction
        self.screen = screen
        self._width = width
        self.boundary = screen.get_width() / width      # maximum grid position in both X and Y directions

        ''' grid_occupied represent list of coordinates of the grid occupied by snake. When snake eats a mouse,
            grid_occupied list grows by one represented by tuple(x,y).
            x,y are in range of 0 to (screen_size / snake_width). Head of snake is last element of the list
        '''
        self.grid_occupied = [(x, 5) for x in range(0, 3)]     # occupy 5 squares initially
        self._prev_tail = ()    # we will always remember previous tail position so we can repaint it in black
        self._last_move_timestamp = 0                   # used in moving the snake
        self._grow = False                              # Should Snake grow for one or not on next move
        self._no_walls = False

    def head(self):
        """
        Returns grid position of the snake's head
        :return: grid position tuple
        """
        return self.grid_occupied[-1]

    def draw(self, draw_everything=False):
        """
        Draws all occupied grid elements of snake in green, and head of snake in blue.

        """
        g = self.grid_occupied
        if draw_everything:
            length = len(g)
            for i in xrange(length-1):
                self._fill_grid_at(g[i], GREEN)
        else:
            self._fill_grid_at(g[-2], GREEN)    # repaint the previous head to green
            self._fill_grid_at(self._prev_tail, BLACK)  # repaint previous tail to black

        # draw head in BLUE
        self._fill_grid_at(g[-1], BLUE)

    def grow(self):
        self._grow = True

    def move(self, direction=None):
        """
        Moved the snake in given direction
        :param direction: direction to move
        :return: True if move is valid, False if head hit the wall
        """

        # first check if direction is valid
        # if snakes is already moving to the right, then snake cannot turn left immediately,
        # it can go only to up, down or continue moving to the right

        if self.direction != -direction:    # allowed moves
            self.direction = direction

        # current_time = pg.time.get_ticks()
        # if current_time < self._last_move_timestamp + 50:  # check if it time to move the snake
        #     return True
        #
        # self._last_move_timestamp = current_time

        head = self.head()
        if self._no_walls:
            if self.direction == DIR_LEFT:
                # calculate new position of the head using modulus arithmetic
                temp_pos = ((head[0]-1) % self.boundary, head[1])
                if temp_pos in self.grid_occupied:                  # snake hit itself, end game
                    return False
                self.grid_occupied.append(temp_pos)                 # new head becomes left grid position to current
            elif self.direction == DIR_RIGHT:
                # calculate new position of the head using modulus arithmetic
                temp_pos = ((head[0]+1) % self.boundary, head[1])
                if temp_pos in self.grid_occupied:                  # snake hit itself, end game
                    return False
                self.grid_occupied.append(temp_pos)                 # new head becomes left grid position to current
            elif self.direction == DIR_UP:
                # calculate new position of the head using modulus arithmetic
                temp_pos = (head[0], (head[1]-1) % self.boundary)
                if temp_pos in self.grid_occupied:                  # snake hit itself, end game
                    return False
                self.grid_occupied.append(temp_pos)                 # new head becomes left grid position to current
            elif self.direction == DIR_DOWN:
                # calculate new position of the head using modulus arithmetic
                temp_pos = (head[0], (head[1]+1) % self.boundary)
                if temp_pos in self.grid_occupied:                  # snake hit itself, end game
                    return False
                self.grid_occupied.append(temp_pos)                 # new head becomes left grid position to current
        else:
            if self.direction == DIR_LEFT:
                if head[0] == 0:                # check if head hit the left wall
                    return False

                self.grid_occupied.append((head[0]-1, head[1]))     # new head becomes left grid position to current
            elif self.direction == DIR_RIGHT:
                if head[0] == self.boundary-1:    # check if head hit the right wall
                    return False

                self.grid_occupied.append((head[0]+1, head[1]))     # new head becomes right grid position to current
            elif self.direction == DIR_UP:
                if head[1] == 0:                # check if head hit the up wall
                    return False

                self.grid_occupied.append((head[0], head[1]-1))     # new head becomes up grid position to current
            elif self.direction == DIR_DOWN:
                if head[1] == self.boundary-1:    # check if head hit the down wall
                    return False

                self.grid_occupied.append((head[0], head[1]+1))     # new head becomes down grid position to current

        if not self._grow:
            self._prev_tail = self.grid_occupied.pop(0)         # remove snake's tail (first element in list)

        self._grow = False   # always reset grow flag - it is set from outside only when snake eats a mouse

        return True

    def _fill_grid_at(self, (x, y), color):
        """
        Draws and fills rectangle in grid position x,y
        :param color: color to fill the rectangle
        """

        pg.draw.rect(self.screen, color, [x * self._width, y * self._width, self._width, self._width], 0)







