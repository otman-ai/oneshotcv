import numpy as np
import pytest


@pytest.fixture
def image():
    """A plain mid-gray BGR image."""
    return np.full((240, 320, 3), 127, dtype=np.uint8)


@pytest.fixture
def mask():
    """A rectangular mask matching the ``image`` fixture size."""
    m = np.zeros((240, 320), dtype=np.uint8)
    m[60:180, 80:240] = 255
    return m
