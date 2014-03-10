__author__ = 'Apollo117'
import SpiceyPy as spice

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