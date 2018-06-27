#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from .coordinate import Coordinate


class BoundingBox(object):
    """docstring for BoundingBox"""
    def __init__(self, p1=(0, 0), p2=(0, 0)):
        super(BoundingBox, self).__init__()
        self.p1 = Coordinate(p1).min(Coordinate(p1))
        self.p2 = Coordinate(p2).max(Coordinate(p2))

    @property
    def north(self):
        return Coordinate(self.p1.x + (self.p2.x - self.p1.x) / 2., self.p1.y)

    @property
    def east(self):
        return Coordinate(self.p2.x, self.p1.y + (self.p2.y - self.p1.y) / 2.)

    @property
    def south(self):
        return Coordinate(self.p1.x + (self.p2.x - self.p1.x) / 2., self.p2.y)

    @property
    def west(self):
        return Coordinate(self.p1.x, self.p1.y + (self.p2.y - self.p1.y) / 2.)

    @property
    def north_west(self):
        return Coordinate(self.p1.x, self.p1.y)

    @property
    def north_east(self):
        return Coordinate(self.p2.x, self.p1.y)

    @property
    def south_west(self):
        return Coordinate(self.p1.x, self.p2.y)

    @property
    def south_east(self):
        return Coordinate(self.p2.x, self.p2.y)

    @property
    def center(self):
        return Coordinate(self.p1.x + (self.p2.x - self.p1.x) / 2., self.p1.y + (self.p2.y - self.p1.y) / 2.)

    @property
    def height(self):
        return self.p2[1] - self.p1[1]

    @property
    def width(self):
        return self.p2[0] - self.p1[0]

    def merge(self, other):
        if other is None:
            return self
        else:
            p1 = Coordinate(self.p1).min(Coordinate(other.p1))
            p2 = Coordinate(self.p2).max(Coordinate(other.p2))

            return BoundingBox(p1, p2)

    def __str__(self):
        return '[(%.2f, %.2f), (%.2f, %.2f)]' % (self.p1[0], self.p1[1], self.p2[0], self.p2[1])
