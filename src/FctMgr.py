# -*- coding: utf8 -*-

from math import *

from config import *


def plot(center_x, center_y, range_x, range_y, step, functions):
    """This function creates a matrix and draws the functions passed in parameter."""
    range_x = float(range_x) / 2
    range_y = float(range_y) / 2

    # create the matrix with dimensions HEIGHT and WIDTH
    M = [[BG for y_i in range(HEIGHT)] for x_i in range(WIDTH)]

    # draw the axes
    drawAxes(M, center_x, center_y, range_x, range_y, AXIS_COLOR)

    # draw the functions passed in parameter
    for i in range(len(functions)):
        drawFunction(
            M,
            center_x,
            center_y,
            range_x,
            range_y,
            functions[i],
            step,
            PLOTCOLORS[i % COLORS_NBR],
        )
    return M


def xTox_i(x, center_x, range_x):
    """This function transforms the x coordinate into column number of the matrix.

    Input: x coordinate to transform,
           x-coordinate of the center of the image,
           width of the image in px.
    Output: coordinate (column number) of the pixel in the matrix
    """
    return int((x + range_x - center_x) * WIDTH / (2 * range_x))


def x_iTox(x_i, center_x, range_x):
    """This function transforms the column number of the matrix into x coordinate."""
    return x_i * (2 * range_x) / WIDTH - range_x + center_x


def yToy_i(y, center_y, range_y):
    """This function transforms the y coordinate into number of the row in the matrix.

    Input: Y coordinate to transform,
           Y coordinate of the center of the image,
           Height of the image in px.
    Output: coordinate (row number) of the pixel in the matrix
    """
    return HEIGHT - int((y + range_y - center_y) * HEIGHT / (2 * range_y))


def y_iToy(y_i, center_y, range_y):
    """This function transforms the row number of the matrix into the y coordinate."""
    return (HEIGHT - y_i) * (2 * range_y) / HEIGHT - range_y + center_y


def drawSymbol(M, xIndex, yIndex, symbol):
    """This function draws a symbol in the matrix.

    Input: The matrix (image),
           The coordinates of the upper left corner of the symbol,
           The symbol to draw.
    """
    for i in range(len(symbol)):
        for j in range(len(symbol[i])):
            if (
                symbol[i][j] != BG[0]
                and xIndex + j < WIDTH
                and yIndex + i < HEIGHT
            ):
                M[xIndex + j][yIndex + i] = (
                    symbol[i][j],
                    symbol[i][j],
                    symbol[i][j],
                )


def drawNumber(M, xIndex, yIndex, number):
    """This function draws a number in the matrix (image)."""
    #'number' is a string!
    for digit in number:
        drawSymbol(M, xIndex, yIndex, symbols[digit])
        xIndex += SYMBOL_WIDTH


def drawAxes(M, center_x, center_y, range_x, range_y, color):
    """This function draws the axes with the ticks and labels."""
    # ----X axis----
    # calculate the line number (0 on Y) = c
    # if c<0 => 0
    # if c> HEIGHT-1 => HEIGHT-1
    coord_y = min(HEIGHT - 1, max(0, yToy_i(0, center_y, range_y)))

    # adjust the position of the labels (above the axis / below the axis)
    coord_label_x = -1
    if coord_y > 2 * SYMBOL_HEIGHT:
        coord_label_x = coord_y - OFFSET_LABEL - SYMBOL_HEIGHT
    else:
        coord_label_x = coord_y + OFFSET_LABEL

    # the axis:
    drawLine(M, 0, coord_y, WIDTH - 1, coord_y, color)

    # arrow:
    drawLine(
        M,
        WIDTH - ARROW_HEIGHT,
        coord_y + ARROW_WIDTH,
        WIDTH - 1,
        coord_y,
        color,
    )
    drawLine(
        M,
        WIDTH - ARROW_HEIGHT,
        coord_y - ARROW_WIDTH,
        WIDTH - 1,
        coord_y,
        color,
    )
    # label 'X':
    drawSymbol(
        M,
        WIDTH - 2 * OFFSET_LABEL_AXE - SYMBOL_WIDTH,
        coord_label_x,
        symbols["x"],
    )

    # tics and labels:
    for x in range(-1 * int(range_x) + int(center_x), int(range_x + center_x)):
        x_i = xTox_i(x, center_x, range_x)
        drawLine(
            M, x_i, coord_y - TIC_SIZE, x_i, coord_y + TIC_SIZE, color
        )  # tic
        drawNumber(M, x_i, coord_label_x, str(x))  # label

    # ----Y axis----
    # calculate column number (0 on X) = c
    # if c<0 => 0
    # if c> WIDTH-1 => WIDTH-1
    coord_x = max(0, min(WIDTH - 1, xTox_i(0, center_x, range_x)))

    # adjust the position of the labels (right of the axis / left of the axis)
    coord_label_y = -1
    if coord_x < WIDTH - 2 * SYMBOL_WIDTH:
        coord_label_y = coord_x + OFFSET_LABEL
    else:
        coord_label_y = coord_x - OFFSET_LABEL - SYMBOL_WIDTH
    # axis:
    drawLine(M, coord_x, 0, coord_x, HEIGHT - 1, color)

    # arrow:
    drawLine(M, coord_x, 0, coord_x + ARROW_WIDTH, ARROW_HEIGHT, color)
    drawLine(M, coord_x, 0, coord_x - ARROW_WIDTH, ARROW_HEIGHT, color)

    # label 'Y':
    drawSymbol(
        M, coord_label_y, OFFSET_LABEL_AXE + SYMBOL_HEIGHT, symbols["y"]
    )

    # Tics:
    numberLength = len(str(-1 * int(range_y) + int(center_y))) * SYMBOL_WIDTH
    if (
        coord_label_y + numberLength > coord_x
        and coord_label_y + numberLength > WIDTH
    ):
        coord_label_y -= numberLength
    for y in range(-1 * int(range_y) + int(center_y), int(range_y + center_y)):
        y_i = yToy_i(y, center_y, range_y)
        drawLine(
            M, coord_x - TIC_SIZE, y_i, coord_x + TIC_SIZE, y_i, color
        )  # tic
        drawNumber(M, coord_label_y, y_i, str(y))  # label


def drawFunction(
    M, center_x, center_y, range_x, range_y, function, step, color
):
    """This function draws the function in the matrix."""
    x = -range_x + center_x
    x_old = y_old = None

    x_i = xTox_i(x, center_x, range_x)
    while x_i < WIDTH:
        try:
            y = eval(function)
            y_i = yToy_i(y, center_y, range_y)

            # draw a line between (x_old,y_old) and (x_i,y_i)
            if (
                x_old != None
                and not (y_i > HEIGHT and y_old < 0)
                and not (y_old > HEIGHT and y_i < 0)
            ):
                # If the two do not have an extremely large gap between them (avoids tracing the "assymptotes" of the functions)
                if (
                    (y_old <= HEIGHT and y_old >= 0)
                    or (y_old >= HEIGHT and y_i <= HEIGHT)
                    or (y_old <= 0 and y_i >= 0)
                ):
                    # Three possible cases:
                    # y_old is in the window, we connect the two points
                    # y_old is not in the window but y_i, yes, we connect the two points
                    # y_old is in the window but y_i, no, we connect the two points
                    # This condition allows to avoid to make additional useless calculations, since the points we ask to represent are not in the window
                    drawLine(M, x_old, y_old, x_i, y_i, color)
            x_old = x_i
            y_old = y_i
        except OverflowError:
            # If there is an error because the number is too large or too close to 0, you should still try to plot the function
            if y > 4.8e238:
                # To avoid an error in the yToy_i function, we reduce the already very large number
                y = 4.8e237
            y_i = yToy_i(y, center_y, range_y)
            if (
                x_old != None
                and not (y_i > HEIGHT and y_old < 0)
                and not (y_old > HEIGHT and y_i < 0)
            ):
                if (
                    (y_old < HEIGHT and y_old > 0)
                    or (y_old > HEIGHT and y_i < HEIGHT)
                    or (y_old < 0 and y_i > 0)
                ):
                    drawLine(M, x_old, y_old, x_i, y_i, color)
            x_old = x_i
            y_old = y_i
        except:
            # If there is a math error or divisedbyzero error, we continue the function without drawing points
            y = x_old = y_old = None
        x += step
        x_i = xTox_i(x, center_x, range_x)


def drawLine(M, x_0, y_0, x_1, y_1, color):
    """This function draws a straight line between two points."""
    if abs(y_1 - y_0) > abs(x_1 - x_0):
        # the slope is steep
        m = float(x_1 - x_0) / (y_1 - y_0)
        if y_0 > y_1:
            y_0, y_1 = y_1, y_0
            x_0, x_1 = x_1, x_0

        x_i = x_0
        for y_i in range(y_0, y_1):
            if 0 <= x_i < WIDTH and 0 <= y_i < HEIGHT:
                M[int(x_i)][y_i] = color
            x_i += m
    else:
        m = float(y_1 - y_0) / (x_1 - x_0)
        y_i = y_0
        for x_i in range(x_0, x_1):
            if 0 <= x_i < WIDTH and 0 <= y_i < HEIGHT:
                M[x_i][int(y_i)] = color
            y_i += m
