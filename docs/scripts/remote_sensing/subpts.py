# Solution subpts.py
import spiceypy

def subpts(utctim='2004 jun 11 19:32:00'):
    METAKR = 'subpts.tm'
    spiceypy.furnsh(METAKR)
    print(f'Converting UTC Time: {utctim}')
    et = spiceypy.str2et(utctim)
    print(f'   ET seconds past J2000: {et:16.3f}')
    # Compute sub-points using both an ellipsoidal and a DSK shape model.
    for method in ('NEAR POINT/Ellipsoid', 'NADIR/DSK/Unprioritized'):
        print(f'\n Sub-point/target shape model: {method}\n')
        # Compute the apparent sub-observer point of CASSINI on Phoebe.
        spoint, trgepc, srfvec = spiceypy.subpnt(
        method, 'PHOEBE', et, 'IAU_PHOEBE', 'LT+S', 'CASSINI')
        print('   Apparent sub-observer point of CASSINI on Phoebe in the\n'
        '   IAU_PHOEBE frame (km):')
        print(f'      X = {spoint[0]:16.3f}')
        print(f'      Y = {spoint[1]:16.3f}')
        print(f'      Z = {spoint[2]:16.3f}')
        print(f'    ALT = {spiceypy.vnorm(srfvec):16.3f}')
        # Compute the apparent sub-solar point on Phoebe as seen from CASSINI.
        spoint, trgepc, srfvec = spiceypy.subslr(method, 'PHOEBE', et, 'IAU_PHOEBE', 'LT+S', 'CASSINI')
        print('   Apparent sub-solar point on Phoebe as seen from CASSINI in\n'
        '   the IAU_PHOEBE frame (km):')
        print(f'      X = {spoint[0]:16.3f}')
        print(f'      Y = {spoint[1]:16.3f}')
        print(f'      Z = {spoint[2]:16.3f}')
    spiceypy.kclear()

subpts()
