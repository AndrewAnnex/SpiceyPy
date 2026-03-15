import spiceypy


def convrt():

    mkfile = "convrt.tm"
    spiceypy.furnsh(mkfile)

    utc = "2004-06-11T19:32:00"
    et = spiceypy.str2et(utc)

    print(f"UTC       = {utc}")
    print(f"ET        = {et:20.6f}")

    spiceypy.unload(mkfile)


if __name__ == "__main__":
    convrt()
