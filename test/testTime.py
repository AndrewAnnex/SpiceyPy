__author__ = 'Apollo117'
import SpiceyPy as spice
import os

cwd = os.path.realpath(os.path.dirname(__file__))
_testKernelPath = cwd + "/testKernels.txt"
spice.furnsh(_testKernelPath)
et = -527644192.5403653
output = spice.et2utc(et, "J", 6, 35)
print(output)
spice.kclear()