# Solution convtm
import spiceypy


def convtm(utctim="2004 jun 11 19:32:00"):
    # Local Parameters
    METAKR = "convtm.tm"
    SCLKID = -82
    spiceypy.furnsh(METAKR)

    print(f"Converting UTC Time: {utctim}")
    # Convert utctim to ET.
    et = spiceypy.str2et(utctim)
    print(f"   ET Seconds Past J2000: {et:16.3f}")

    # Convert ET to a calendar time string; this can be done two ways.
    calet = spiceypy.etcal(et)
    print(f"   Calendar ET (etcal):   {calet}")

    # Or use timout for finer control over the output format.
    # The picture below was built by examining the header of timout.
    calet = spiceypy.timout(et, "YYYY-MON-DDTHR:MN:SC ::TDB")
    print(f"   Calendar ET (timout):  {calet}")

    # Convert ET to spacecraft clock time.
    sclkst = spiceypy.sce2s(SCLKID, et)
    print(f"   Spacecraft Clock Time: {sclkst}")

    # unload the kernel
    spiceypy.unload(METAKR)


# provide the input UTC Time:
convtm("2004 jun 11 19:32:00")
