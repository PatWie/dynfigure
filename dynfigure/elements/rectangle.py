#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from .base import element_register, BaseElement
from ..style import Style
import numpy as np


@element_register()
class Rectangle(BaseElement):
    def __init__(self, start, stop, style=Style()):
        self.default()

        self.style = style.clone()

        self.start = np.array(start)
        self.stop = np.array(stop)
