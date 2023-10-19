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
gl.glEnable(gl.GL_POINT_SMOOTH)

#gl.glEnable(gl.GL_DEPTH_TEST)
#gl.glEnable(gl.GL_CULL_FACE)

sin_x = 0

@window.event
def on_draw():
    global sin_x

    window.clear()

    gl.glMatrixMode(gl.GL_PROJECTION) # Теперь текущей является матрица проецирования
    gl.glLoadIdentity() # Инициализация матрицы проецирования
    gl.glOrtho(0, w, 0, h, -1, 1) # Ортографическое проецирование

    points = 1000
    step = w / points
    for i in range(0, 10):
        gl.glColor3f(*colorsys.hsv_to_rgb(1 / 10 * i, 1, 1))
        gl.glBegin(gl.GL_LINE_STRIP)
        for point in range(points + 1):
            x = step * point
            g_h = h / 20
            y_base = h / 10 * i + g_h
            y = y_base - math.sin(x / (i + 1) + sin_x) * g_h
            gl.glVertex2f(x, y)
        gl.glEnd()

def update(dt):
    global sin_x
    sin_x += 10 * dt

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60) # schedule 60 times per second
    pyglet.app.run()
