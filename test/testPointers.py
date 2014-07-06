__author__ = 'Apollo117'
import SpiceyPy as spice
import ctypes
testArray = [-11,0,22,750]


print(spice.bsrchi(-11, 4, testArray))
print(spice.bsrchi(22, 4, testArray))
print(spice.bsrchi(751, 4, testArray))
print(spice.bsrchi(750, 4, testArray))


testArray = [-11.0,0.0,22.0,750.0]

print(spice.bsrchd(-11.0, 4, testArray))
print(spice.bsrchd(22.0, 4, testArray))
print(spice.bsrchd(751.0, 4, testArray))
print(spice.bsrchd(750.0, 4, testArray))

print("Test BSRCHC")
testCharArray = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]

print([x for x in testCharArray])
print(spice.bsrchc("GALILEO", 5, 10, testCharArray))


print("Test lstltc: ")
print(spice.lstltc("NEWTON", 5, 10, testCharArray))
print(spice.lstltc("Galileo", 5, 10, testCharArray))
print(spice.lstltc("EINSTEIN", 5, 10, testCharArray))