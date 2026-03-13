mk = r"""
KPL/MK
\begindata
KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                    'kernels/spk/de405s.bsp',
                    'kernels/pck/pck00008.tpc')
"""
with open("aderr.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file aderr.tm")
print("")
#
# Import the CSPICE-Python interface.
#
import spiceypy


# For simplicity, we request only one input.
# The program calculates the state vector from
# Earth to the user specified target 'targ' in the
# J2000 frame, at ephemeris time zero, using
# aberration correction LT+S (light time plus
# stellar aberration).
def aderr(targ: str):
    print(f"Target: {targ}")
    spiceypy.furnsh("aderr.tm")
    try:
        #
        # Perform the state lookup.
        #
        state, ltime = spiceypy.spkezr(targ, 0.0, "J2000", "LT+S", "EARTH")
        #
        # No error, output the state.
        #
        r0, r1, r2, v0, v1, v2 = state
        print(f"R : {r0:20.6f} {r1:20.6f} {r2:20.6f}")
        print(f"V : {v0:20.6f} {v1:20.6f} {v2:20.6f}")
        print(f"LT: {ltime:20.6f}\n")
    except spiceypy.SpiceyError as err:
        #
        # What if spiceypy.spkezr signaled an error?
        # Then spiceypy signals an error to python.
        #
        # Examine the value of 'err' to retrieve the
        # error message.
        #
        print(err)
        print()
    finally:
        #
        # Done. Unload the kernels.
        #
        spiceypy.kclear()


if __name__ == "__main__":
    aderr("Moon")
    aderr("Mars")
    aderr("Pluto barycenter")
    aderr("Puck")
