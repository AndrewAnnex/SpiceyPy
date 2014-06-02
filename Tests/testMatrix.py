__author__ = 'Apollo117'
import SpiceyPy as spice
import numpy as np
m1 =[[1.0,2.0,3.0],[0.0,4.0,5.0],[0.0,6.0,0.0]]
m2 =[[1.0,0.0,0.0],[2.0,4.0,6.0],[3.0,5.0,0.0]]
print("xpose: ", spice.xpose(m1))
print("xpose: ", spice.xpose(m2))
print("xposeg: ", spice.xposeg(m1, 3, 3))


m1 = [[0.0,0.0],[0.0,1.0],[0.0,2.0]]
print("xposeg: ", spice.xposeg(m1, 3, 2))


m1 = [[1.0,1.0,1.0],[2.0,3.0,4.0]]
v2 = [1.0,2.0,3.0]
print(spice.mxvg(m1, v2, 2, 3))

m1 = [[1.0,2.0,3.0],[3.0,2.0,1.0]]
m2 = [[1.0,2.0,0.0],[2.0,1.0,2.0],[1.0,2.0,0.0],[2.0,1.0,2.0]]
print(spice.mxmtg(m1, m2, 2, 3, 4))

m1 = [[1.0,4.0],[2.0,5.0],[3.0,6.0]]
m2 = [[1.0, 3.0, 5.0],[2.0,4.0,6.0]]

print(spice.mxmg(m1, m2, 3,2,3))
m1 = [[1.0,2.0],[1.0,3.0],[1.0,4.0]]
v2 = [1.0,2.0,3.0]
print(spice.mtxvg(m1, v2, 2, 3))