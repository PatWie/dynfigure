#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from abc import abstractmethod, ABCMeta
import six
from functools import wraps
import copy
import uuid

from ..scope import get_scope
from ..coordinate_system import get_coordinate_system


@six.add_metaclass(ABCMeta)
class BaseElement(object):
    """Represents an object which can be drawn in a scene

    Attributes:
        uuid (TYPE): Description
    """
    def default(self):
        self.csys = get_coordinate_system()
        self.uuid = uuid.uuid4().hex

    def dtype(self):
        return 'DynFigure.Element'

    def __str__(self):
        return '<DynFigure.Baselement>'

    def draw(self, camera):
        camera.draw(self)

    def this(self):
        return self


def element_register():
    """Allow usage of scopes to apply the same kargs to all elements within
       a scope

    Returns:
        TYPE: Description
    """
    def wrapper(cls):
        @wraps(cls)
        def wrapped_class(*args, **kwargs):
            actual_args = copy.copy(get_scope()[cls.__name__])
            actual_args.update(kwargs)
            outputs = cls(*args, **actual_args)
            return outputs

        return wrapped_class
    return wrapper
