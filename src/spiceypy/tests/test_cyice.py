import pytest
from spiceypy.cyice.cyice import cyice


def test_b1900():
    assert cyice.b1900() == 2415020.31352
