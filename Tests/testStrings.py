__author__ = 'Apollo117'
import SpiceyPy as spice

print(spice.ucase("This is an example", len("This is an example")+1))

#print(spice.utc2et("Tue Aug  6 11:10:57  1996"))
print(spice.tkvrsn("TOOLKIT"))

exList = ["all","casr","bot"]

print(spice.orderc(3, exList, 3))

print(spice.pos("AN ANT AND AN ELEPHANT        ", "AN", 9))