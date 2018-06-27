#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

"""
Visualization of K-Means used for clustering.
"""

from dynfigure import *
from dynfigure.elements import *

import numpy as np

np.random.seed(4242)

NUM_CLUSTERS = 4
NUM_POINTS = 213
HEIGHT = 500
WIDTH = 500
FRAMES_MOVE = 30


def visualize_state(X, C, assignments=None, show_lines=False):
    colors = Color.scheme(NUM_CLUSTERS, start=2)

    with CoordinateSystem(xscale=1, yscale=1):

        scene = Scene()
        if assignments is None:
            # draw data points
            with Scope(Circle, style=Style(color='color3', fill_color='color3!0.9!white', line_width=0.5)):
                for x in X:
                    scene.put(Circle(list(x), 1))
        else:
            def sty(c): return Style(color=c, fill_color=c, line_width=0.5)
            for k in range(X.shape[0]):
                scene.put(Circle(list(X[k]), 1, sty(colors[assignments[k]])))

        # draw centroids
        for k in range(NUM_CLUSTERS):
            scene.put(Circle(list(C[k]), 3, Style(color=colors[k],
                                                  fill_color=colors[k].interpolate('white', 0.7),
                                                  line_width=0.5)))

        # draw lines
        if show_lines:
            if assignments is not None:
                for k in range(X.shape[0]):
                    style = Style(color=colors[assignments[k]],
                                  fill_color=colors[assignments[k]], line_width=1)
                    scene.put(Line(list(C[assignments[k]]), list(X[k, :]), style))

        return scene


X = np.random.randn(NUM_POINTS, 2)
X[:, 0] = Coordinate.stretch(domain=[X[:, 0].min(), X[:, 0].max()], range=[-WIDTH // 2, WIDTH // 2])(X[:, 0])
X[:, 1] = Coordinate.stretch(domain=[X[:, 1].min(), X[:, 1].max()], range=[-HEIGHT // 2, HEIGHT // 2])(X[:, 1])

C = np.expand_dims(X.mean(axis=0), axis=0) + (np.random.randn(NUM_CLUSTERS, 2))


def algorithm(X, C):
    # the algorithm
    for step_id in range(15):
        # assign clusters
        ids = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in C]) for x_i in X])

        yield visualize_state(X, C, assignments=ids, show_lines=True)

        # update cluster centers
        C_new = C.copy()
        for k in range(NUM_CLUSTERS):
            C_new[k] = X[ids == k].mean(axis=0)

        for t in ease.EaseOutCubic(FRAMES_MOVE).generate():
            yield visualize_state(X, (1 - t) * C + t * C_new, assignments=ids, show_lines=True)

        C = C_new.copy()


with exporter.Mp4('kmeans.mp4', height=HEIGHT, width=WIDTH) as video:
    cam = camera.Camera2D(height=HEIGHT, width=WIDTH)

    for scene in algorithm(X, C):
        video.add_frame(cam.render(scene))


with exporter.Gif('kmeans.gif', height=HEIGHT, width=WIDTH, fps=30) as video:
    for scene in algorithm(X, C):
        video.add_frame(cam.render(scene))
