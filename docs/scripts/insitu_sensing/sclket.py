import spiceypy

def sclket():

    mkfile = 'sclket.tm'
    spiceypy.furnsh(mkfile)

    utc =  '2004-06-11T19:32:00'
    et = spiceypy.str2et(utc)

    print(f'UTC       = {utc:s}')
    print(f'ET        = {et:20.6f}')

    scid = -82
    sclk = '1465674964.105'
    et = spiceypy.scs2e(scid, sclk)

    print(f'SCLK      = {sclk:s}')
    print(f'ET        = {et:20.6f}')

    spiceypy.unload(mkfile)


if __name__ == '__main__':
    sclket()
