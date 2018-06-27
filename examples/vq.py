#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

"""
Visualization of Vector-Quantization used for clustering.
"""

from dynfigure import *
from dynfigure.elements import *
import numpy as np

H = W = 1024
PAD = 128
NUM_CENTROIDS = 16

# generate some data
np.random.seed(42)

X = np.concatenate([
    np.random.randn(50, 2) + np.array([0, 5]),
    np.random.randn(450, 2) + np.array([1.5, 0.5]),
    np.random.randn(250, 2) + np.array([5, 0]),
], axis=0)


# stretch points -> make sure they fit the entire sceen
X[:, 0] = Coordinate.stretch(domain=[X[:, 0].min(), X[:, 0].max()], range=[-W//2 + PAD, W//2 - PAD])(X[:, 0])
X[:, 1] = Coordinate.stretch(domain=[X[:, 1].min(), X[:, 1].max()], range=[-H//2 + PAD, H//2 - PAD])(X[:, 1])



def draw_points(X, scene, opacity=0.5, radius=['4px', '4px'], color='black'):
    """Helper to draw points
    """
    with CoordinateSystem():
        c_opacity = 0.9 * opacity
        f_opacity = 0.5 * opacity

        circles = []
        # draw data points
        with Scope(Circle, style=Style(color='%s!%f!white' % (color, c_opacity),
                                       fill_color='%s!%f!white' % (color, f_opacity),
                                       line_width=0.8)):
            for x in X:
                circles.append(Circle(x, radius))
                scene.put(circles[-1])

        return circles


# ----------------------------------------------------------------------------------------------------------------------
# animate clustering on each axis independently
# ----------------------------------------------------------------------------------------------------------------------
def animate_clustering(X, steps=10):

    def kmeans_update(X, C, step=0):
        C_new = C.copy()
        num_clusters = C_new.shape[0]
        ids = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in C_new]) for x_i in X])
        C_new = C_new.copy()
        for k in range(num_clusters):
            C_new[k] = X[ids == k].mean(axis=0)
        return C_new

    C_start = X.mean(axis=0) + np.random.randn(NUM_CENTROIDS, 2) * 80

    scene = Scene()
    draw_points(X, scene, opacity=0.3)


    C_objs = draw_points(C_start, scene, radius=['8px', '8px'], color='red', opacity=1)

    with CoordinateSystem(xshift=PAD // 2, yshift=PAD // 2):
        for step in range(steps):
            C_stop = kmeans_update(X, C_start)

            for tau in ease.EaseOutCubic(30).generate():

                C_pos = tau * C_stop + (1 - tau) * C_start

                for k in range(NUM_CENTROIDS):
                    C_objs[k].position = C_pos[k]

                yield scene

            C_start = C_stop.copy()


# ----------------------------------------------------------------------------------------------------------------------
# export to video
# ----------------------------------------------------------------------------------------------------------------------
# scene = next(animate_clustering(X))
# cam = camera.Camera2D(width=W, height=H)
# cam.render(scene).save('debug.png')

with exporter.Mp4('vq.mp4', height=H, width=W) as video:
    cam = camera.Camera2D(width=W, height=H)
    for scene in animate_clustering(X):
        video.add_frame(cam.render(scene))
