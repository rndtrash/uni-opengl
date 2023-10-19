#!/usr/bin/env python3

import pyglet
from pyglet import gl
import math
import random

# Direct OpenGL commands to this window.
w = 640
h = 480
window = pyglet.window.Window(width=w, height=h)

gl.glClearColor(0, 0, 0, 1) # чёрный цвет
gl.glClear(gl.GL_COLOR_BUFFER_BIT)
gl.glEnable(gl.GL_POINT_SMOOTH)

#gl.glEnable(gl.GL_DEPTH_TEST)
#gl.glEnable(gl.GL_CULL_FACE)

@window.event
def on_draw():
    window.clear()

    gl.glMatrixMode(gl.GL_PROJECTION) # Теперь текущей является матрица проецирования
    gl.glLoadIdentity() # Инициализация матрицы проецирования
    gl.glOrtho(0, w, 0, h, -1, 1) # Ортографическое проецирование
    
    for _ in range(100):
        gl.glPointSize(random.uniform(1, 100))
        gl.glBegin(gl.GL_POINTS)
        gl.glColor3f(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        gl.glVertex2f(random.uniform(0, w), random.uniform(0, h))
        gl.glEnd()

def update(dt):
    pass

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/4) # schedule 60 times per second
    pyglet.app.run()
