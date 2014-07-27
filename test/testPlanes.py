__author__ = 'Apollo117'
import SpiceyPy as spice

testplane = spice.stypes.Plane(tuple([1.0, 20.0, 1.0]), 4.0)
print(testplane)
print(testplane.normal)
print(testplane.constant)
print(spice.pl2nvc(testplane))
print(spice.stypes.Plane())
plane = spice.nvc2pl([1.0, 1.0, 1.0], 23.0)
print(plane)