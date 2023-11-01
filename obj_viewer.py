#!/usr/bin/env python3

# Просмотрщик моделей в формате OBJ
# Кузьменко Иван, 36/2, 2023
# https://github.com/rndtrash/uni-opengl
#
# Управление:
# - Вращение: стрелки влево и вправо
# - Масштаб: стрелки вверх и вниз
# - Режим автоматического вращения: пробел
#
# 3D модель сделана Grodbert, разрешение на использование и распространение получено

import pyglet
from pyglet import gl
import math
import random
import colorsys
import re
import time

model_path = input("Введите путь к файлу (например, hampter.obj): ")

re_vertex = re.compile('^v\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)$')
re_normal = re.compile('^vn\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)\s(-?[0-9]+(\.[0-9]+)?)$')
re_face = re.compile('^f\s([0-9]+)\/([0-9]+)\/([0-9]+)\s([0-9]+)\/([0-9]+)\/([0-9]+)\s([0-9]+)\/([0-9]+)\/([0-9]+)$')

model_verts = []
model_normals = []
model_faces = []
with open(model_path) as f:
    for line in f:
        s = re_vertex.search(line)
        if s != None:
            print("vertex")
            model_verts.append((float(s.group(1)), float(s.group(3)), float(s.group(5))))
        else:
            s = re_normal.search(line)
            if s != None:
                print("normal")
                model_normals.append((float(s.group(1)), float(s.group(3)), float(s.group(5))))
            else:
                s = re_face.search(line)
                if s != None:
                    model_faces.append(
                        (
                            # vertex normal                      vertex pos
                            (model_normals[int(s.group(3)) - 1], model_verts[int(s.group(1)) - 1]),
                            (model_normals[int(s.group(6)) - 1], model_verts[int(s.group(4)) - 1]),
                            (model_normals[int(s.group(9)) - 1], model_verts[int(s.group(7)) - 1])
                        )
                    )
                else:
                    print("unknown", line)

triangles_count = len(model_faces)

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
direction = 0

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
    for f in model_faces:
        for v in f:
            gl.glNormal3f(*v[0])
            gl.glVertex3f(*v[1])
    gl.glEnd()

    print("FPS:", 1 / (time.time() - time_begin), "triangles:", triangles_count)

def update(dt):
    global angle
    global scale
    global direction

    if keys[pyglet.window.key.SPACE]:
        if direction == 0:
            direction = 1
        else:
            direction = 0

    if direction != 0:
        if keys[pyglet.window.key.LEFT]:
            direction = 1
        elif keys[pyglet.window.key.RIGHT]:
            direction = -1
        angle += 10 * dt * direction
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
