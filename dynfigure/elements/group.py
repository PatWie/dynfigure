#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from ..color import Color
from .base import BaseElement, element_register
from ..frame import Frame
from ..exporter import get_exporter_context
import copy


@element_register()
class Group(BaseElement):

    """docstring for Group"""
    def __init__(self):
        self.default()
        self.elements = []

    def put(self, elements):
        """Put drawable element into the scene

        Args:
            elements (Element): element to draw
        """

        if not isinstance(elements, list):
            elements = [elements]

        for element in elements:
            assert element.dtype() == 'DynFigure.Element', 'Group.put requires and element'
            self.elements.append(element)

    def remove(self, element):
        """Remove drawable element from the scene

        Args:
            element (Element): element to remove
        """
        for k, el in enumerate(self.elements):
            if el.uuid == element.uuid:
                del self.elements[k]
                break

    def find(self, element):
        """Return a reference to a drawable element from the scene

        Args:
            element (Element): element to find
        """
        for k, el in enumerate(self.elements):
            if el.uuid == element.uuid:
                return self.elements[k]

    def draw(self, camera, verbose=False):
        for element in self.elements:
            if verbose:
                print('draw %s' % element)
            element.draw(camera)
        camera.flush()

    def __str__(self):
        return '<DynFigure.Group:(%i)>' % len(self.elements)

    def bbox(self):
        bbox = None
        for element in self.elements:
            bbox = element.bbox().merge(bbox)
        return bbox

    def place(self, dummy):
        raise Exception('groups cannot be placed')

Scene = Group
# @element_register()
# class Scene(Group):
#     pass
#     # def render(self):
#     #     """Return rendered scene (handy shortcut)

#     #     Example:

#     #         f = Frame(height=1000, width=1000)
#     #         f.render(scene)

#     #         # same as (when in video context)
#     #         scene.render()

#     #     Returns:
#     #         TYPE: Description
#     #     """
#     #     ctx = get_exporter_context()
#     #     return Frame(height=ctx.height, width=ctx.width).render(self)
