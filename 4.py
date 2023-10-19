#!/usr/bin/env python3

import pyglet
from pyglet import gl
import math
import random
import colorsys
import re

re_vertex = re.compile('^v\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)$')
re_normal = re.compile('^vn\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)$')
re_face = re.compile('^f\s(([0-9]+)(\/[0-9]+\/[0-9]+))\s(([0-9]+)(\/[0-9]+\/[0-9]+))\s(([0-9]+)(\/[0-9]+\/[0-9]+))$')

hampter_verts = []
hampter_normals = [] # TODO:
hampter_faces = []
with open('hampter.obj') as f:
    for line in f:
        s = re_vertex.search(line)
        if s != None:
            print("vertex")
            hampter_verts.append((float(s.group(1)), float(s.group(3)), float(s.group(5))))
        else:
            s = re_normal.search(line)
            if s != None:
                print("normal")
            else:
                s = re_face.search(line)
                if s != None:
                    hampter_faces.append((int(s.group(2)), int(s.group(5)), int(s.group(8))))
                else:
                    print("unknown", line)

# Direct OpenGL commands to this window.
w = 800
h = 600
window = pyglet.window.Window(width=w, height=h)

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

gl.glClearColor(0, 0, 0, 1) # чёрный цвет
gl.glClear(gl.GL_COLOR_BUFFER_BIT)
#gl.glEnable(gl.GL_POINT_SMOOTH)

gl.glEnable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_CULL_FACE)

angle = 0
scale = 1

@window.event
def on_draw():
    window.clear()

    gl.glMatrixMode(gl.GL_PROJECTION) # Теперь текущей является матрица проецирования
    gl.glLoadIdentity() # Инициализация матрицы проецирования
    gl.glOrtho(-1, 1, -h/w, h/w, -1, 1) # Ортографическое проецирование

    gl.glRotatef(angle, 0, -1, 0)
    gl.glScalef(scale, scale, scale)
    for f in hampter_faces:
        gl.glBegin(gl.GL_TRIANGLES)
        for vi in f:
            v = hampter_verts[vi - 1]
            gl.glVertex3f(*v)
        gl.glEnd()

def update(dt):
    global angle
    global scale

    if keys[pyglet.window.key.LEFT]:
        print('LEFT')
        angle += 10 * dt
    elif keys[pyglet.window.key.RIGHT]:
        print('RIGHT')
        angle -= 10 * dt
    if angle < 0:
        angle = 360 + angle
    else:
        angle %= 360

    if keys[pyglet.window.key.UP]:
        print('UP')
        scale += 1 * dt
    elif keys[pyglet.window.key.DOWN]:
        print('DOWN')
        scale -= 1 * dt
    scale = min(max(scale, 1), 10)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60) # schedule 60 times per second
    pyglet.app.run()
