import numpy as np

from matplotlib.transforms import Transform, Affine2D
from matplotlib.path import Path


class BBoxTransform(Transform):
    """
    A class to transform from the frame of reference of the bounding box to
    display coordinates.

    This is evaluated on-the-fly using the current bounding box and axes.

    Parameters
    ----------
    ax : `~matplotlib.axes.Axes`
        The Axes that the bounding box is being plotted into
    """

    input_dims = 2
    output_dims = 2
    is_separable = False

    def transform_path(self, path):
        """
        Transform a Matplotlib Path

        Parameters
        ----------
        path : :class:`~matplotlib.path.Path`
            The path to transform

        Returns
        -------
        path : :class:`~matplotlib.path.Path`
            The resulting path
        """
        return Path(self.transform(path.vertices), path.codes)

    transform_path_non_affine = transform_path

    def __init__(self, bbox):
        self._ax = None
        self.bbox = bbox
        self._frozen_ax_transform = None
        super(BBoxTransform, self).__init__()

    @property
    def bbox_to_raw_display(self):
        # TODO: this can be cached if the bbox parameters haven't changed
        tr = (Affine2D().scale(self.bbox.width, self.bbox.height)
                        .translate(-self.bbox.width * 0.5, -self.bbox.height * 0.5)
                        .rotate_deg(self.bbox.theta)
                        .translate(*self.bbox.center))
        return tr

    def tie_to_axes(self, ax):
        self._ax = ax
        self._frozen_ax_transform = self._ax.transData.frozen()

    def transform(self, coords):
        """
        Transform from bounding box coordinates to display coordinates.
        """

        # Transform to the original display coordinates
        tr = self.bbox_to_raw_display
        raw_display = tr.transform(coords)

        if self._ax is None:
            return raw_display
        else:
            tr = self._frozen_ax_transform.inverted() + self._ax.transData
            return tr.transform(raw_display)

    def inverted(self, coords):
        raise NotImplementedError("")
