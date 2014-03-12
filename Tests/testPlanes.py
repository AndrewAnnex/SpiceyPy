__author__ = 'Apollo117'
import SpiceyPy as spice

testplane = spice.stypes.Plane(tuple([1.0, 20.0, 1.0]), 4.0)
print(testplane)
print(spice.pl2nvc(testplane))