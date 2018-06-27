#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from abc import abstractmethod, ABCMeta
import six
import numpy as np

# see http://gsgd.co.uk/sandbox/jquery/easing/jquery.easing.1.3.js
# see http://easings.net


@six.add_metaclass(ABCMeta)
class Ease(object):
    """docstring for Ease"""

    def __init__(self, duration, start_value=0, end_value=1):
        super(Ease, self).__init__()
        self.duration = duration
        self.start_value = start_value
        self.end_value = end_value
        self.value_diff = end_value - start_value

    @abstractmethod
    def __call__(self, t):
        pass

    def generate(self):
        for t in np.arange(0, self.duration):
            yield self.__call__(t)


class EaseLinear(Ease):
    def __call__(self, t):
        return self.value_diff * (t / float(self.duration)) + self.start_value


class EaseInQuad(Ease):
    def __call__(self, t):
        return self.value_diff * (t / float(self.duration)) * (t / float(self.duration)) + self.start_value


class EaseInSine(Ease):
    def __call__(self, t):
        t = t / float(self.duration)
        b = self.start_value
        c = self.value_diff
        return -c * np.cos(t * (np.pi / 2.)) + c + b


class EaseOutCubic(Ease):
    def __call__(self, t):
        t = t / (float(self.duration) / 2.)
        b = self.start_value
        c = self.value_diff

        if t < 1:
            return c / 2. * t * t * t + b
        else:
            t -= 2
            return c / 2. * (t * t * t + 2) + b


class EaseOutBounce(Ease):
    def __call__(self, t):
        t = t / float(self.duration)
        b = self.start_value
        c = self.value_diff

        if t < 1 / 2.75:
            return c * (7.5625 * t * t) + b
        elif t < 2 / 2.75:
            t -= (1.5 / 2.75)
            return c * (7.5625 * t * t + .75) + b
        elif t < 2.5 / 2.75:
            t -= (2.25 / 2.75)
            return c * (7.5625 * t * t + .9375) + b
        else:
            t -= (2.625 / 2.75)
            return c * (7.5625 * t * t + .984375) + b


class EaseOutElastic(Ease):
    def __call__(self, t):
        b = self.start_value
        c = self.value_diff
        d = self.duration

        s = 1.70158
        p = 0
        a = c

        if t == 0:
            return b

        t = t / float(self.duration)
        if t == 1:
            return b + c

        if p == 0:
            p = d * 0.3

        if a < np.abs(c):
            a = c
            s = p / 4.
        else:
            s = p / (2. * np.pi) * np.arcsin(c / float(a))

        return a * np.power(2, -10 * t) * np.sin((t * d - s) * (2 * np.pi) / p) + c + b
