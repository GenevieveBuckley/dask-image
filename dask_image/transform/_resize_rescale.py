import dask.array as da
from dask.array.overlap import coerce_depth, coerce_boundary, trim_internal
import numpy as np
import skimage.transform

from . import _utils


@_utils._update_wrapper(skimage.transform.rescale)
def rescale(image,
            scale,
            order=1,
            mode='reflect',
            cval=0,
            clip=True,
            preserve_range=False,
            multichannel=False,
            anti_aliasing=True,
            anti_aliasing_sigma=None,
            depth=10,
            **kwargs):
    chunks = ((np.array(image.chunksize) + (2*depth)) * scale).astype(int)
    result = da.map_overlap(image,
                            skimage.transform.rescale,
                            scale=scale,
                            depth=depth,
                            boundary='reflect',
                            dtype=float,
                            chunks=chunks,
                            trim=False,
                            **kwargs)
    depth2 = coerce_depth(image.ndim, int(depth * scale))
    boundary2 = coerce_boundary(image.ndim, boundary=None)
    result = trim_internal(result, depth2, boundary2)
    return result
