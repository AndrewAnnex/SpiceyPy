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

import spiceypy as spice
import spiceypy.utils.support_types as stypes
import pytest
import ctypes
import numpy as np
import numpy.testing as npt
import array


def test_SpiceEllipse():
    spice.kclear()
    spice.reset()
    viewpt = [2.0, 0.0, 0.0]
    limb = spice.edlimb(np.sqrt(2), 2.0 * np.sqrt(2), np.sqrt(2), viewpt)
    expected_s_minor = [0.0, 0.0, -1.0]
    expected_s_major = [0.0, 2.0, 0.0]
    expectedCenter = [1.0, 0.0, 0.0]
    npt.assert_array_almost_equal(limb.center, expectedCenter)
    npt.assert_array_almost_equal(limb.semi_major, expected_s_major)
    npt.assert_array_almost_equal(limb.semi_minor, expected_s_minor)
    assert str(limb).startswith("<SpiceEllipse")
    spice.reset()
    spice.kclear()


def test_SpicePlane():
    norm = [0.0, 0.0, 1.0]
    orig = [0.0, 0.0, 0.0]
    plane = spice.nvp2pl(norm, orig)
    npt.assert_array_almost_equal(plane.normal, norm)
    assert plane.constant == 0.0
    assert str(plane).startswith("<SpicePlane")


def test_SpiceCell():
    test_cell = stypes.SPICEINT_CELL(8)
    spice.appndi(1, test_cell)
    spice.appndi(2, test_cell)
    spice.appndi(3, test_cell)
    assert [x for x in test_cell] == [1, 2, 3]
    assert len(test_cell) == 3
    assert 1 in test_cell
    assert 2 in test_cell
    assert 3 in test_cell
    assert 4 not in test_cell
    with pytest.raises(TypeError):
        test_cell.__getitem__("a")
    with pytest.raises(IndexError):
        test_cell.__getitem__(3)
    assert str(test_cell).startswith("<SpiceCell")


def test_spicecell_equality():
    c1 = stypes.Cell_Int(8)
    spice.appndi([1, 2, 3], c1)
    c2 = stypes.Cell_Int(8)
    spice.appndi([1, 2, 3], c2)
    c3 = stypes.Cell_Int(8)
    spice.appndi([1, 2, 4], c3)
    c4 = stypes.Cell_Int(8)
    spice.appndi([1, 2, 3, 3], c4)
    assert c1 != 1
    assert c1 == c2
    assert c1 != c3
    c3 = spice.valid(3, 3, c3)
    assert c3.isSet
    assert not c4.isSet
    assert c1 != c4


def test_empty_spice_cell_slicing():
    test_cell = stypes.SPICEDOUBLE_CELL(1)
    assert test_cell[0:1] == []


def test_numpy_and_strings():
    s = np.array(["3/0597205898.09324"])[0]
    sc = stypes.string_to_char_p(s)
    assert stypes.to_python_string(sc)


def test_SpiceCellSliceInts():
    test_vals = [1, 2, 3]
    test_cell = stypes.SPICEINT_CELL(5)
    spice.appndi(test_vals, test_cell)
    assert test_cell[0] == test_vals[0]
    assert test_cell[1] == test_vals[1]
    assert test_cell[2] == test_vals[2]
    assert test_cell[-1] == test_vals[-1]
    assert test_cell[-2] == test_vals[-2]
    assert test_cell[-3] == test_vals[-3]
    assert test_cell[0:1] == test_vals[0:1]
    assert test_cell[1:2] == test_vals[1:2]
    assert test_cell[2:3] == test_vals[2:3]
    assert test_cell[0:2] == test_vals[0:2]
    assert test_cell[0:3] == test_vals[0:3]
    assert test_cell[0:5] == test_vals[0:5]
    assert test_cell[::2] == test_vals[::2]
    assert test_cell[5:10] == test_vals[5:10]
    assert test_cell[::-1] == test_vals[::-1]
    assert test_cell[::-2] == test_vals[::-2]
    assert test_cell[2:-1] == test_vals[2:-1]


def test_to_double_vector():
    made_from_list = stypes.to_double_vector([1.0, 2.0, 3.0])
    assert len(made_from_list) == 3
    made_from_tuple = stypes.to_double_vector((1.0, 2.0, 3.0))
    assert len(made_from_tuple) == 3
    made_from_numpy_array = stypes.to_double_vector(np.array([1.0, 2.0, 3.0]))
    assert len(made_from_numpy_array) == 3
    made_from_python_array = stypes.to_double_vector(array.array("d", [1.0, 2.0, 3.0]))
    assert len(made_from_python_array) == 3
    test_array3 = ctypes.c_double * 3
    made_from_ctypes_array = stypes.to_double_vector(test_array3(1.0, 2.0, 3.0))
    assert len(made_from_ctypes_array) == 3
    with pytest.raises(TypeError):
        stypes.to_double_vector("ABCD")
    with pytest.raises(TypeError):
        stypes.to_double_vector(array.array("i", [1, 2, 3]))


def test_to_int_vector():
    made_from_list = stypes.to_int_vector([1, 2, 3])
    assert len(made_from_list) == 3
    made_from_tuple = stypes.to_int_vector((1, 2, 3))
    assert len(made_from_tuple) == 3
    made_from_numpy_array = stypes.to_int_vector(np.array([1, 2, 3]))
    assert len(made_from_numpy_array) == 3
    made_from_python_array = stypes.to_int_vector(array.array("i", [1, 2, 3]))
    assert len(made_from_python_array) == 3
    test_array3 = ctypes.c_int * 3
    made_from_ctypes_array = stypes.to_int_vector(test_array3(1, 2, 3))
    assert len(made_from_ctypes_array) == 3
    with pytest.raises(TypeError):
        stypes.to_int_vector("ABCD")
    with pytest.raises(TypeError):
        stypes.to_int_vector(array.array("d", [1.0, 2.0, 3.0]))


def test_to_double_matrix():
    made_from_list = stypes.to_double_matrix([[1.0, 2.0], [3.0, 4.0]])
    assert len(made_from_list) == 2
    made_from_tuple = stypes.to_double_matrix(((1.0, 2.0), (3.0, 4.0)))
    assert len(made_from_tuple) == 2
    made_from_numpy_array = stypes.to_double_matrix(np.array([[1.0, 2.0], [3.0, 4.0]]))
    assert len(made_from_numpy_array) == 2
    with pytest.raises(TypeError):
        stypes.to_double_matrix("ABCD")


def test_to_int_matrix():
    made_from_list = stypes.to_int_matrix([[1, 2], [3, 4]])
    assert len(made_from_list) == 2
    made_from_tuple = stypes.to_int_matrix(((1, 2), (3, 4)))
    assert len(made_from_tuple) == 2
    made_from_numpy_array = stypes.to_int_matrix(np.array([[1, 2], [3, 4]]))
    assert len(made_from_numpy_array) == 2
    with pytest.raises(TypeError):
        stypes.to_int_matrix("ABCD")
    with pytest.raises(TypeError):
        stypes.to_int_matrix([[1.0, 2.0], [3.0, 4.0]])


def test_to_improve_coverage():
    # SpiceyError().__str__()
    xsept = spice.stypes.SpiceyError("abc")
    assert xsept.short == "abc"
    # stypes.empty_char_array when missing keyword arguments
    eca = stypes.empty_char_array()
    # stypes.empty_double_matrix and stypes.empty_int_matrix when x is c_int
    edm = stypes.empty_double_matrix(x=ctypes.c_int(4))
    eim = stypes.empty_int_matrix(x=ctypes.c_int(4))
    # stypes.*MatrixType().from_param(param) when isinstance(param,Array)
    for stmt, typ in zip(
        (
            stypes.DoubleMatrixType(),
            stypes.IntMatrixType(),
        ),
        (
            float,
            int,
        ),
    ):
        made_from_list = stmt.from_param(
            [[typ(1), typ(2), typ(3)], [typ(6), typ(4), typ(0)]]
        )
        assert made_from_list == stmt.from_param(made_from_list)
    # DataType.__init__()
    assert stypes.DataType()
    # SpiceDLADescr methods
    stsdlad = stypes.SpiceDLADescr()
    assert isinstance(stsdlad.bwdptr, int)
    assert isinstance(stsdlad.fwdptr, int)
    assert isinstance(stsdlad.ibase, int)
    assert isinstance(stsdlad.isize, int)
    assert isinstance(stsdlad.dbase, int)
    assert isinstance(stsdlad.cbase, int)
    assert isinstance(stsdlad.csize, int)
    # __str__ methods in multiple classes
    for obj in (
        stypes.SpiceEKAttDsc(),
        stypes.SpiceEKSegSum(),
        stypes.empty_spice_ek_expr_class_vector(1),
        stypes.empty_spice_ek_data_type_vector(1),
        stypes.empty_spice_ek_expr_class_vector(ctypes.c_int(1)),
        stypes.empty_spice_ek_data_type_vector(ctypes.c_int(1)),
    ):
        assert type(obj.__str__()) is str
    # SpiceCell methods:  .is_time; .is_bool; .reset.
    stsct = stypes.SPICETIME_CELL(10)
    assert stsct.is_time()
    stscb = stypes.SPICEBOOL_CELL(10)
    assert stscb.is_bool()
    stsct2 = stypes.Cell_Time(10)
    assert stsct2.is_time()
    stscb2 = stypes.Cell_Bool(10)
    assert stscb2.is_bool()
    assert stscb.reset() is None


def test_Cell_Double_empty():
    cell = stypes.Cell_Double(1)
    assert isinstance(cell, stypes.Cell_Double)
    assert isinstance(cell, stypes.SpiceCell)
    assert cell[0:1] == []


def test_Cell_Double():
    cell = stypes.Cell_Double(8)
    spice.appndd(1.1, cell)
    spice.appndd(2.2, cell)
    spice.appndd(3.3, cell)
    assert [x for x in cell] == [1.1, 2.2, 3.3]


def test_Cell_Int_empty():
    cell = stypes.Cell_Int(1)
    assert isinstance(cell, stypes.Cell_Int)
    assert isinstance(cell, stypes.SpiceCell)
    assert cell[0:1] == []


def test_Cell_Int():
    cell = stypes.Cell_Int(8)
    spice.appndi(1, cell)
    spice.appndi(2, cell)
    spice.appndi(3, cell)
    assert [x for x in cell] == [1, 2, 3]


def test_Cell_Char():
    test_cell = stypes.Cell_Char(10, 10)
    spice.appndc("one", test_cell)
    spice.appndc("two", test_cell)
    spice.appndc("three", test_cell)
    assert test_cell[0] == "one"
    assert test_cell[1] == "two"
    assert test_cell[2] == "three"


def test_cell_equality():
    cell = stypes.Cell_Int(8)
    assert cell == []
    spice.appndi(1, cell)
    spice.appndi(2, cell)
    spice.appndi(3, cell)
    assert not cell == []
    assert not cell == [1]
    assert not cell == [1, 2]
    assert cell == [1, 2, 3]
    assert not cell == [1, 2, 3, 4]
    celld = stypes.Cell_Double(8)
    spice.appndd(1.1, celld)
    spice.appndd(2.2, celld)
    spice.appndd(3.3, celld)
    assert celld == [1.1, 2.2, 3.3]
    assert not celld == cell
