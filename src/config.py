# -*- coding: utf8 -*-

from symbols import *

# board:
WIDTH = 800
HEIGHT = 600

# colors:
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 127, 0)
BLUE = (0, 0, 255)
BLUE_SKY = (90, 155, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
TURQUOISE = (0, 255, 255)
ORANGE = (255, 127, 0)
VIOLET = (170, 20, 170)

BG = WHITE
AXIS_COLOR = GREY

PLOTCOLORS = [
    TURQUOISE,
    RED,
    GREEN,
    BLUE,
    PINK,
    YELLOW,
    ORANGE,
    DARK_GREEN,
    VIOLET,
    BLUE_SKY,
]
COLORS_NBR = len(PLOTCOLORS)

AREA_COLOR = YELLOW

# axes:
TIC_SIZE = 4
ARROW_HEIGHT = 20
ARROW_WIDTH = 10

# labels:
OFFSET_LABEL = 5
OFFSET_LABEL_AXE = 15

# We can assume that all symbols have the same size.
SYMBOL_HEIGHT = len(symbols["0"])
SYMBOL_WIDTH = len(symbols["0"][0])

# area calculation
E = 2
epsilon = 10
