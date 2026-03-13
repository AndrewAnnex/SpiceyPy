import spiceypy


def getsta():

    mkfile = "getsta.tm"
    spiceypy.furnsh(mkfile)

    utc = "2004-06-11T19:32:00"
    et = spiceypy.str2et(utc)

    print(f"UTC       = {utc:s}")
    print(f"ET        = {et:20.6f}")

    scid = -82
    sclk = "1465674964.105"
    et = spiceypy.scs2e(scid, sclk)

    print(f"SCLK      = {sclk:s}")
    print(f"ET        = {et:20.6f}")

    target = "CASSINI"
    frame = "ECLIPJ2000"
    corrtn = "NONE"
    observ = "SUN"

    state, ltime = spiceypy.spkezr(target, et, frame, corrtn, observ)

    print(f" X        = {state[0]:20.6f}")
    print(f" Y        = {state[1]:20.6f}")
    print(f" Z        = {state[2]:20.6f}")
    print(f"VX        = {state[3]:20.6f}")
    print(f"VY        = {state[4]:20.6f}")
    print(f"VZ        = {state[5]:20.6f}")

    spiceypy.unload(mkfile)


if __name__ == "__main__":
    getsta()
