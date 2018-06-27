#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

"""
Simple clock, mostly for debugging new stuff.
"""

from dynfigure import *
from dynfigure.elements import *

SIZE = 512

with CoordinateSystem() as sys:
    scene = Scene()
    clock_center = [0, 0]

    clock_diameter = SIZE // 2 - 28
    clock_radius = clock_diameter // 2

    scene.put(Circle(clock_center, clock_diameter, style=Style(color='black', line_width=0.5)))

    scene.put(Circle(clock_center, 3, style=Style(color='black',
                                                  fill_color='black')))

    with Scope([Line], style=Style(color='black!0.9!white', line_width=1)):
        # minutes
        for alpha in range(0, 360, 6):
            # start = clock_center + Coordinate(angle=alpha, distance=clock_radius * 0.9)
            # stop = clock_center + Coordinate(angle=alpha, distance=clock_radius)

            start = clock_center + sys.polar2cartesian(angle=alpha, distance=clock_diameter * 0.9)
            stop = clock_center + sys.polar2cartesian(angle=alpha, distance=clock_diameter)
            scene.put(Line(start, stop))

    with Scope([Line], style=Style(color='black!0.9!white', line_width=5)):
        # hours
        for alpha in range(0, 360, 30):
            start = clock_center + sys.polar2cartesian(angle=alpha, distance=clock_diameter * 0.8)
            stop = clock_center + sys.polar2cartesian(angle=alpha, distance=clock_diameter)
            scene.put(Line(start, stop))

    hand_hrs = Line(clock_center,
                    clock_center + sys.polar2cartesian(angle=6 * 20, distance=clock_diameter * 0.5),
                    style=Style(color='black', line_width=7))
    scene.put(hand_hrs)

    hand_min = Line(clock_center,
                    clock_center + sys.polar2cartesian(angle=6 * 8, distance=clock_diameter * 0.75),
                    style=Style(color='black', line_width=3))
    scene.put(hand_min)

    hand_sec = Line(clock_center,
                    clock_center + sys.polar2cartesian(angle=6 * 0 + 6 * 15, distance=clock_diameter),
                    style=Style(color='red'))
    scene.put(hand_sec)

    cam = camera.Camera2D(width=SIZE, height=SIZE)

    with exporter.Mp4('clock.mp4', height=SIZE, width=SIZE) as vid:
        for i in range(60):
            hand_sec.stop = (clock_center + sys.polar2cartesian(angle=-6 * i + 6 * 15, distance=clock_diameter))

            vid.add_frame(cam.render(scene), vid.fps)

    with exporter.Gif('clock.gif', height=SIZE, width=SIZE, fps=1) as vid:
        for i in range(60):
            hand_sec.stop = (clock_center + sys.polar2cartesian(angle=-6 * i + 6 * 15, distance=clock_diameter))
            vid.add_frame(cam.render(scene))
