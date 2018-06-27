#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from .base import element_register, BaseElement
from ..style import Style
import numpy as np
from PIL import Image as PilImage
import six


@element_register()
class Image(BaseElement):
    def __init__(self, src, top_left=[0, 0], style=Style(), scaling=1.):
        """Summary

        Args:
            position: position as world coordinates
            radius: radius in world coordinates
            style: draw style
        """
        self.default()
        self.style = style.clone()
        self.top_left = np.array(top_left)
        if isinstance(src, six.string_types):
            self.img = PilImage.open(src).convert("RGBA")
        else:
            self.img = src

        self.scaling = scaling

        if self.scaling != 1.0:
            width, height = self.img.size
            width, height = int(self.scaling * width), int(self.scaling * height)
            self.img = self.img.resize((width, height), PilImage.ANTIALIAS)

    def __str__(self):
        return '<DynFigure.Image:({}:{})>'.format(self.top_left, self.src.size)
