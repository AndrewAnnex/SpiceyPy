# IMPORTANT, as of now the spice.so file needs to also be in the tests directory
__author__ = 'Apollo117'
import SpiceyPy as spice
satnm = 'PHOEBE'
fixref = 'IAU_PHOEBE'
scnm = 'CASSINI'
instnm = 'CASSINI_ISS_NAC'
time = '2004 jun 11 19:32:00'

# You must make your own meta kernel, see the spice example program on the naif website under tutorials
# http://naif.jpl.nasa.gov/naif/tutorials.html
spice.furnsh('./Kernels/testmetak.txt')

print(spice.ktotal("ALL"))
print(spice.szpool("MAXVAR"))

et = spice.str2et(time)
print("Spicetypes Epoch: ", et)

radii = spice.bodvrd(satnm, "RADII", 3)
print("Spicetypes Radii: ", radii)

instid = spice.bodn2c(instnm)
print("Spicetypes Instrument ID: ", instid)
print("")
fovRes = list(spice.getfov(instid, 10, 41, 41))
print("Fov results: ", fovRes)
print("")
print(fovRes[3])
print("")
sincptRes = list(spice.sincpt("Ellipsoid", satnm, et, fixref, "CN+S", scnm, fovRes[1], fovRes[2]))
print("Sincpt results: ", sincptRes)
backupSrfVec = sincptRes[2]
print("")
reclatRes = spice.reclat(sincptRes[0])
print("")
print("Reclat results: ", reclatRes)
re = radii[0]
rp = radii[2]
f = (re - rp)/re
print("")
print(re)
print(f)
recgeoRes = spice.recgeo(sincptRes[0], re, f)

print("Recgeo results: ", recgeoRes)

print("ILUMIN STUFF")
print("satnm: ", satnm)
print("et: ", et)
print("fixref: ", fixref)
print("scnm: ", scnm)

print("point: ", sincptRes[1])

iluminRes = list(spice.ilumin("Ellipsoid", satnm, et, fixref, "CN+S", scnm, sincptRes[0]))

print("")
print(iluminRes)
#print("Ilumin results: ", iluminRes)
print("DPR: ", spice.dpr())
print("")
print("Intercept planetocentric longitude (deg): ", spice.dpr()*reclatRes[1])
print("Intercept planetocentric latitude (deg): ", spice.dpr()*reclatRes[2])
print("Intercept planetodetic longitude (deg): ", spice.dpr()*recgeoRes[0])
print("Intercept planetodetic latitude (deg): ", spice.dpr()*recgeoRes[1])
print("Range from spacecraft to intercept point (km): ", spice.vnorm(iluminRes[1]))
print("Intercept phase angle (deg): ", spice.dpr()*iluminRes[2])
print("Intercept solar incidence angle (deg): ", spice.dpr()*iluminRes[3])
print("Intercept emission angle (deg): ", spice.dpr()*iluminRes[4])

spice.kclear()