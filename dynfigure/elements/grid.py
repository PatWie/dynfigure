#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from .base import element_register, BaseElement
from ..style import Style
import numpy as np


@element_register()
class Grid(BaseElement):
    def __init__(self, start, stop, xstep=1, ystep=1, style=Style()):
        self.default()
        self.style = style.clone()

        self.start = np.array(start)
        self.stop = np.array(stop)

        self.step = np.array([xstep, ystep])

    @property
    def xstep(self):
        return self.step[0]

    @property
    def ystep(self):
        return self.step[0]
