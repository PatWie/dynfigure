#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>


from abc import abstractmethod, ABCMeta
import six
import numpy as np
import PIL
import PIL.Image
import aggdraw
from ..color import Color

__all__ = ['BaseCamera']


@six.add_metaclass(ABCMeta)
class BaseCamera(object):
    """docstring for BaseCamera"""

    def __init__(self, m=1, width=1920, height=1080, pc=None,
                 background_color=Color('white'),
                 verbose=False):
        """Abstract Camera class

        Args:
            m (int, optional): pixel width
            width (int, optional): width of camera scene
            height (int, optional): height of camera scene
            pc (TYPE, optional): principal point of camera
            background_color (TYPE, optional): background_color
            verbose (bool, optional): print debug information during rendering
        """
        super(BaseCamera, self).__init__()
        self.__height = height
        self.__width = width
        self.__m = m

        if pc is None:
            pc = [width // 2, height // 2]

        self.__pc = pc

        self.background_color = background_color
        self.verbose = verbose

        self.setup()

    @property
    def pc(self):
        """Return principal camera point (screen space)
        """
        return self.__pc

    @property
    def screen_height(self):
        """Return total screen-height
        """
        return self.__height

    @property
    def screen_width(self):
        """Return total screen-width
        """
        return self.__width

    @property
    def screen_left(self):
        """Return x coordinate of left-most pixel (screen space)
        """
        return -self.__width // 2

    @property
    def screen_right(self):
        """Return x coordinate of right-most pixel (screen space)
        """
        return self.__width // 2

    @property
    def screen_top(self):
        """Return y coordinate of top-most pixel (screen space)
        """
        return self.__height // 2

    @property
    def screen_bottom(self):
        """Return y coordinate of bottom-most pixel (screen space)
        """
        return -self.__height // 2

    # painting methods
    def render(self, scene):
        """Summary

        Args:
            scene (TYPE): Description

        Returns:
            TYPE: Description
        """

        self.img = PIL.Image.new("RGBA", (self.__width, self.__height), self.background_color.rgb)
        self.ctx = aggdraw.Draw(self.img)

        scene.draw(self)
        return self.img

    def flush(self):
        self.ctx.flush()

    def draw(self, obj):
        # TODO: refactor
        tname = obj.__class__.__name__
        if self.verbose:
            print('Camera.draw {}'.format(obj))

        if tname == 'Circle':
            csys = obj.csys

            p = csys.apply(obj.position)
            r = csys.stretch(obj.radius)

            if r.shape[0] == 1:
                r = np.array([r[0], r[0]])

            p = self.world2image(p)[0]

            self.ctx.ellipse([p[0] - r[0], p[1] - r[1],
                              p[0] + r[0], p[1] + r[1]], obj.style.pen, obj.style.brush)
        elif tname == 'Image':

            self.ctx.flush()

            width, height = obj.img.size

            xy = obj.top_left.tolist()
            xy = [xy[0], xy[1], xy[0] + width, xy[1] + height]

            matched = PIL.Image.new("RGBA", self.img.size, (0, 255, 255, 0))
            matched.paste(obj.img, xy, obj.img)
            self.img = PIL.Image.alpha_composite(self.img, matched)
            # self.img.paste(obj.img, xy)

            self.ctx = aggdraw.Draw(self.img)
        elif tname == 'Line':
            # coordinates transformation
            start = obj.csys.apply(obj.start)
            stop = obj.csys.apply(obj.stop)

            # world coordinates to screen coordinates
            start = self.world2image(start)[0]
            stop = self.world2image(stop)[0]

            self.ctx.line((start[0], start[1],
                           stop[0], stop[1]), obj.style.pen)

        else:
            raise Exception('no renderer registered for element of type \'%s\'' % tname)

    # projection methods

    def _p2e(self, X):
        """
        Convert projective coordinates to Euclidean coordinates
        Remarks:
            [x, y, z]    --> [x / z, y / z]
            [x, y, z, s] --> [x / s, y / s, z / s]
        Args:
            X (np.ndarray[n, 3 or 4]): projective coordinate
        Returns:
            np.ndarray[n, 2 or 3]: euclidean coordinate
        """

        assert(type(X) == np.ndarray)
        assert((X.shape[0] == 4) | (X.shape[0] == 3))
        return (X / X[-1, :])[0:-1, :]

    def _e2p(self, x):
        """
        Convert Euclidean coordinates to projective coordinates
        Remarks:
            [x, y]    --> [x, y, 1]
            [x, y, z] --> [x, y, z, 1]
        Args:
            x (np.ndarray[n, 2 or 3]): euclidean coordinate
        Returns:
            np.ndarray[n, 3 or 4]: projective coordinate
        """

        assert(type(x) == np.ndarray)
        assert((x.shape[0] == 3) | (x.shape[0] == 2))
        return np.vstack((x, np.ones((1, x.shape[1]))))

    @abstractmethod
    def world2image(self, x):
        pass

    @abstractmethod
    def scale(self, x):
        pass

    @abstractmethod
    def setup(self, x):
        pass


