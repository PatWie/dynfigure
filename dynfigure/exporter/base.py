#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>


from abc import abstractmethod, ABCMeta
import six

__all__ = ['get_exporter_context', 'Base']
_ExportSystemStack = []


def get_exporter_context():
    global _ExportSystemStack
    if len(_ExportSystemStack) > 0:
        return _ExportSystemStack[-1]
    else:
        return None
        # raise Exception('no exporter in current context')


@six.add_metaclass(ABCMeta)
class Base(object):
    """docstring for Base"""

    def __init__(self, fn, fps=30, height=1080, width=1920, skip=False):
        super(Base, self).__init__()
        self._fn = fn
        self._fps = fps
        self._height = height
        self._width = width
        self.skip = skip

    @property
    def fps(self):
        return self._fps

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @abstractmethod
    def add_frame(self, frame, length=1):
        pass

    def __enter__(self):
        global _ExportSystemStack
        _ExportSystemStack.append(self)
        return self._enter()

    @abstractmethod
    def _enter(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _ExportSystemStack
        del _ExportSystemStack[-1]
        self._exit(exc_type, exc_val, exc_tb)

    @abstractmethod
    def _exit(self):
        pass