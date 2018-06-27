#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

"""
Visualization of Product-Quantization used for clustering.
"""

from dynfigure import *
from dynfigure.elements import *
import numpy as np

H = W = 1024
PAD = 128
NUM_CENTROIDS = 4

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
# animate projection of points to axis
# ----------------------------------------------------------------------------------------------------------------------
def animate_move(scene, X, tau):
    opacity_mapper = Coordinate.stretch(domain=[0, 1], range=[0.5, 1])
    opacity_points_mapper = Coordinate.stretch(domain=[0, 1], range=[0.5, 0.3])

    draw_points(X, scene, opacity=opacity_points_mapper(tau))

    r = int(tau * 6 + (1 - tau) * 4)
    rr = int(tau * 1 + (1 - tau) * 4)

    X_left = X.copy()
    X_left[:, 0] = -W//2 + PAD

    X_bottom = X.copy()
    X_bottom[:, 1] = -H//2 + PAD

    draw_points(tau * X_left + (1 - tau) * X, scene, radius=['%ipx' % r, '%ipx' % rr],
                 opacity=opacity_mapper(tau))
    draw_points(tau * X_bottom + (1 - tau) * X, scene, radius=['%ipx' % rr, '%ipx' % r],
                opacity=opacity_mapper(tau))

    return scene


def animate_move_generator():
    # x-axis projection
    for tau in ease.EaseOutCubic(30 * 4).generate():
        scene = Scene()
        animate_move(scene, X, tau)
        yield scene


# ----------------------------------------------------------------------------------------------------------------------
# animate clustering on each axis independently
# ----------------------------------------------------------------------------------------------------------------------
def animate_axis_clustering(X, steps=4):

    def kmeans_update(X, C, step=0):
        C_new = C.copy()
        num_clusters = C_new.shape[0]
        ids = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in C_new]) for x_i in X])
        C_new = C_new.copy()
        for k in range(num_clusters):
            C_new[k] = X[ids == k].mean(axis=0)
        return C_new

    # projected

    X_xaxis = X.copy()
    X_xaxis[:, 1] = -H//2 + PAD

    X_yaxis = X.copy()
    X_yaxis[:, 0] = -W//2 + PAD

    noise_x_axis = np.random.randn(NUM_CENTROIDS, 2) * 80 * np.array([1, 0])
    noise_y_axis = np.random.randn(NUM_CENTROIDS, 2) * 80 * np.array([0, 1])


    # start clustering here
    x_clusters_start = X_xaxis.mean(axis=0) + noise_x_axis
    y_clusters_start = X_yaxis.mean(axis=0) + noise_y_axis

    scene = Scene()
    draw_points(X, scene, opacity=0.3)

    draw_points(X_xaxis, scene, radius=['1px', '6px'], opacity=1)
    draw_points(X_yaxis, scene, radius=['6px', '1px'], opacity=1)

    x_objs = draw_points(x_clusters_start, scene, radius=['8px', '8px'], color='red', opacity=1)
    y_objs = draw_points(y_clusters_start, scene, radius=['8px', '8px'], color='red', opacity=1)

    with CoordinateSystem():
        for step in range(steps):
            x_clusters_stop = kmeans_update(X_xaxis, x_clusters_start)
            y_clusters_stop = kmeans_update(X_yaxis, y_clusters_start)

            for tau in ease.EaseOutCubic(30).generate():

                x_cluster_position = tau * x_clusters_stop + (1 - tau) * x_clusters_start
                y_cluster_position = tau * y_clusters_stop + (1 - tau) * y_clusters_start

                for k in range(NUM_CENTROIDS):
                    x_objs[k].position = x_cluster_position[k]
                    y_objs[k].position = y_cluster_position[k]

                yield scene, x_clusters_stop, y_clusters_stop

            x_clusters_start = x_clusters_stop.copy()
            y_clusters_start = y_clusters_stop.copy()


# ----------------------------------------------------------------------------------------------------------------------
# animate projection clusters from axis to space back
# ----------------------------------------------------------------------------------------------------------------------
def animate_project_back(X, x_cluster_start, y_cluster_start):

    new_clusters = np.zeros((NUM_CENTROIDS * NUM_CENTROIDS, 2))
    for i in range(NUM_CENTROIDS):
        for j in range(NUM_CENTROIDS):
            ij = i * NUM_CENTROIDS + j
            new_clusters[ij, 0] = x_cluster_start[i, 0]
            new_clusters[ij, 1] = y_cluster_start[j, 1]

    X_xaxis = X.copy()
    X_xaxis[:, 1] = -H//2 + PAD

    X_yaxis = X.copy()
    X_yaxis[:, 0] = -W//2 + PAD

    x_clusters_start = new_clusters * np.array([1, 0]) + np.array([0, -H//2 + PAD])
    y_clusters_start = new_clusters * np.array([0, 1]) + np.array([-W//2 + PAD, 0])

    x_clusters_stop = new_clusters
    y_clusters_stop = new_clusters

    scene = Scene()
    draw_points(X, scene, opacity=0.3)

    draw_points(X_xaxis, scene, radius=['1px', '6px'], opacity=1)
    draw_points(X_yaxis, scene, radius=['6px', '1px'], opacity=1)

    x_objs = draw_points(x_clusters_start, scene, radius=['8px', '8px'], color='red', opacity=1)
    y_objs = draw_points(y_clusters_start, scene, radius=['8px', '8px'], color='red', opacity=1)

    for tau in ease.EaseOutCubic(30 * 4).generate():

        with CoordinateSystem():
            x_cluster_position = tau * x_clusters_stop + (1 - tau) * x_clusters_start
            y_cluster_position = tau * y_clusters_stop + (1 - tau) * y_clusters_start

            for k in range(NUM_CENTROIDS * NUM_CENTROIDS):
                    x_objs[k].position = x_cluster_position[k]
                    y_objs[k].position = y_cluster_position[k]

        yield scene


# ----------------------------------------------------------------------------------------------------------------------
# export to video
# ----------------------------------------------------------------------------------------------------------------------
with exporter.Mp4('pq.mp4', height=H, width=W) as video:
    cam = camera.Camera2D(width=W, height=H)

    # cam.render(next(animate_move_generator())).save('debug.png')

    # move points to axis
    for scene in animate_move_generator():
        video.add_frame(cam.render(scene))

    # clustering per axis
    cluster_x = None
    cluster_y = None
    for scene, cluster_x, cluster_y in animate_axis_clustering(X):
        video.add_frame(cam.render(scene))

    # project clusters back to space
    for scene in animate_project_back(X, cluster_x, cluster_y):
        video.add_frame(cam.render(scene))
