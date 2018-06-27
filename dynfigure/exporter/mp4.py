#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Patrick Wieschollek <mail@patwie.com>

import subprocess as sp
from .base import Base


class Mp4(Base):
    def add_frame(self, frame, length=1):
        if frame is not None:
            for l in range(length):
                self._writing_process.stdin.write(frame.tobytes())

    def _enter(self):
        print('writing to %s' % self._fn)

        # stolen from https://github.com/3b1b/manim/blob/be69bf3c8af1b1904449c99eee3c76557f3ee2dc/scene/scene.py#L594
        command = [
            'ffmpeg',
            '-y',  # overwrite output file if it exists
            '-f', 'rawvideo',
            '-s', '%dx%d' % (self._width, self._height),  # size of one frame
            '-pix_fmt', 'rgba',
            '-r', str(self._fps),  # frames per second
            '-i', '-',  # The imput comes from a pipe
            '-an',  # Tells FFMPEG not to expect any audio
            '-loglevel', 'error',
        ]

        command += [
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
        ]

        command += [self._fn]

        self._writing_process = sp.Popen(command, stdin=sp.PIPE)
        return self

    def _exit(self, exc_type, exc_val, exc_tb):
        self._writing_process.stdin.close()
        self._writing_process.wait()
