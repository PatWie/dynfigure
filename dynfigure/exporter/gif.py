#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

import subprocess as sp
from .base import Base
import uuid
import os
import shutil


class Gif(Base):

    def __init__(self, fn, fps=30, height=1080, width=1920):
        super(Base, self).__init__()
        self._fn = fn
        self._fps = fps
        self._height = height
        self._width = width
        self.uuid = uuid.uuid4().hex

    def add_frame(self, frame, length=1):

        if frame is not None:

            assert self._height == frame.height
            assert self._width == frame.width

            for l in range(length):
                frame_fn = os.path.join(self.tmp_dir, 'frame%010i.png' % self.counter)
                self.counter += 1
                self.frame_png_names.append(frame_fn)
                frame.save(frame_fn)

    def _enter(self):
        print('writing to %s' % self._fn)

        self.tmp_dir = os.path.join('/tmp', self.uuid)
        self.frame_png_names = []
        self.counter = 0
        os.mkdir(self.tmp_dir)

        return self

    def _exit(self, exc_type, exc_val, exc_tb):

        command = [
            'convert',
            '-delay',
            str(100. / self._fps),
            '-loop',
            '0',
            os.path.join(self.tmp_dir, '*.png'),
            self._fn
        ]
        pipe = sp.Popen(command, stdin=sp.PIPE)
        pipe.stdin.close()
        pipe.wait()

        shutil.rmtree(self.tmp_dir)
