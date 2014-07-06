__author__ = 'Apollo117'
import SpiceyPy as spice
import ctypes


def listtocharvector(x):
    assert (isinstance(x, list))
    return (ctypes.c_char_p * len(x))(*[strtocharpoint(y) for y in x])


def strtocharpoint(x, inlen=None):
    if inlen and isinstance(x, str):
        return ctypes.create_string_buffer(x.encode(encoding='UTF-8'), inlen)
    if isinstance(x, bytes):
        return x
    if isinstance(x, ctypes.c_int):
        return strtocharpoint(" " * x.value)
    if isinstance(x, int):
        return strtocharpoint(" " * x)
    return ctypes.c_char_p(x.encode(encoding='UTF-8'))


def listtosmartcharvector(inList, x, y):
    return ((ctypes.c_char*x)*y)(*[ctypes.create_string_buffer(string.encode(encoding='UTF-8'), x) for string in inList])


def smartercharvector(inList, x, y):
    assert (isinstance(inList, list))
    return ((ctypes.c_char*x)*y)(*[strtocharpoint(l, inlen=x) for l in inList])


def listToCharArray(inList, xLen=None, yLen=None):
    assert (isinstance(inList, list))
    if not yLen:
        yLen = len(inList)
    if not xLen:
        xLen = max(len(s) for s in inList)
    return ((ctypes.c_char*xLen)*yLen)(*[strtocharpoint(l, inlen=xLen) for l in inList])


def listToCharArrayPtr(inList):
    assert (isinstance(inList, list))
    yLen = len(inList)
    xLen = max(len(s) for s in inList)
    return ctypes.cast(((ctypes.c_char*xLen)*yLen)(*[strtocharpoint(l, inlen=xLen) for l in inList]), ctypes.c_char_p)


print("Test BSRCHC")
testCharArray = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
array = listtocharvector(testCharArray)
array2 = listtosmartcharvector(testCharArray, 10, 5)
string1 = strtocharpoint("BOHR", inlen=10)
array3 = smartercharvector(testCharArray, 10, 5)
array4 = listToCharArray(testCharArray)
array5 = listToCharArrayPtr(testCharArray)
print(array)
print(array2)
print(string1)
print(array3)
print(array4)
print(array5)
print(ctypes.cast(array4, ctypes.c_char_p))
print(strtocharpoint(10))
value = strtocharpoint("GALILEO")
ndim = ctypes.c_int(5)
lenvals = ctypes.c_int(10)
print("Old way: ")
print(spice.libspice.bsrchc_c(value, ndim, lenvals, array))
print("New way: ")
spice.libspice.bsrchc_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
print(spice.libspice.bsrchc_c(value, ndim, lenvals, ctypes.cast(array2, ctypes.c_char_p)))
print(spice.libspice.bsrchc_c(value, ndim, ctypes.c_int(8), ctypes.cast(array4, ctypes.c_char_p)))
print(spice.libspice.bsrchc_c(value, ndim, ctypes.c_int(8), array5))