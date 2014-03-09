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

et = spice.str2et(time)
print("Spicetypes Epoch: ", et)

radii = spice.bodvrd(satnm, "RADII", 3)
print("Spicetypes Radii: ", radii)

instid = spice.bodn2c(instnm)
print("Spicetypes Instrument ID: ", instid)
print("")
fovRes = spice.getfov(instid, 10, 41, 41)
print("Fov results: ", fovRes)
print("")
print(fovRes['bounds'])
print("")
sincptRes = spice.sincpt("Ellipsoid", satnm, et, fixref, "CN+S", scnm, fovRes['frame'], fovRes['bsight'])
print("Sincpt results: ", sincptRes)
backupSrfVec = sincptRes['srfvec']
print("")

reclatRes = spice.reclat(sincptRes['spoint'])
print("")
print("Reclat results: ", reclatRes)
re = radii[0]
rp = radii[2]
f = (re - rp)/re
print("")
print(re)
print(f)
recgeoRes = spice.recgeo(sincptRes['spoint'], re, f)

print("Recgeo results: ", recgeoRes)

print("ILUMIN STUFF")
print("satnm: ", satnm)
print("et: ", et)
print("fixref: ", fixref)
print("scnm: ", scnm)
print("point: ", sincptRes['spoint'])

iluminRes = spice.ilumin("Ellipsoid", satnm, et, fixref, "CN+S", scnm, sincptRes['spoint'])

print("")
print(iluminRes)
#print("Ilumin results: ", iluminRes)
print("DPR: ", spice.dpr())
print("")
print("Intercept planetocentric longitude (deg): ", spice.dpr()*reclatRes[1])
print("Intercept planetocentric latitude (deg): ", spice.dpr()*reclatRes[2])
print("Intercept planetodetic longitude (deg): ", spice.dpr()*recgeoRes[0])
print("Intercept planetodetic latitude (deg): ", spice.dpr()*recgeoRes[1])
print("Range from spacecraft to intercept point (km): ", spice.vnorm(iluminRes['srfvec']))
print("Intercept phase angle (deg): ", spice.dpr()*iluminRes['phase'])
print("Intercept solar incidence angle (deg): ", spice.dpr()*iluminRes['solar'])
print("Intercept emission angle (deg): ", spice.dpr()*iluminRes['emissn'])