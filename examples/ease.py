#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

"""
Visualization several ease functions.
"""

from dynfigure import *
from dynfigure.elements import *
import numpy as np


def kth_position(k):
    return 100 + k * 30


tweens = [
    ease.EaseInSine,
    ease.EaseOutBounce,
    ease.EaseInQuad,
    ease.EaseOutElastic,
    ease.EaseLinear
]

PART_HEIGHT = 100
PART_WIDTH = 100
PADDING = 50

HEIGHT = 200
WIDTH = len(tweens) * (PART_WIDTH + PADDING) + PADDING


def draw_state(t):
    with CoordinateSystem(xscale=1, yscale=1):
        scene = Scene()
        # scene.put(Grid((0, 0), (WIDTH, HEIGHT), 50, 50, style=Style('black!0.5!white', line_width=0.1)))

        for k, tween in enumerate(tweens):

            curve = []

            with CoordinateSystem(xshift=50 + PART_WIDTH * k + PADDING * k - WIDTH // 2, yshift=-50, xscale=1, yscale=1):
                for x, y in enumerate(tween(100).generate()):
                    curve.append((x, y))

                curve = np.array(curve)

                x_stretch = Coordinate.stretch(domain=[curve[:, 0].min(), curve[:, 0].max()],
                                               range=[0, PART_WIDTH])
                curve[:, 0] = x_stretch(curve[:, 0])
                y_stretch = Coordinate.stretch(domain=[curve[:, 1].min(), curve[:, 1].max()],
                                               range=[0, PART_HEIGHT])
                curve[:, 1] = y_stretch(curve[:, 1])

                for k in range(curve.shape[0] - 1):
                    scene.put(Line(list(curve[k]), list(curve[k + 1]), style=Style('red', 'red!0.5!white')))

                current_x = x_stretch(t)
                current_y = y_stretch(tween(100)(t))

                scene.put(Circle((current_x, current_y), '5px', style=Style('color2', 'color2!0.5!white')))

        return scene

# ----------------------------------------------------------------------------------------------------------------------
# export to video
# ----------------------------------------------------------------------------------------------------------------------
with exporter.Mp4('ease.mp4', height=HEIGHT, width=WIDTH) as video:
    cam = camera.Camera2D(height=HEIGHT, width=WIDTH)

    for t in range(100):
        video.add_frame(cam.render(draw_state(t)))

with exporter.Gif('ease.gif', height=HEIGHT, width=WIDTH, fps=30) as video:
    for t in range(100):
        video.add_frame(cam.render(draw_state(t)))
