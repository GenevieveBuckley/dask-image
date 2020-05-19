#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest

import numpy as np

import skimage.data
import skimage.transform

import dask.array as da

import dask_image.transform


@pytest.mark.parametrize(
    "numpy_image, chunks, scale, rgb",
    [
        (skimage.data.camera(), (256, 256), 2, False),
        (skimage.data.camera(), (256, 256), 0.5, False),
        (skimage.data.astronaut(), (256, 256, 3), 2, True),
        (skimage.data.astronaut(), (256, 256, 3), 0.5, True),
    ],
)
def test_rescale(numpy_image, chunks, scale, rgb):
    image = da.from_array(numpy_image, chunks=chunks)
    result = dask_image.transform.rescale(image, scale, multichannel=rgb)
    computed_result = result.compute()
    expected = skimage.transform.rescale(numpy_image, scale, multichannel=rgb)
    assert result.shape == expected.shape
    assert computed_result.shape == expected.shape
    assert np.allclose(computed_result.astype(int), expected.astype(int))
