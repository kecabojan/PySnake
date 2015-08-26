"""
Main module of the game
"""
__author__ = 'Bojan Keca'

import sys
import timeit
from random import randint
from snake import Snake
from constants import *

sys.path.append(r'c:\pydev')

import pygame as pg


def secure_screen_size():
    """
    Ensures that screen size to snake width ratio is correct,
    increments the screen size until ratio is good
    """
    global SCREEN_SIZE

    while SCREEN_SIZE % SCREEN_WIDTH_TO_SNAKE_WIDTH != 0:
        SCREEN_SIZE += 1


class SnakeGame(object):
    """
    Represents game object, handles snake's movement and drawing,
    mice creating, score count, draws everything.
    """

    def __init__(self):
        secure_screen_size()
        pg.init()               # initialize pygame module

        self._screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pg.display.set_caption('PySnake Game')

        # set of all grid fields: range for x and y go from 0 to SCREEN_WIDTH_TO_SNAKE_WIDTH - 1
        # it will be used to pick a place for draw mouse for snake to chase
        self._grid_field_list = [(x, y) for x in xrange(SCREEN_WIDTH_TO_SNAKE_WIDTH) for y in xrange(SCREEN_WIDTH_TO_SNAKE_WIDTH)]
        self._grid_field_size = self._screen.get_width() / SCREEN_WIDTH_TO_SNAKE_WIDTH   # in pixels

        # create snake
        self._snake = Snake(self._screen, self._screen.get_width() / SCREEN_WIDTH_TO_SNAKE_WIDTH)

        # Clock object is used to slow down and main loop, it ensures the FPS
        self._clock = pg.time.Clock()

        # default speed of the game
        self._speed = 10
        # default speed increment when snake catches mouse
        self._speed_inc = 3
        # increment score when snake catches mouse
        self._score = 0

    def run(self):
        # draw the white background onto the surface
        self._screen.fill(BLACK)

        self._snake.draw(draw_everything=True)
        mouse_pos = self._draw_mouse()
        pg.display.update()

        running = True
        direction = DIR_RIGHT   # initial movement direction
        while self._snake.move(direction) and running:
            self._snake.draw()
            pg.display.flip()

            # check if snake's head is on the mouse field
            if self._snake.head() == mouse_pos:
                self._score += 1
                self._snake.grow()
                self._delete_mouse(mouse_pos)   # snake eats mouse -> remove it from field
                mouse_pos = self._draw_mouse()  # re-draw mouse again
                self._speed += self._speed_inc  # increase play speed

            self._clock.tick(self._speed)   # ensure frame rate of the game -> higher the FPS, snake will be faster

            for event in pg.event.get():
                if event.type is pg.QUIT:
                    running = False
                elif event.type is pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_LEFT:
                        direction = DIR_LEFT
                    elif event.key == pg.K_RIGHT:
                        direction = DIR_RIGHT
                    elif event.key == pg.K_UP:
                        direction = DIR_UP
                    elif event.key == pg.K_DOWN:
                        direction = DIR_DOWN

    def _draw_mouse(self):
        """
        Picks random location and draws mouse
        :return: mouse location -> tuple (x,y)
        """

        pos = self._snake.grid_occupied[0]
        while pos in self._snake.grid_occupied:
            pos = (randint(0, SCREEN_WIDTH_TO_SNAKE_WIDTH-1), randint(0, SCREEN_WIDTH_TO_SNAKE_WIDTH-1))

        # draw a pink circle onto the surface
        center = (pos[0] * self._grid_field_size + self._grid_field_size / 2,
                  pos[1] * self._grid_field_size + self._grid_field_size / 2)
        pg.draw.circle(self._screen, PINK, center, self._grid_field_size / 2, 0)

        return pos

    def _delete_mouse(self, pos):
        """
        Removes mouse from given position
        """
        center = (pos[0] * self._grid_field_size + self._grid_field_size / 2,
                  pos[1] * self._grid_field_size + self._grid_field_size / 2)
        pg.draw.circle(self._screen, BLACK, center, self._grid_field_size / 2, 0)


def main():
    SnakeGame().run()

if __name__ == "__main__":
    main()