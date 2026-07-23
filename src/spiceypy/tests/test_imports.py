"""
The MIT License (MIT)

Copyright (c) [2015-2025] [Andrew Annex]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import spiceypy


def test_all_names_are_importable():
    """
    A missing comma in __all__ silently concatenates two entries
    (e.g. "exceptions" "stypes" -> "exceptionsstypes"), which breaks
    `from spiceypy import *` at runtime.
    """
    missing = [name for name in spiceypy.__all__ if not hasattr(spiceypy, name)]
    assert not missing, f"__all__ entries not defined on spiceypy: {missing}"


def test_star_import():
    namespace = {}
    exec("from spiceypy import *", namespace)
    for name in spiceypy.__all__:
        assert name in namespace, f"{name} not bound by `from spiceypy import *`"


def test_all_has_no_duplicates():
    duplicates = sorted({n for n in spiceypy.__all__ if spiceypy.__all__.count(n) > 1})
    assert not duplicates, f"duplicate __all__ entries: {duplicates}"
