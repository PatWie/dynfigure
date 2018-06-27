import numpy as np
from .base import BaseCamera


class Camera2D(BaseCamera):
    """Very basic Camera which should considers 2D coordinates
    """
    def setup(self):
        self.__T = np.array([[1., 0, self.pc[0]],
                             [0, -1., self.pc[1]],
                             [0, 0, 1.]])

    def scale(self, x):
        return x

    def world2image(self, x):
        x = np.array(x).T
        # only supports 2D coordinates
        assert(x.shape[0] == 2)

        x = x.reshape(2, -1)
        x = self._e2p(x)
        x = np.matmul(self.__T, x)

        return self._p2e(x).T

