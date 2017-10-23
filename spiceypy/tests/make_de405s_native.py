"""
The MIT License (MIT)

Copyright (c) [2015-2017] [Andrew Annex]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Purpose:

    Convert [BIG-IEEE] DE-405 SPK to native byte order;
    insert <native>-IEEE string

    Source file:

        https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de405s.bsp
          => de405s_bigendian.bsp (locally)
          => MD5 hash:  b010eb485bd01da5b651c58a6c8f8e67

    Destination file:

        de405s.bsp


N.B This script does exactly the same thing, byte-for-byte with the exception
    of the insertion of the <native>-IEEE string, that the SPICE utility
    BINGO does via the command

        bingo -ieee2pc de405s_bigendian.bsp de405s.bsp


Sample usage:

    Within gettestkernels.py (no output):

        import make_de405s_native as mdn
        mdn.make_de405s_native()

    Command-line:

        python -c 'import make_de405s_native,sys;make_de405s_native.make_de405s_native(logFile=sys.stdout)'

"""
import os
import sys
import numpy
import hashlib

class fakeIO(object):
    def __init__(self):
        pass
    def write(self, s):
        pass

def make_de405s_native(logFile=fakeIO()):

    cwd = os.path.dirname(__file__)
    fnDe405s_msb = os.path.join(cwd, 'de405s_bigendian.bsp')
    fnDe405s_lcl = os.path.join(cwd, 'de405s.bsp')

    pfx, bo = ('>', 'big') if "FORCE_BIGENDIAN" in os.environ else ('=', sys.byteorder)

    i4 = 4, numpy.dtype('>i4'), numpy.dtype(pfx+'i4')
    f8= 8, numpy.dtype('>f8'), numpy.dtype(pfx+'f8')
    LOCFMT = b'BIG-IEEE' if bo == 'big' else b'LTL-IEEE'  # LOCFMT (8 bytes)

    with open(fnDe405s_msb, 'rb') as fIn:
        with open(fnDe405s_lcl, 'wb') as fOut:

            md5 = hashlib.md5()

            def update_md_and_spk(bites):
                md5.update(bites)
                fOut.write(bites)

            def sn_copy(n):
                update_md_and_spk(fIn.read(n))

            def xn_copy(n, xn):
                arr = numpy.array(numpy.fromstring(fIn.read(n*xn[0]), dtype=xn[1]), dtype=xn[2])
                update_md_and_spk(arr.tostring())
                return arr

            # In the DAF context, a word is 8 bytes long = 1 DBL = 2 4-byte INTs

            # DAF Record 1
            # - Cf. https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/daf.html#The%20File%20Record   
            sn_copy(8)                      # Copy LOCIDW
            ND, NI = xn_copy(2, i4)         # Copy ND, NI
            assert ND==2 and NI==6
            sn_copy(60)                     # Copy LOCIFN
            fwd, bwd, fre = xn_copy(3, i4)  # Copy FWARD, BWARD, FREE = Location of first free (unused) word
            assert fwd==7 and bwd==7
            rem = fre - 1                   # (Location of first free word - 1) = words remaining to write before starting this record
            fIn.read(8)                     # Discard 8 bytes from input DAF
            update_md_and_spk(LOCFMT)       # Write LOCFMT (8 bytes)
            sn_copy(928)                    # Copy Balance of record
            rem -= 128                      # Decrement remaining words for record just completed

            # DAF Records 2-6 are comments in de405s.bsp
            sn_copy(1024 * (6 - 1))
            rem -= (128 * (6 - 1))          # Decrement remaining words for records 2-6

            # DAF Record 7:  First, and only, summary record in de405s.bsp
            # - Cf. https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/daf.html#Summary%20Records
            # TI => even number of INTs (half-words) that hold NI INTs
            # SS => Number of words that hold ND DBLs + NI INTs
            TI = ((NI + 1) >> 1) << 1       # 3 words for INTs per single summary
            SS = ND + (TI >> 1)             # 5 words (2 + 3) per single summary
            assert TI == 6 and SS == 5
            nxt, prv, nsm = xn_copy(3, f8)  # NEXT, PREV, NSUM from summary record
            assert nxt==0.0                 # - No next summary record:  this is the last summary record
            assert prv==0.0                 # - No previous summary record:  this is the first summary record
            assert nsm==15.0                # - This summary record contains 15 single summaries
            while nsm > 0.0:
                nsm -= 1.0
                xn_copy(ND, f8)             # DC
                xn_copy(TI, i4)             # IC
            xn_copy(50, f8)                 # Remaining 50 DPs = 128 - (3 + (15 * SS))
            rem -= 128                      # Decrement remaining words for record 7

            # DAF Record 8:  array (sgement) names; mirrors DAF Summary record
            sn_copy(1024)                   # Names are strings; no swapping required
            rem -= 128                      # Decrement remaining words for records 8

            # The rest of the records contain only DBL words
            while rem > 0:
                xn_copy(128, f8)            # Copy each DAF DBL record
                rem -= 128                  # Decrement remaining words for each DBL record

            expectedMd5hash = '865893b7f64f323b5b0ef949edb4f242' if bo == 'big' else '6870f7bd98ff45afcf61dbb993a98650'
            assert expectedMd5hash == md5.hexdigest()

    logFile.write('Successful MD5 hash ({}) check; SPK [{}] creation complete\n'.format(expectedMd5hash, fnDe405s_lcl))
