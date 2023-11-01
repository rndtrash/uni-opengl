#!/usr/bin/env python3

import pyglet
from pyglet import gl
import math
import random
import colorsys

# Direct OpenGL commands to this window.
w = 800
h = 600
window = pyglet.window.Window(width=w, height=h)

gl.glClearColor(0, 0, 0, 1) # чёрный цвет
gl.glClear(gl.GL_COLOR_BUFFER_BIT)
gl.glEnable(gl.GL_LINE_SMOOTH)

#gl.glEnable(gl.GL_DEPTH_TEST)
#gl.glEnable(gl.GL_CULL_FACE)

def makeSnowflakeBranch(x, y, radius, branches, max_depth, angle, radius_range, current_depth):
    this_pos = (math.cos(angle) * radius * 0.5 + x, math.sin(angle) * radius * 0.5 + y)
    points = [this_pos]

    if current_depth != max_depth and branches > 1:
        for i in range(branches):
            new_angle = angle + (i * radius_range / (branches - 1)) - radius_range / 2
            points.append(this_pos)
            points.extend(makeSnowflakeBranch(this_pos[0], this_pos[1], radius * 0.4, branches // 2, max_depth, new_angle, radius_range * 2, current_depth + 1))

    return points

def makeSnowflake(radius, branches, depth):
    lines = []

    angle_mult = math.radians(360 / branches)
    for i in range(branches):
        angle = i * angle_mult
        lines.append((0, 0))
        lines.extend(makeSnowflakeBranch(0, 0, radius, branches // 2, depth, angle, angle_mult, 0))
    
    return lines

def rgb(*args):
    return [i / 255 for i in args]


snowflake = makeSnowflake(0.5, 6, 2)

@window.event
def on_draw():
    window.clear()

    gl.glMatrixMode(gl.GL_PROJECTION) # Теперь текущей является матрица проецирования
    gl.glLoadIdentity() # Инициализация матрицы проецирования
    gl.glOrtho(-w / h, w / h, -1, 1, -1, 1) # Ортографическое проецирование

    gl.glColor3f(*rgb(21, 178, 235))
    gl.glLineWidth(2)
    gl.glBegin(gl.GL_LINES)
    for l in snowflake:
        gl.glVertex2f(*l)
    gl.glEnd()

def update(dt):
    pass

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60) # schedule 60 times per second
    pyglet.app.run()
