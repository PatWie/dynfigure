#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

from contextlib import contextmanager
from collections import defaultdict
import copy

__all__ = ['Scope', 'get_scope']

_ScopeStack = []


@contextmanager
def Scope(elements, **kwargs):
    if not isinstance(elements, list):
        elements = [elements]

    new_scope = copy.copy(get_scope())
    for l in elements:
        new_scope[l.__name__].update(kwargs)
    _ScopeStack.append(new_scope)
    yield
    del _ScopeStack[-1]


def get_scope():
    if len(_ScopeStack) > 0:
        return _ScopeStack[-1]
    else:
        return defaultdict(dict)
