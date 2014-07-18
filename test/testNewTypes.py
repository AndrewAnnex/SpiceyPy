import SpiceyPy as spice
import numpy as np

a = spice.stypes.toDoubleVector([1.0, 2, 3])
print(a)
b = spice.stypes.toDoubleVector((1.0, 2, 3))
print(b)
c = spice.stypes.toDoubleVector(np.array([1.0, 2, 3]))
print(c)
d = spice.stypes.toDoubleVector(np.array([1, 2, 3]))
print(d)
e = spice.stypes.toIntVector(np.array([1, 2, 3]))
print(e)
f = spice.stypes.toIntVector((1, 2, 3))
print(f)

g = spice.stypes.listtodoublematrix([[1.0, 2], [3, 4.0]], x=2, y=2)
print("g", g)

h = spice.stypes.toDoubleMatrix([[1.0, 2, 3], [3, 4.0, 3]])
print(h)

i = spice.stypes.toDoubleMatrix(np.array([[1, 2, 3.0], [4, 5, 6], [7, 8, 9]]))
print(i)

j = spice.stypes.toDoubleMatrix(np.matrix([[1, 2, 3.0], [4, 5, 6], [7, 8, 9]]))
print(j)
