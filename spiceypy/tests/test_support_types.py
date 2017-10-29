"""
The MIT License (MIT)

Copyright (c) [2015-2017] [Andrew Annex]

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
    expectedSMinor = [0.0, 0.0, -1.0]
    expectedSMajor = [0.0, 2.0, 0.0]
    expectedCenter = [1.0, 0.0, 0.0]
    npt.assert_array_almost_equal(limb.center, expectedCenter)
    npt.assert_array_almost_equal(limb.semi_major, expectedSMajor)
    npt.assert_array_almost_equal(limb.semi_minor, expectedSMinor)
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
    testCell = stypes.SPICEINT_CELL(8)
    spice.appndi(1, testCell)
    spice.appndi(2, testCell)
    spice.appndi(3, testCell)
    assert [x for x in testCell] == [1, 2, 3]
    assert len(testCell) == 3
    assert 1 in testCell
    assert 2 in testCell
    assert 3 in testCell
    assert 4 not in testCell
    with pytest.raises(TypeError):
        testCell.__getitem__('a')
    with pytest.raises(IndexError):
        testCell.__getitem__(3)
    assert str(testCell).startswith("<SpiceCell")


def test_EmptySpiceCellSlicing():
    testCell = stypes.SPICEDOUBLE_CELL(1)
    assert testCell[0:1] == []


def test_SpiceCellSliceInts():
    testVals = [1, 2, 3]
    testCell = stypes.SPICEINT_CELL(5)
    spice.appndi(testVals, testCell)
    assert testCell[0] == testVals[0]
    assert testCell[1] == testVals[1]
    assert testCell[2] == testVals[2]
    assert testCell[-1] == testVals[-1]
    assert testCell[-2] == testVals[-2]
    assert testCell[-3] == testVals[-3]
    assert testCell[0:1] == testVals[0:1]
    assert testCell[1:2] == testVals[1:2]
    assert testCell[2:3] == testVals[2:3]
    assert testCell[0:2] == testVals[0:2]
    assert testCell[0:3] == testVals[0:3]
    assert testCell[0:5] == testVals[0:5]
    assert testCell[::2] == testVals[::2]
    assert testCell[5:10] == testVals[5:10]
    assert testCell[::-1] == testVals[::-1]
    assert testCell[::-2] == testVals[::-2]
    assert testCell[2:-1] == testVals[2:-1]


def test_toBoolVector():
    madeFromList = stypes.toBoolVector([False, True, False])
    assert len(madeFromList) == 3
    madeFromTuple = stypes.toBoolVector((False, True, False))
    assert len(madeFromTuple) == 3
    madeFromNumpyArray = stypes.toBoolVector(np.ones((3, 1), dtype=bool))
    assert len(madeFromNumpyArray) == 3
    TestArray3 = ctypes.c_bool * 3
    madeFromCtypesArray = stypes.toBoolVector(TestArray3(False, True, False))
    assert len(madeFromCtypesArray) == 3
    with pytest.raises(TypeError):
        stypes.toBoolVector("ABCD")
    spice.kclear()


def test_toDoubleVector():
    madeFromList = stypes.toDoubleVector([1.0, 2.0, 3.0])
    assert len(madeFromList) == 3
    madeFromTuple = stypes.toDoubleVector((1.0, 2.0, 3.0))
    assert len(madeFromTuple) == 3
    madeFromNumpyArray = stypes.toDoubleVector(np.array([1.0, 2.0, 3.0]))
    assert len(madeFromNumpyArray) == 3
    madeFromPythonArray = stypes.toDoubleVector(array.array('d', [1.0, 2.0, 3.0]))
    assert len(madeFromPythonArray) == 3
    TestArray3 = ctypes.c_double * 3
    madeFromCtypesArray = stypes.toDoubleVector(TestArray3(1.0, 2.0, 3.0))
    assert len(madeFromCtypesArray) == 3
    with pytest.raises(TypeError):
        stypes.toDoubleVector("ABCD")
    with pytest.raises(TypeError):
        stypes.toDoubleVector(array.array('i', [1, 2, 3]))


def test_toIntVector():
    madeFromList = stypes.toIntVector([1, 2, 3])
    assert len(madeFromList) == 3
    madeFromTuple = stypes.toIntVector((1, 2, 3))
    assert len(madeFromTuple) == 3
    madeFromNumpyArray = stypes.toIntVector(np.array([1, 2, 3]))
    assert len(madeFromNumpyArray) == 3
    madeFromPythonArray = stypes.toIntVector(array.array('i', [1, 2, 3]))
    assert len(madeFromPythonArray) == 3
    TestArray3 = ctypes.c_int * 3
    madeFromCtypesArray = stypes.toIntVector(TestArray3(1, 2, 3))
    assert len(madeFromCtypesArray) == 3
    with pytest.raises(TypeError):
        stypes.toIntVector("ABCD")
    with pytest.raises(TypeError):
        stypes.toIntVector(array.array('d', [1.0, 2.0, 3.0]))


def test_toDoubleMatrix():
    madeFromList = stypes.toDoubleMatrix([[1.0, 2.0], [3.0, 4.0]])
    assert len(madeFromList) == 2
    madeFromTuple = stypes.toDoubleMatrix(((1.0, 2.0), (3.0, 4.0)))
    assert len(madeFromTuple) == 2
    madeFromNumpyArray = stypes.toDoubleMatrix(np.array([[1.0, 2.0], [3.0, 4.0]]))
    assert len(madeFromNumpyArray) == 2
    madeFromNumpyMatrix = stypes.toDoubleMatrix(np.matrix([[1.0, 2.0], [3.0, 4.0]]))
    assert len(madeFromNumpyMatrix) == 2
    with pytest.raises(TypeError):
        stypes.toDoubleMatrix("ABCD")


def test_toIntMatrix():
    madeFromList = stypes.toIntMatrix([[1, 2], [3, 4]])
    assert len(madeFromList) == 2
    madeFromTuple = stypes.toIntMatrix(((1, 2), (3, 4)))
    assert len(madeFromTuple) == 2
    madeFromNumpyArray = stypes.toIntMatrix(np.array([[1, 2], [3, 4]]))
    assert len(madeFromNumpyArray) == 2
    madeFromNumpyMatrix = stypes.toIntMatrix(np.matrix([[1, 2], [3, 4]]))
    assert len(madeFromNumpyMatrix) == 2
    with pytest.raises(TypeError):
        stypes.toIntMatrix("ABCD")
    with pytest.raises(TypeError):
        stypes.toIntMatrix([[1.0, 2.0], [3.0, 4.0]])


def test_to_improve_coverage():
    # SpiceyError().__str__()
    xsept = spice.stypes.SpiceyError('abc')
    assert str(xsept) == 'abc'
    # stypes.emptyCharArray when missing keyword arguments
    eca = stypes.emptyCharArray()
    # stypes.emptyDoubleMatrix and stypes.emptyIntMatrix when x is c_int
    edm = stypes.emptyDoubleMatrix(x=ctypes.c_int(4))
    eim = stypes.emptyIntMatrix(x=ctypes.c_int(4))
    # stypes.*MatrixType().from_param(param) when isinstance(param,Array)
    for stmt,typ in zip((stypes.DoubleMatrixType(), stypes.IntMatrixType(),),
                        (float, int,)):
        madeFromList = stmt.from_param([[typ(1),typ(2),typ(3)],[typ(6),typ(4),typ(0)]])
        assert madeFromList is stmt.from_param(madeFromList)
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
    for obj in (stypes.SpiceEKAttDsc(), stypes.SpiceEKSegSum(), stypes.emptySpiceEKExprClassVector(1),
                stypes.emptySpiceEKDataTypeVector(1), stypes.emptySpiceEKExprClassVector(ctypes.c_int(1)), stypes.emptySpiceEKDataTypeVector(ctypes.c_int(1))):
        assert type(obj.__str__()) is str
    # SpiceCell methods:  .is_time; .is_bool; .reset.
    stsct = stypes.SPICETIME_CELL(10)
    assert stsct.is_time()
    stscb = stypes.SPICEBOOL_CELL(10)
    assert stscb.is_bool()
    assert stscb.reset() is None
