# -*- coding: utf-8 -*-

import numpy as np
import scipy.ndimage.filters

from . import _utils
from ..utils._dispatcher import Dispatcher

dispatch_convolve = Dispatcher(name="dispatch_convolve")

@dispatch_convolve.register(np.ndarray)
def numpy_convolve():
    return scipy.ndimage.filters.convolve


@dispatch_convolve.register_lazy("cupy")
def register_cupy():
    import cupyx.scipy.ndimage

    @dispatch_convolve.register(cupy.ndarray)
    def cupy_convolve():
        return cupyx.scipy.ndimage.filters.convolve


@_utils._update_wrapper(scipy.ndimage.filters.convolve)
def convolve(image,
             weights,
             mode='reflect',
             cval=0.0,
             origin=0):
    origin = _utils._get_origin(weights.shape, origin)
    depth = _utils._get_depth(weights.shape, origin)
    depth, boundary = _utils._get_depth_boundary(image.ndim, depth, "none")

    result = image.map_overlap(
        dispatch_convolve(),
        depth=depth,
        boundary=boundary,
        dtype=image.dtype,
        weights=weights,
        mode=mode,
        cval=cval,
        origin=origin
    )

    return result


@_utils._update_wrapper(scipy.ndimage.filters.correlate)
def correlate(image,
              weights,
              mode='reflect',
              cval=0.0,
              origin=0):
    origin = _utils._get_origin(weights.shape, origin)
    depth = _utils._get_depth(weights.shape, origin)
    depth, boundary = _utils._get_depth_boundary(image.ndim, depth, "none")

    result = image.map_overlap(
        scipy.ndimage.filters.correlate,
        depth=depth,
        boundary=boundary,
        dtype=image.dtype,
        weights=weights,
        mode=mode,
        cval=cval,
        origin=origin
    )

    return result
