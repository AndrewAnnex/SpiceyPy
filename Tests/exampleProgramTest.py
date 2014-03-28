__author__ = 'Apollo117'
import SpiceyPy as spice
satnm = 'PHOEBE'
fixref = 'IAU_PHOEBE'
scnm = 'CASSINI'
instnm = 'CASSINI_ISS_NAC'
time = '2004 jun 11 19:32:00'

# You must download the needed kernels, please read testMetaK.txt for links
spice.furnsh('./testMetaK.txt')

et = spice.str2et(time)
print("Epoch: ", et)

radii = spice.bodvrd(satnm, "RADII", 3)
print("Radii: ", radii)

instid = spice.bodn2c(instnm)
print("Instrument ID: ", instid)
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

print("ILUMIN parameters prior to running command")
print("satnm: ", satnm)
print("et: ", et)
print("fixref: ", fixref)
print("scnm: ", scnm)

print("point: ", sincptRes[1])

iluminRes = list(spice.ilumin("Ellipsoid", satnm, et, fixref, "CN+S", scnm, sincptRes[0]))

print("")
print("Ilumin results: ", iluminRes)
print("")
print("Final results")
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