"""
Simple Geometrical Drawer - Простая рисовалка
геометрических фигур с консольно-графическим интерфейсом.
"""

import os
import sys
from math import sqrt
from abc import ABCMeta, abstractmethod

from thirdparty.graph import *


POINT_SIZE = 2
WINDOW_SIZE = (800, 600)
CANVAS_SIZE = (800, 600)


def clear_screen():
    if 'win32' in sys.platform:
        os.system('cls')
    else:
        os.system('clear')


def draw_point(x, y):
    prev_pen_color = penColor()
    prev_brush_color = brushColor()
    penColor('black')
    brushColor('black')
    circle(x, y, POINT_SIZE)
    penColor(prev_pen_color)
    brushColor(prev_brush_color)


class DrawingMode(metaclass=ABCMeta):

    def select(self):
        onMouseClick(self.lclick_handler, 1)
        onMouseClick(self.rclick_handler, 3)

    @abstractmethod
    def lclick_handler(self, ev):
        pass

    @abstractmethod
    def rclick_handler(self, ev):
        pass


class PolygonMode(DrawingMode):

    def __init__(self):
        self.coordstack = []

    def lclick_handler(self, ev):
        draw_point(ev.x, ev.y)
        self.coordstack.append((ev.x, ev.y))

    def rclick_handler(self, ev):
        if len(self.coordstack) == 0:
            return
        self.coordstack.append(self.coordstack[0])
        polygon(self.coordstack)
        self.coordstack.clear()


class CircleMode(DrawingMode):

    def __init__(self):
        self.center = None

    def lclick_handler(self, ev):
        if self.center is None:
            draw_point(ev.x, ev.y)
            self.center = (ev.x, ev.y)
        else:
            radius = int(sqrt((ev.x - self.center[0]) ** 2 + (ev.y - self.center[1]) ** 2))
            circle(self.center[0], self.center[1], radius)
            self.center = None

    def rclick_handler(self, ev):
        pass


_drawing_modes = {'polygon': PolygonMode(), 'circle': CircleMode()}


def select_pen_color():
    color = input('pen color?> ').strip()
    if color:
        penColor(color)


def select_brush_color():
    color = input('brush color?> ').strip()
    if color:
        brushColor(color)


def select_geom_object():
    geom_object = input('geometric object?> ').strip()
    if geom_object in _drawing_modes:
        _drawing_modes[geom_object].select()


def get_command(unused_ev):
    clear_screen()
    command = input('simple_drawer_console(> ').strip()
    if command == 'bc':
        select_brush_color()
    elif command == 'pc':
        select_pen_color()
    elif command == 'gb':
        select_geom_object()
    elif command == '':
        pass
    else:
        print('simple_drawer_error: unrecognizable command')


if __name__ == '__main__':
    penColor('black')
    windowSize(*WINDOW_SIZE)
    canvasSize(*CANVAS_SIZE)

    _drawing_modes['polygon'].select()

    onKey('c', get_command)

    run()
