import numpy as np
from numpy.testing import assert_allclose
import matplotlib.pyplot as plt

from ..bbox import BBox


class TestBBoxTransform(object):

    def setup_method(self, method):
        self.bbox = BBox(center=(300, 200), width=200, height=50, theta=0)
        self.tr = self.bbox.transform

    def test_raw_display_unrotated(self):
        corners = np.array([(0., 0.), (1., 0.), (1., 1.), (0., 1.)])
        result = self.tr.transform(corners)
        assert_allclose(result, [(200, 175), (400, 175), (400., 225), (200., 225)])

    def test_raw_display_rotate(self):
        # this tests that self.tr auto-updates after a rotation
        self.bbox.theta = 30.
        corners = np.array([(0., 0.), (1., 0.), (1., 1.), (0., 1.)])
        result = self.tr.transform(corners)
        assert_allclose(result, [[ 225.89745962,  128.34936491],
                                 [ 399.10254038,  228.34936491],
                                 [ 374.10254038,  271.65063509],
                                 [ 200.89745962,  171.65063509]])

    def test_tie_to_axes(self):

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_axes([0.25, 0.4, 0.5, 0.4])

        self.bbox.tie_to_axes(ax)

        corners = np.array([(0., 0.), (1., 0.), (1., 1.), (0., 1.)])
        result = self.tr.transform(corners)
        assert_allclose(result, [(200, 175), (400, 175), (400., 225), (200., 225)])

        ax.set_xlim(0., 2.)
        ax.set_ylim(-5., 5.)

        corners = np.array([(0., 0.), (1., 0.), (1., 1.), (0., 1.)])
        result = self.tr.transform(corners)
        assert_allclose(result, [(200, 465.5), (300, 465.5), (300., 470.5), (200., 470.5)])
