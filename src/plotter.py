# -*- coding: utf8 -*-

import argparse
import sys

from FctMgr import *
from PPMMgr import *

## Init parser:
parser  = argparse.ArgumentParser(description='This is a plotter program.')

parser.add_argument('-o', type=str, action = "store", 
                    default="out.ppm", dest="filename",
                    help='filename. Default : out.ppm')

parser.add_argument('-s', type=float, action = "store", 
                    default=0.1, dest="step",
                    help='step, default value: 0.1')

parser.add_argument('--xrange', type=float, action = "store", 
                    default=10.0, dest="range_x",
                    help='range X, default value: 10')

parser.add_argument('--yrange', type=float, action = "store", 
                    default=10.0, dest="range_y",
                    help='range Y, default value: 10')
                    
parser.add_argument('--xcenter', type=float, action = "store", 
                    default=0.0, dest="center_x",
                    help='center X, default value: 0')

parser.add_argument('--ycenter', type=float, action = "store", 
                    default=0.0, dest="center_y",
                    help='center Y, default value: 0')

parser.add_argument('functions', metavar='f', type=str, nargs='+',
                   help='functions')

## read all the arguments of the function call:
args = parser.parse_args()

try:

    range_x = args.range_x
    range_y = args.range_y
    center_x = args.center_x
    center_y = args.center_y
    step = args.step
    functions = args.functions

    ## call the function that does all the work on the matrix M: creation, drawing the axes, drawing the function 
    M = plot(center_x, center_y, range_x, range_y, step, functions)

    ## save the result in the 'filename' file
    matrixToFile(M, args.filename)

except:
    print 'Error: please enter correct values for the arguments'.
