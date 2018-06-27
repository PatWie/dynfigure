#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

import six
import copy


class PikzColorException(Exception):
    pass


class Color(object):
    """docstring for Color"""

    def __init__(self, r=255, g=255, b=255, a=255):
        super(Color, self).__init__()

        if isinstance(r, Color):
            self.r, self.g, self.b, self.a = r.r, r.g, r.b, r.a
        elif isinstance(r, six.string_types):
            c = self.interpret_color_string_as_rgb(r)
            self.r, self.g, self.b, self.a = c.r, c.g, c.b, c.a
        else:
            self.r, self.g, self.b, self.a = r, g, b, a

        self.r = int(self.r)
        self.g = int(self.g)
        self.b = int(self.b)
        self.a = int(self.a)

    def interpolate(self, other, w=0.5):
        other = Color(other)

        return Color(w * self.r + (1 - w) * other.r,
                     w * self.g + (1 - w) * other.g,
                     w * self.b + (1 - w) * other.b,
                     w * self.a + (1 - w) * other.a)

    @staticmethod
    def scheme(num, start=1):
        return [Color('color%i' % i) for i in range(start, start + num)]

    def interpret_color_string_as_rgb(self, val):

        if isinstance(val, Color):
            return val.rgb

        color_dict = {'white': (255, 255, 255, 255),
                      'red': (255, 0, 0, 255),
                      'green': (0, 255, 0, 255),
                      'blue': (0, 0, 255, 255),
                      'black': (0, 0, 0, 255)}

        color_scheme = {
            'color1': (15, 21, 24, 255),
            'color2': (0, 114, 189, 255),
            'color3': (27, 158, 119, 255),
            'color4': (217, 83, 25, 255),
            'color5': (126, 47, 142, 255),
            'color6': (162, 20, 47, 255),
            'color7': (77, 190, 238, 255),
            'color8': (119, 172, 48, 255),
            'color9': (227, 26, 28, 255),
            'color10': (141, 211, 199, 255),
            'color11': (185, 151, 207, 255),
            'color12': (249, 38, 114, 255),
            'color13': (253, 151, 31, 255),
            'color14': (0, 127, 217, 255),
            'color15': (0, 127, 0, 255),
            'color16': (204, 0.0, 0.0, 255),
            'color17': (255, 255, 0, 255)
        }

        if len(val.split('!')) == 3:
            # interpolate
            color_a = self.interpret_color_string_as_rgb(val.split('!')[0])
            color_b = self.interpret_color_string_as_rgb(val.split('!')[2])

            try:
                w = float(val.split('!')[1])
            except Exception as e:
                raise PikzColorException(e)

            return color_a.interpolate(color_b, w)
        else:
            if val in color_dict.keys():
                return Color(*color_dict[val])

            if val in color_scheme.keys():
                return Color(*color_scheme[val])

        raise PikzColorException('color %s does not exists' % val)

    def clone(self):
        return copy.deepcopy(self)

    @property
    def rgb(self):
        return (self.r, self.g, self.b, self.a)

    # def __str__(self):
    #     return '#%02x%02x%02x%02x' % (self.r, self.g, self.b, self.a)

    @property
    def hash(self):
        return 'mycolor%02x%02x%02x%02x' % (self.r, self.g, self.b, self.a)

    def __eq__(self, other):
        if other.r == self.r and other.g == self.g and other.b == self.b and other.a == self.a:
            return True
        else:
            return False
