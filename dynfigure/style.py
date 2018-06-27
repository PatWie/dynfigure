#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from .color import Color
import aggdraw
import copy


class Style(object):
    """docstring for Style"""
    def __init__(self, color=None, fill_color=None, line_width=None, opacity=None):
        super(Style, self).__init__()

        self.color = Color(color) if color is not None else None
        self.fill_color = Color(fill_color) if fill_color is not None else None

        self.line_width = line_width if line_width is not None else 1
        self.opacity = opacity if opacity is not None else 255

    @property
    def pen(self):
        if self.color is not None:
            return aggdraw.Pen(self.color.rgb, self.line_width)
        else:
            return None

    @property
    def brush(self):
        if self.fill_color is not None:
            return aggdraw.Brush(self.fill_color.rgb, self.opacity)
        else:
            return None

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        s = []
        if self.color is not None:
            s.append('draw=%s' % self.color.hash())

        if self.fill_color is not None:
            s.append('fill=%s' % self.fill_color.hash())

        if self.line_width is not None:
            s.append('line width=%s' % self.line_width)

        if self.opacity is not None:
            s.append('opacity=%.2f' % self.opacity)

        return ', '.join(s)
