#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

"""
Visualization of Product-Quantization used for clustering.
"""

from dynfigure import *
from dynfigure.elements import *
import numpy as np

H = W = 512
PAD = 64
NUM_CENTROIDS1 = 2
NUM_CENTROIDS2 = 2

blue_color = Color(31, 120, 180, 255)
red_color = Color(178, 24, 43, 255)

# generate some data
np.random.seed(42)

X = np.concatenate([
    np.random.randn(50, 2) + np.array([0, 5]),
    np.random.randn(450, 2) + np.array([1.5, 0.5]),
    np.random.randn(250, 2) + np.array([5, 0]),
], axis=0)


def kmeans_update(X, C):
    C_new = C.copy()
    num_clusters = C_new.shape[0]
    ids = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in C_new]) for x_i in X])
    C_new = C_new.copy()
    for k in range(num_clusters):
        tmp = X[ids == k]
        if tmp.shape[0] > 0:
            C_new[k] = tmp.mean(axis=0)
    return C_new


def kmeans_update2(X, l1_ids, C):
    C_new = C.copy()

    for l1 in range(l1_ids.max() + 1):
        subX = X[l1_ids == l1]
        if subX.shape[0] > 0:
            subC = C_new[l1 * NUM_CENTROIDS2:l1 * NUM_CENTROIDS2 + NUM_CENTROIDS2, :]
            C_new[l1 * NUM_CENTROIDS2:l1 * NUM_CENTROIDS2 + NUM_CENTROIDS2, :] = kmeans_update(subX, subC)

    return C_new


# stretch points -> make sure they fit the entire sceen
X[:, 0] = Coordinate.stretch(domain=[X[:, 0].min(), X[:, 0].max()], range=[-W // 2 + PAD, W // 2 - PAD])(X[:, 0])
X[:, 1] = Coordinate.stretch(domain=[X[:, 1].min(), X[:, 1].max()], range=[-H // 2 + PAD, H // 2 - PAD])(X[:, 1])


def draw_points(X, scene, opacity=0.5, radius=['4px', '4px'], color='black'):
    """Helper to draw points
    """
    with CoordinateSystem():
        c_opacity = 0.9 * opacity
        f_opacity = 0.5 * opacity

        color = Color(color)

        color = color.interpolate(Color('white'), c_opacity)
        fill_color = color.interpolate(Color('white'), f_opacity)

        circles = []
        # draw data points
        with Scope(Circle, style=Style(color=color,
                                       fill_color=fill_color,
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
xl1 = None
yl1 = None
xl2 = None
yl2 = None


def animate_axis_clustering_l1(X, steps=6):
    global xl1
    global yl1
    # projected
    X_xaxis = X.copy()
    X_xaxis[:, 1] = -H // 2 + PAD

    X_yaxis = X.copy()
    X_yaxis[:, 0] = -W // 2 + PAD

    noise_x_axis = np.random.randn(NUM_CENTROIDS1, 2) * 80 * np.array([1, 0])
    noise_y_axis = np.random.randn(NUM_CENTROIDS1, 2) * 80 * np.array([0, 1])

    # start clustering here
    x_clusters_start = X_xaxis.mean(axis=0) + noise_x_axis
    y_clusters_start = X_yaxis.mean(axis=0) + noise_y_axis

    scene = Scene()
    draw_points(X, scene, opacity=0.3)

    draw_points(X_xaxis, scene, radius=['1px', '4px'], opacity=1)
    draw_points(X_yaxis, scene, radius=['4px', '1px'], opacity=1)

    x_objs = draw_points(x_clusters_start, scene, radius=['4px', '4px'], color=blue_color, opacity=1)
    y_objs = draw_points(y_clusters_start, scene, radius=['4px', '4px'], color=blue_color, opacity=1)

    with CoordinateSystem():
        for step in range(steps):
            x_clusters_stop = kmeans_update(X_xaxis, x_clusters_start)
            y_clusters_stop = kmeans_update(X_yaxis, y_clusters_start)

            for tau in ease.EaseOutCubic(20).generate():

                x_cluster_position = tau * x_clusters_stop + (1 - tau) * x_clusters_start
                y_cluster_position = tau * y_clusters_stop + (1 - tau) * y_clusters_start

                for k in range(NUM_CENTROIDS1):
                    x_objs[k].position = x_cluster_position[k]
                    y_objs[k].position = y_cluster_position[k]

                yield scene, x_clusters_stop, y_clusters_stop

            x_clusters_start = x_clusters_stop.copy()
            y_clusters_start = y_clusters_stop.copy()

    xl1 = x_clusters_stop.copy()
    yl1 = y_clusters_stop.copy()


# ----------------------------------------------------------------------------------------------------------------------
# animate clustering on each axis independently
# ----------------------------------------------------------------------------------------------------------------------


def animate_shift_l1_clusters(X):
    global xl1
    global yl1
    global xl2
    global yl2
    # projected
    X_xaxis = X.copy()
    X_xaxis[:, 1] = -H // 2 + PAD

    X_yaxis = X.copy()
    X_yaxis[:, 0] = -W // 2 + PAD

    # start clustering here
    xl1_stop = xl1 - np.array([0, 20])
    yl1_stop = yl1 - np.array([20, 0])

    scene = Scene()
    draw_points(X, scene, opacity=0.3)

    draw_points(X_xaxis, scene, radius=['1px', '4px'], opacity=1)
    draw_points(X_yaxis, scene, radius=['4px', '1px'], opacity=1)

    x_objs = draw_points(xl1, scene, radius=['4px', '4px'], color=blue_color, opacity=1)
    y_objs = draw_points(yl1, scene, radius=['4px', '4px'], color=blue_color, opacity=1)

    with CoordinateSystem():
        for tau in ease.EaseOutCubic(30).generate():
            xl1_position = tau * xl1_stop + (1 - tau) * xl1
            yl1_position = tau * yl1_stop + (1 - tau) * yl1

            for k in range(NUM_CENTROIDS1):
                x_objs[k].position = xl1_position[k]
                y_objs[k].position = yl1_position[k]

            yield scene

    xl1 = xl1_position
    yl1 = yl1_position


def animate_axis_clustering_l2(X, steps=6):
    global xl1
    global yl1
    global xl2
    global yl2
    # projected
    X_xaxis = X.copy()
    X_xaxis[:, 1] = -H // 2 + PAD

    X_yaxis = X.copy()
    X_yaxis[:, 0] = -W // 2 + PAD

    # start clustering here

    xl2 = np.concatenate([xl1, xl1], axis=1).reshape([-1, 2]) \
        + np.random.randn(NUM_CENTROIDS1 * NUM_CENTROIDS2, 2) * 20 * np.array([1, 0])
    yl2 = np.concatenate([yl1, yl1], axis=1).reshape([-1, 2]) \
        + np.random.randn(NUM_CENTROIDS1 * NUM_CENTROIDS2, 2) * 20 * np.array([0, 1])

    x_clusters_start = xl2.copy()
    y_clusters_start = yl2.copy()

    scene = Scene()
    draw_points(X, scene, opacity=0.3)

    draw_points(X_xaxis, scene, radius=['1px', '4px'], opacity=1)
    draw_points(X_yaxis, scene, radius=['4px', '1px'], opacity=1)

    # level 1
    draw_points(xl1, scene, radius=['4px', '4px'], color=blue_color, opacity=1)
    draw_points(yl1, scene, radius=['4px', '4px'], color=blue_color, opacity=1)

    x_objs = draw_points(x_clusters_start, scene, radius=['4px', '4px'], color=red_color, opacity=1)
    y_objs = draw_points(y_clusters_start, scene, radius=['4px', '4px'], color=red_color, opacity=1)

    ids_x = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in xl1]) for x_i in X_xaxis])
    ids_y = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in yl1]) for x_i in X_yaxis])

    with CoordinateSystem():
        for step in range(steps):

            x_clusters_stop = kmeans_update2(X_xaxis, ids_x, x_clusters_start)
            y_clusters_stop = kmeans_update2(X_yaxis, ids_y, y_clusters_start)

            for tau in ease.EaseOutCubic(20).generate():

                x_cluster_position = tau * x_clusters_stop + (1 - tau) * x_clusters_start
                y_cluster_position = tau * y_clusters_stop + (1 - tau) * y_clusters_start

                for k in range(NUM_CENTROIDS1 * NUM_CENTROIDS2):
                    x_objs[k].position = x_cluster_position[k]
                    y_objs[k].position = y_cluster_position[k]

                yield scene

            x_clusters_start = x_clusters_stop.copy()
            y_clusters_start = y_clusters_stop.copy()

    xl2 = x_clusters_start.copy()
    yl2 = y_clusters_start.copy()


# ----------------------------------------------------------------------------------------------------------------------
# animate projection clusters from axis to space back
# ----------------------------------------------------------------------------------------------------------------------
def animate_project_back(X):
    global xl1
    global yl1
    global xl2
    global yl2

    new_clusters_l1 = np.zeros((NUM_CENTROIDS1 * NUM_CENTROIDS1, 2))
    new_clusters_l2 = np.zeros((NUM_CENTROIDS1 * NUM_CENTROIDS2 * NUM_CENTROIDS1 * NUM_CENTROIDS2, 2))
    for i in range(NUM_CENTROIDS1):
        for j in range(NUM_CENTROIDS1):
            ij = i * NUM_CENTROIDS1 + j
            new_clusters_l1[ij, 0] = xl1[i, 0]
            new_clusters_l1[ij, 1] = yl1[j, 1]
    for i in range(NUM_CENTROIDS1 * NUM_CENTROIDS2):
        for j in range(NUM_CENTROIDS1 * NUM_CENTROIDS2):
            ij = i * NUM_CENTROIDS1 * NUM_CENTROIDS2 + j
            new_clusters_l2[ij, 0] = xl2[i, 0]
            new_clusters_l2[ij, 1] = yl2[j, 1]

    X_xaxis = X.copy()
    X_xaxis[:, 1] = -H // 2 + PAD

    X_yaxis = X.copy()
    X_yaxis[:, 0] = -W // 2 + PAD

    xl1_start = new_clusters_l1 * np.array([1, 0]) - np.array([0, 20]) + np.array([0, -H//2 + PAD])
    yl1_start = new_clusters_l1 * np.array([0, 1]) - np.array([20, 0]) + np.array([-W//2 + PAD, 0])

    xl2_start = new_clusters_l2 * np.array([1, 0]) + np.array([0, -H//2 + PAD])
    yl2_start = new_clusters_l2 * np.array([0, 1]) + np.array([-W//2 + PAD, 0])

    xl1_stop = new_clusters_l1
    yl1_stop = new_clusters_l1

    xl2_stop = new_clusters_l2
    yl2_stop = new_clusters_l2

    scene = Scene()
    draw_points(X, scene, opacity=0.3)

    draw_points(X_xaxis, scene, radius=['1px', '4px'], opacity=1)
    draw_points(X_yaxis, scene, radius=['4px', '1px'], opacity=1)

    x_objs1 = draw_points(xl1_start, scene, radius=['4px', '4px'], color=blue_color, opacity=1)
    y_objs1 = draw_points(yl1_start, scene, radius=['4px', '4px'], color=blue_color, opacity=1)

    x_objs2 = draw_points(xl2_start, scene, radius=['4px', '4px'], color=red_color, opacity=1)
    y_objs2 = draw_points(yl2_start, scene, radius=['4px', '4px'], color=red_color, opacity=1)

    for tau in ease.EaseOutCubic(30 * 4).generate():

        with CoordinateSystem():
            xl1_pos = tau * xl1_stop + (1 - tau) * xl1_start
            yl1_pos = tau * yl1_stop + (1 - tau) * yl1_start

            xl2_pos = tau * xl2_stop + (1 - tau) * xl2_start
            yl2_pos = tau * yl2_stop + (1 - tau) * yl2_start

            for k in range(NUM_CENTROIDS1 * NUM_CENTROIDS1):
                x_objs1[k].position = xl1_pos[k]
                y_objs1[k].position = yl1_pos[k]

            for k in range(NUM_CENTROIDS1 * NUM_CENTROIDS1 * NUM_CENTROIDS2 * NUM_CENTROIDS2):
                x_objs2[k].position = xl2_pos[k]
                y_objs2[k].position = yl2_pos[k]

        yield scene


# ----------------------------------------------------------------------------------------------------------------------
# export to video
# ----------------------------------------------------------------------------------------------------------------------

def paste_scheme(scene):
    ii = Image('pqt_scheme.png', [W, 40], scaling=0.5)
    scene.put(ii)
    return scene


with exporter.Mp4('pqt.mp4', height=H, width=2 * W) as video:
    cam = camera.Camera2D(width=2 * W, height=H, pc=[W // 2, H // 2])

    scene = None

    if False:
        scene = paste_scheme(next(animate_move_generator()))
        cam.render(scene).save('debug.png')

    # move points to axis
    for scene in animate_move_generator():
        video.add_frame(cam.render(paste_scheme(scene)))

    # clustering per axis
    cluster_x = None
    cluster_y = None
    for scene, cluster_x, cluster_y in animate_axis_clustering_l1(X):
        video.add_frame(cam.render(paste_scheme(scene)))

    for scene in animate_shift_l1_clusters(X):
        video.add_frame(cam.render(paste_scheme(scene)))

    for scene in animate_axis_clustering_l2(X):
        video.add_frame(cam.render(paste_scheme(scene)))

    for scene in animate_project_back(X):
        video.add_frame(cam.render(paste_scheme(scene)))

    cam.render(scene).save('final_pqt.png')
