#!/usr/bin/env python3

import pyglet
from pyglet import gl
import math

# Direct OpenGL commands to this window.
s = 20
w = 72 * s
h = 36 * s
window = pyglet.window.Window(width=w, height=h)
fov = h/w

gl.glClearColor(230/255, 27/255, 38/255, 1) # Красный цвет rgb(230, 27, 38)
gl.glClear(gl.GL_COLOR_BUFFER_BIT)

#gl.glEnable(gl.GL_DEPTH_TEST)
#gl.glEnable(gl.GL_CULL_FACE)

def makeStar(x, y, radius, innerRadius = 0.38, pointsPerFifth = 10):
    triangles = []

    for star_point in range(5):
        alpha = math.radians(90) - math.radians(72) * star_point
        beta = math.radians(90) - math.radians(72) * (star_point + 1)
        pStar = math.radians(90 + 72 / 2) - math.radians(72) * star_point
        vStar = (x + math.cos(pStar) * radius * innerRadius, y +math.sin(pStar) * radius * innerRadius, 0)
        for p in range(pointsPerFifth):
            pAlpha = alpha + math.radians(72) * p / pointsPerFifth
            pBeta = alpha + math.radians(72) * (p + 1) / pointsPerFifth
            triangles.append((
                (x + math.cos(pBeta) * radius, y + math.sin(pBeta) * radius, 0),
                (x + math.cos(pAlpha) * radius, y + math.sin(pAlpha) * radius, 0),
                vStar
            ))
    
    return triangles

#for t in makeStar(fov, 0.5):
#    print(t)

@window.event
def on_draw():
    window.clear()

    gl.glMatrixMode(gl.GL_PROJECTION) # Теперь текущей является матрица проецирования
    gl.glLoadIdentity() # Инициализация матрицы проецирования
    gl.glOrtho(-1, 1, -fov, fov, -1, 1) # Ортографическое проецирование
    
    gl.glColor3f(2/255, 77/255, 157/255) # Синий цвет rgb(2, 77, 157)
    
    gl.glBegin(gl.GL_QUADS) # Обход против часовой стрелки
    gl.glVertex3f(1, 1 * fov, 0)
    gl.glVertex3f(-1, 1 * fov, 0)
    gl.glVertex3f(-1, (1 - 6/36) * fov, 0)
    gl.glVertex3f(1, (1 - 6/36) * fov, 0)
    gl.glEnd()
    
    gl.glBegin(gl.GL_QUADS) # Обход против часовой стрелки
    gl.glVertex3f(1, -1 * fov, 0)
    gl.glVertex3f(-1, -1 * fov, 0)
    gl.glVertex3f(-1, (-1 + 6/36) * fov, 0)
    gl.glVertex3f(1, (-1 + 6/36) * fov, 0)
    gl.glEnd()

    gl.glColor3f(247/255, 247/255, 247/255) # Белый цвет rgb(247, 247, 247)
    
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex3f(1, (1 - 6/36) * fov, 0)
    gl.glVertex3f(-1, (1 - 6/36) * fov, 0)
    gl.glVertex3f(-1, (1 - (6 + 2)/36) * fov, 0)
    gl.glVertex3f(1, (1 - (6 + 2)/36) * fov, 0)
    gl.glEnd()
    
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex3f(1, (-1 + 6/36) * fov, 0)
    gl.glVertex3f(-1, (-1 + 6/36) * fov, 0)
    gl.glVertex3f(-1, (-1 + (6 + 2)/36) * fov, 0)
    gl.glVertex3f(1, (-1 + (6 + 2)/36) * fov, 0)
    gl.glEnd()

    for t in makeStar(-1 + 24 / 72 * 2, 0, 16 / 72):
        gl.glBegin(gl.GL_TRIANGLES)
        for v in t:
            gl.glVertex3f(v[0], v[1], v[2])
        gl.glEnd()

def update(dt):
    pass

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60) # schedule 60 times per second
    pyglet.app.run()
