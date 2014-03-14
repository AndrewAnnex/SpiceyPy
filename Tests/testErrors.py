__author__ = 'Apollo117'
import SpiceyPy as spice
satnm = 'PHOEBE'
fixref = 'IAU_PHOEBE'
scnm = 'CASSINI'
instnm = 'CASSINI_ISS_NAC'
time = '2004 jun 11 19:32:00'


#test changing the error reaction
print(spice.erract("get", 10, b"none"))
print(spice.erract("set", 10, b"report"))
et = spice.str2et(time)
print("should still be going")
print(et)