import spiceypy as spice
import spiceypy.utils.support_types as stypes
import pytest
import ctypes
import numpy as np
import numpy.testing as npt
import array


def test_SpiceEllipse():
    viewpt = [2.0, 0.0, 0.0]
    limb = spice.edlimb(np.sqrt(2), 2.0 * np.sqrt(2), np.sqrt(2), viewpt)
    expectedSMinor = [0.0, 0.0, -1.0]
    expectedSMajor = [0.0, 2.0, 0.0]
    expectedCenter = [1.0, 0.0, 0.0]
    npt.assert_array_almost_equal(limb.center, expectedCenter)
    npt.assert_array_almost_equal(limb.semi_major, expectedSMajor)
    npt.assert_array_almost_equal(limb.semi_minor, expectedSMinor)
    assert str(limb).startswith("<SpiceEllipse")


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
