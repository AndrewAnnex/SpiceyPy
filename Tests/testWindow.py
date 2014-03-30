__author__ = 'Apollo117'

import SpiceyPy as spice

a = spice.stypes.SpiceCell.double(6)
b = spice.stypes.SpiceCell.double(6)

spice.appndd(1.0, a)
spice.appndd(3.0, a)
spice.appndd(7.0, a)
spice.appndd(11.0, a)
spice.appndd(23.0, a)
spice.appndd(27.0, a)

spice.appndd(2.0, b)
spice.appndd(4.0, b)
spice.appndd(8.0, b)
spice.appndd(10.0, b)
spice.appndd(16.0, b)
spice.appndd(18.0, b)

print([x for x in spice.wndifd(a, b)])
print(a[3])