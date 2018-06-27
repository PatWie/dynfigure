#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

import numpy as np
import six

__all__ = ['CoordinateSystem', 'get_coordinate_system']

_CoordinateSystemStack = []


class CoordinateSystem(object):

    """DynFigure interprets (x, y) as
        - x horizontal from left to right
        - y vertical from bottom to top
    """

    def __init__(self, xscale=1, yscale=1, zscale=1, xshift=0, yshift=0, zshift=0):
        super(CoordinateSystem, self).__init__()
        self.scale = [xscale, yscale, zscale]
        self.shift = [xshift, yshift, zshift]

    def apply(self, val):
        """Apply coordinate transformation in word-space

        Args:
            val: some vector in world-coordinates

        Returns:
            some transformed vector in world-coordinates
        """
        if isinstance(val, np.ndarray):
            val = val.tolist()

        if not isinstance(val, list):
            val = [val]

        for k in range(len(val)):
            if isinstance(val[k], six.string_types):
                val[k] = np.array(float(val[k].replace('px', '')))
            else:
                if k < 3:
                    val[k] = self.scale[k] * (val[k] + self.shift[k])

        return np.array(val)

    def stretch(self, val):
        if isinstance(val, np.ndarray):
            val = val.tolist()

        if not isinstance(val, list):
            val = [val]

        for k in range(len(val)):
            if isinstance(val[k], six.string_types):
                val[k] = np.array(float(val[k].replace('px', '')))
            else:
                if k < 3:
                    val[k] = self.scale[k] * (val[k] )

        return np.array(val)



    def __enter__(self):
        global _CoordinateSystemStack
        _CoordinateSystemStack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _CoordinateSystemStack
        del _CoordinateSystemStack[-1]

    def __str__(self):
        vals = (self._xscale, self._yscale, self._zscale, self._xshift, self._yshift, self._zshift)
        return '<DynFigure.CoordinateSystem:(scale: [%.2f, %.2f, %.2f] shift: [%.2f, %.2f, %.2f])>' % (vals)

    @staticmethod
    def polar2cartesian(angle, distance):
        angle = np.deg2rad(angle)
        x = distance * np.cos(angle)
        y = distance * np.sin(angle)

        return np.array([x, y])


def get_coordinate_system():
    global _CoordinateSystemStack
    if len(_CoordinateSystemStack) > 0:
        return _CoordinateSystemStack[-1]
    else:
        return CoordinateSystem()
