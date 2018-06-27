#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from .base import element_register, BaseElement
from ..style import Style
import numpy as np


@element_register()
class Circle(BaseElement):
    def __init__(self, position, radius, style=Style()):
        """Summary

        Args:
            position: position as world coordinates
            radius: radius in world coordinates
            style: draw style
        """
        self.default()
        self.style = style.clone()
        self.position = np.array(position)
        self.radius = radius

    def __str__(self):
        return '<DynFigure.Circle:({}:{})>'.format(self.position, self.radius)
