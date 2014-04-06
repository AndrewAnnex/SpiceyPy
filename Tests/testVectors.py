__author__ = 'Apollo117'
import SpiceyPy as spice
import numpy as np
v1=[1.0, 2.0, 3.0]
v2=[4.0, 5.0, 6.0]

print(spice.vaddg(v1, v2, 3))

v1=[0.0, 1.0, 0.0]
v2=[1.0, 0.0, 0.0]

print(spice.vcrss(v1,v2))

v1 = [2.0, 3.0, 0.0]
v2 = [5.0, 7.0, 12.0]
print(spice.vdist(v1,v2))
print(spice.vdot(v1,v2))
print(spice.vdotg(v1,v2,3))
print(spice.vequ(v1))
print(spice.vequg(v1,3))

v1 = [5.0,12.0,0.0,1.0]
print(spice.vhat(v1[0:3]))
print(spice.vhatg(v1,4))
print(spice.vpack(1.0,2,3))
print(spice.vperp([6.0,6.0,6.0], [2.0, 0.0, 0.0]))
print(spice.vproj([6.0,6.0,6.0], [2.0, 0.0, 0.0]))


print("test rot vectors")
print(spice.vrotv([1.0,2.0,3.0], [0.0,0.0,1.0], spice.halfpi()))
print(spice.vrotv([1.0,0.0,0.0], [0.0,0.0,1.0], spice.halfpi()))
print(spice.vrotv([0.0,1.0,0.0], [0.0,0.0,1.0], spice.halfpi()))

print("Vupack test")
print(spice.vupack([1.0,2.0,3.0]))

print("Zeros test")
print(spice.vzero([0.0,0.0,1.0]))
print(spice.vzero([0.0,0.0,0.0]))

print("unorm test")
print(spice.unorm(np.array([5.0, 7.0, 12.0])))
print(spice.unormg(np.array([5.0, 7.0, 12.0, 2.0]), 4))
print(spice.unorm([5.0, 7.0, 12.0]))
print(spice.unormg([5.0, 7.0, 12.0, 2.0], 4))


print("order tests: ")
print(spice.orderi([3,1,4,2], 4))

print("Test sums: ")
print(spice.sumai([5, 7, 12], 3))

print("Test shell sort:")
print(spice.shelli(6, [99,33,55,44,-77,66]))
print(spice.shelld(6, [99.0,33,55,44,-77,66]))

print("Frame test: ")
print(spice.frame([1.0,2.0,1.0]))
print(spice.frame([0.0,0.0,0.0]))

print("Lstlti test: ")
print(spice.lstlti(1, 6, [-2,-2,0,1,1,11]))
print(spice.lstlti(-2, 6, [-2,-2,0,1,1,11]))
print(spice.lstlti(12, 6, [-2,-2,0,1,1,11]))

print("Orderi test: ")
print(spice.orderi([3,1,4,2], 4))
print(spice.orderi(np.array([3,1,4,2]), 4))

print("Reordi test: ")
print(spice.reordi([0, 2, 1], 3, [3, 2, 1]))
print(spice.reordi(np.asarray([0, 2, 1]), 3, np.asarray([3, 2, 1])))
print("Reordd test: ")
print(spice.reordd([0, 2, 1], 3, [3.5, 2.1, 1.9]))
print(spice.reordd(np.asarray([0, 2, 1]), 3, np.asarray([3.5, 2.1, 1.9])))
print("Reordl test: ")
print(spice.reordl([0, 2, 1], 3, [True, True, False]))
print(spice.reordl(np.array([0, 2, 1]), 3, np.array([True, True, False])))
