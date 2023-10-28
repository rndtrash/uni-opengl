#!/usr/bin/env python3

import pyglet
from pyglet import gl
import math
import random
import colorsys
import re
import time

re_vertex = re.compile('^v\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)$')
re_normal = re.compile('^vn\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)$')
re_face = re.compile('^f\s([0-9]+)\/([0-9]+)\/([0-9]+)\s([0-9]+)\/([0-9]+)\/([0-9]+)\s([0-9]+)\/([0-9]+)\/([0-9]+)$')

hampter_verts = []
hampter_normals = []
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
                hampter_normals.append((float(s.group(1)), float(s.group(3)), float(s.group(5))))
            else:
                s = re_face.search(line)
                if s != None:
                    hampter_faces.append(
                        (
                            # vertex normal                        vertex pos
                            (hampter_normals[int(s.group(3)) - 1], hampter_verts[int(s.group(1)) - 1]),
                            (hampter_normals[int(s.group(6)) - 1], hampter_verts[int(s.group(4)) - 1]),
                            (hampter_normals[int(s.group(9)) - 1], hampter_verts[int(s.group(7)) - 1])
                        )
                    )
                else:
                    print("unknown", line)

hampter_v_n_list = hampter_faces #np.asarray(hampter_faces, dtype=float).reshape((len(hampter_faces), 3, 2, 3))
print(hampter_v_n_list)

# Direct OpenGL commands to this window.
w = 800
h = 600
window = pyglet.window.Window(width=w, height=h, resizable=True)

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

gl.glClearColor(0, 0, 0, 1) # чёрный цвет
gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

gl.glEnable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_CULL_FACE)

angle = 0
scale = 10

def vec(*args):
    return (gl.GLfloat * len(args))(*args)

@window.event
def on_resize(width, height):
    global w
    global h
    print('The window was resized to %dx%d' % (width, height))
    w = width
    h = height

@window.event
def on_draw():
    time_begin = time.time()

    window.clear()

    gl.glViewport(0, 0, w, h)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity() # Инициализация матрицы проецирования
    gl.glFrustum(-1, 1, -1, 1, 3, 10) # Фрустум, перспективная проекция
    # TODO: скорректировать угол обзора, хомяка сжимает при изменении размера окна
    
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    # Да будет свет!
    gl.glEnable(gl.GL_LIGHTING)

    gl.glEnable(gl.GL_LIGHT0)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, vec(-2, 0, -2, 1))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, vec(1.0, 0.2, 0.2, 1))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, vec(0.1, 0.1, 0.1, 1))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPOT_CUTOFF, vec(180.0))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, vec(0.25))

    gl.glEnable(gl.GL_LIGHT1)
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, vec(2, 0, 2, 1))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_DIFFUSE, vec(0.2, 1.0, 0.2, 1))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_AMBIENT, vec(0.1, 0.1, 0.1, 1))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_SPOT_CUTOFF, vec(180.0))
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_CONSTANT_ATTENUATION, vec(0.25))

    gl.glTranslatef(0.0, 0.0, -8.0)
    gl.glRotatef(angle, 0, -1, 0)
    gl.glScalef(scale, scale, scale)
    gl.glBegin(gl.GL_TRIANGLES)
    for f in hampter_v_n_list:
        for v in f:
            gl.glNormal3f(*v[0])
            gl.glVertex3f(*v[1])
    gl.glEnd()

    print("FPS:", 1 / (time.time() - time_begin), "triangles:", len(hampter_v_n_list))

def update(dt):
    global angle
    global scale

    angle += 10 * dt
    return

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
