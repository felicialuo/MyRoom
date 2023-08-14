#################################################
# term project: MyRoom
# helperFn.py
# version 22.12.07

# name: Felicia Luo
# andrew id: zhixinlu
#################################################

import numpy as np

# CITATION: almostEqual revised from CMU 15-112 past hw templates
def almostEqual(d1, d2, epsilon=12): 
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

# CITATION: round_rectangle revised from:
# https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
def round_rectangle(canvas, x0, y0, x1, y1, r=10, fill=True, width=2):
    if fill: canvas.create_rectangle(x0, y0, x1, y1, fill='white', width=0)
    canvas.create_arc(x0, y0, x0+2*r, y0+2*r, start= 90, extent=90, style="arc", width=width)
    canvas.create_arc(x1-2*r, y1-2*r, x1, y1, start=270, extent=90, style="arc", width=width)
    canvas.create_arc(x1-2*r, y0, x1, y0+2*r, start=  0, extent=90, style="arc", width=width)
    canvas.create_arc(x0, y1-2*r, x0+2*r, y1, start=180, extent=90, style="arc", width=width)
    canvas.create_line(x0+r, y0, x1-r, y0, width=width)
    canvas.create_line(x0+r, y1, x1-r, y1, width=width)
    canvas.create_line(x0, y0+r, x0, y1-r, width=width)
    canvas.create_line(x1, y0+r, x1, y1-r, width=width)

def roundNearestInch(d, inchPixelRatio=3):
    return d // inchPixelRatio * inchPixelRatio

# CITATION: cos and sin fn from https://github.com/dungba88/cleaner_robot
def cos(direction):
    # naive implementation of cos
    # direction val: 0-Right, 1-Up, 2-Left, 3-Down
    # corres cos val:1,       0,    -1,     0
    return int(abs(2 - direction) - 1)

def sin(direction):
    # naive implementation of sin
    # direction val: 0-Right, 1-Up, 2-Left, 3-Down
    # corres sin val:0,       1,    0,     -1
    return int(1 - abs(direction - 1))