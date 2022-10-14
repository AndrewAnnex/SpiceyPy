"""
The MIT License (MIT)

Copyright (c) [2015-2022] [Andrew Annex]

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
__all__ = ["_tkversion", "libspice_path", "libspice"]
from ctypes import CDLL, POINTER, c_int, c_double, c_char, c_char_p, c_void_p
from ctypes.util import find_library
import os
import platform

from . import support_types as stypes
from . import callbacks

if "CSPICE_SHARED_LIB" in os.environ.keys():
    libspice_path = os.environ.get("CSPICE_SHARED_LIB", None)
else:
    # capture ld_library_path, todo windows uses PATH, but I cover that case below
    _llp = os.environ.get("LD_LIBRARY_PATH")
    # append CWD to ldd
    os.environ["LD_LIBRARY_PATH"] = f"{f'{_llp}:' if _llp else ''}{os.getcwd()}"
    # locate cspice
    libspice_path = find_library("cspice")
    # restore ld_library_path
    if _llp:
        # if it was defined before, restore it
        os.environ["LD_LIBRARY_PATH"] = _llp
    else:
        # if not restore to None. Does not affect system level environment variable
        os.environ.pop("LD_LIBRARY_PATH", None)
# Try again on windows, todo combine with above to make it cleaner
if not libspice_path:
    # fallback to find file relative to current path
    host_OS = platform.system()
    sharedLib = "libcspice.dll" if host_OS == "Windows" else "libcspice.so"
    libspice_path = os.path.join(os.path.dirname(__file__), sharedLib)

libspice = CDLL(libspice_path)
# cache the tkversion for exceptions
libspice.tkvrsn_c.restype = c_char_p
_tkversion = libspice.tkvrsn_c(b"toolkit").decode("utf-8")

s_cell_p = POINTER(stypes.SpiceCell)
s_elip_p = POINTER(stypes.Ellipse)
s_plan_p = POINTER(stypes.Plane)
s_dla_p = POINTER(stypes.SpiceDLADescr)
s_eks_p = POINTER(stypes.SpiceEKSegSum)
s_eka_p = POINTER(stypes.SpiceEKAttDsc)
s_dsk_p = POINTER(stypes.SpiceDSKDescr)
c_double_p = POINTER(c_double)
c_int_p = POINTER(c_int)

__author__ = "AndrewAnnex"

# ######################################################################################################################
# A

libspice.appndc_c.argtypes = [c_char_p, s_cell_p]
libspice.appndd_c.argtypes = [c_double, s_cell_p]
libspice.appndi_c.argtypes = [c_int, s_cell_p]
libspice.axisar_c.argtypes = [(c_double * 3), c_double, (c_double * 3) * 3]
libspice.azlcpo_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_int,
    c_int,
    (c_double * 3),
    c_char_p,
    c_char_p,
    (c_double * 6),
    c_double_p,
]
libspice.azlrec_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int,
    c_int,
    (c_double * 3),
]
# #######################################################################################################################
# B
libspice.b1900_c.restype = c_double
libspice.b1950_c.restype = c_double
libspice.bodc2n_c.argtypes = [c_int, c_int, c_char_p, c_int_p]
libspice.bodc2s_c.argtypes = [c_int, c_int, c_char_p]
libspice.boddef_c.argtypes = [c_char_p, c_int]
libspice.bodeul_.argtypes = [
    c_int_p,
    c_double_p,
    c_double_p,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.badkpv_c.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int, c_char]
libspice.badkpv_c.restype = c_int
libspice.bltfrm_c.argtypes = [c_int, s_cell_p]
libspice.bodfnd_c.argtypes = [c_int, c_char_p]
libspice.bodfnd_c.restype = c_int
libspice.bodn2c_c.argtypes = [c_char_p, c_int_p, c_int_p]
libspice.bods2c_c.argtypes = [c_char_p, c_int_p, c_int_p]
libspice.bodvar_c.argtypes = [c_int, c_char_p, c_int_p, c_void_p]
libspice.bodvcd_c.argtypes = [c_int, c_char_p, c_int, c_int_p, c_void_p]
libspice.bodvrd_c.argtypes = [c_char_p, c_char_p, c_int, c_int_p, c_void_p]
libspice.brcktd_c.argtypes = [c_double, c_double, c_double]
libspice.brcktd_c.restype = c_double
libspice.brckti_c.argtypes = [c_int, c_int, c_int]
libspice.brckti_c.restype = c_int
libspice.bschoc_c.argtypes = [c_char_p, c_int, c_int, c_char_p, c_int_p]
libspice.bschoc_c.restype = c_int
libspice.bschoi_c.argtypes = [c_int, c_int, c_int_p, c_int_p]
libspice.bschoi_c.restype = c_int
libspice.bsrchc_c.argtypes = [c_char_p, c_int, c_int, c_char_p]
libspice.bsrchc_c.restype = c_int
libspice.bsrchd_c.argtypes = [c_double, c_int, c_double_p]
libspice.bsrchd_c.restype = c_int
libspice.bsrchi_c.argtypes = [c_int, c_int, c_int_p]
libspice.bsrchi_c.restype = c_int
########################################################################################################################
# C
libspice.card_c.argtypes = [s_cell_p]
libspice.card_c.restype = c_int
libspice.ccifrm_c.argtypes = [c_int, c_int, c_int, c_int_p, c_char_p, c_int_p, c_int_p]
libspice.cgv2el_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3), s_elip_p]
libspice.chbder_c.argtypes = [
    c_double_p,
    c_int,
    (c_double * 2),
    c_double,
    c_int,
    c_double_p,
    c_double_p,
]
libspice.chbigr_c.argtypes = [
    c_int,
    c_double_p,
    (c_double * 2),
    c_double,
    c_double_p,
    c_double_p,
]
libspice.chbint_c.argtypes = [
    c_double_p,
    c_int,
    (c_double * 2),
    c_double,
    c_double_p,
    c_double_p,
]
libspice.chbval_c.argtypes = [c_double_p, c_int, (c_double * 2), c_double, c_double_p]
libspice.chkin_c.argtypes = [c_char_p]
libspice.chkout_c.argtypes = [c_char_p]
libspice.cidfrm_c.argtypes = [c_int, c_int, c_int_p, c_char_p, c_int_p]
libspice.ckcls_c.argtypes = [c_int]
libspice.ckcov_c.argtypes = [
    c_char_p,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_char_p,
    s_cell_p,
]
libspice.ckobj_c.argtypes = [c_char_p, s_cell_p]
libspice.ckfrot_c.argtypes = [c_int, c_double, (c_double * 3) * 3, c_int_p, c_int_p]
libspice.ckfxfm_c.argtypes = [c_int, c_double, (c_double * 6) * 6, c_int_p, c_int_p]
libspice.ckgp_c.argtypes = [
    c_int,
    c_double,
    c_double,
    c_char_p,
    ((c_double * 3) * 3),
    c_double_p,
    c_int_p,
]
libspice.ckgpav_c.argtypes = [
    c_int,
    c_double,
    c_double,
    c_char_p,
    ((c_double * 3) * 3),
    (c_double * 3),
    c_double_p,
    c_int_p,
]
libspice.ckgr02_c.argtypes = [c_int, (c_double * 5), c_int, (c_double * 10)]
libspice.ckgr03_c.argtypes = [c_int, (c_double * 5), c_int, (c_double * 8)]
libspice.cklpf_c.argtypes = [c_char_p, c_int_p]
libspice.ckmeta_c.argtypes = [c_int, c_char_p, c_int_p]
libspice.cknr02_c.argtypes = [c_int, (c_double * 5), c_int_p]
libspice.cknr03_c.argtypes = [c_int, (c_double * 5), c_int_p]
libspice.ckopn_c.argtypes = [c_char_p, c_char_p, c_int, c_int_p]
libspice.ckupf_c.argtypes = [c_int]
libspice.ckw01_c.argtypes = [
    c_int,
    c_double,
    c_double,
    c_int,
    c_char_p,
    c_int,
    c_char_p,
    c_int,
    c_double_p,
    POINTER(c_double * 4),
    POINTER(c_double * 3),
]
libspice.ckw02_c.argtypes = [
    c_int,
    c_double,
    c_double,
    c_int,
    c_char_p,
    c_char_p,
    c_int,
    c_double_p,
    c_double_p,
    POINTER(c_double * 4),
    POINTER(c_double * 3),
    c_double_p,
]
libspice.ckw03_c.argtypes = [
    c_int,
    c_double,
    c_double,
    c_int,
    c_char_p,
    c_int,
    c_char_p,
    c_int,
    c_double_p,
    POINTER(c_double * 4),
    POINTER(c_double * 3),
    c_int,
    c_double_p,
]
libspice.ckw05_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_double,
    c_double,
    c_int,
    c_char_p,
    c_int,
    c_char_p,
    c_int,
    c_double_p,
    c_void_p,
    c_double,
    c_int,
    c_double_p,
]
libspice.clight_c.argtypes = None
libspice.clight_c.restype = c_double
libspice.clpool_c.argtypes = None
libspice.cltext_.argtypes = [c_char_p, c_int]
libspice.cmprss_c.argtypes = [c_char, c_int, c_char_p, c_int, c_char_p]
libspice.cnmfrm_c.argtypes = [c_char_p, c_int, c_int_p, c_char_p, c_int_p]
libspice.conics_c.argtypes = [(c_double * 8), c_double, (c_double * 6)]
libspice.convrt_c.argtypes = [c_double, c_char_p, c_char_p, c_double_p]
libspice.copy_c.argtypes = [s_cell_p, s_cell_p]
libspice.cpos_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.cpos_c.restype = c_int
libspice.cposr_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.cposr_c.restype = c_int
libspice.cvpool_c.argtypes = [c_char_p, c_int_p]
libspice.cyllat_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.cylrec_c.argtypes = [c_double, c_double, c_double, (c_double * 3)]
libspice.cylsph_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]

########################################################################################################################
# D

libspice.dafac_c.argtypes = [c_int, c_int, c_int, c_void_p]
libspice.dafbbs_c.argtypes = [c_int]
libspice.dafbfs_c.argtypes = [c_int]
libspice.dafcls_c.argtypes = [c_int]
libspice.dafcs_c.argtypes = [c_int]
libspice.dafdc_c.argtypes = [c_int]
libspice.dafec_c.argtypes = [c_int, c_int, c_int, c_int_p, c_void_p, c_int_p]
libspice.daffna_c.argtypes = [c_int_p]
libspice.daffpa_c.argtypes = [c_int_p]
libspice.dafgda_c.argtypes = [c_int, c_int, c_int, c_double_p]
libspice.dafgh_c.argtypes = [c_int_p]
libspice.dafgn_c.argtypes = [c_int, c_char_p]
libspice.dafgs_c.argtypes = [c_double_p]
libspice.dafgsr_c.argtypes = [c_int, c_int, c_int, c_int, c_double_p, c_int_p]
libspice.dafhsf_c.argtypes = [c_int, c_int_p, c_int_p]
libspice.dafopr_c.argtypes = [c_char_p, c_int_p]
libspice.dafopw_c.argtypes = [c_char_p, c_int_p]
libspice.dafps_c.argtypes = [c_int, c_int, c_double_p, c_int_p, c_double_p]
libspice.dafrda_c.argtypes = [c_int, c_int, c_int, c_double_p]
libspice.dafrfr_c.argtypes = [
    c_int,
    c_int,
    c_int_p,
    c_int_p,
    c_char_p,
    c_int_p,
    c_int_p,
    c_int_p,
]
libspice.dafrs_c.argtype = [c_double_p]
libspice.dafus_c.argtypes = [c_double_p, c_int, c_int, c_double_p, c_int_p]
libspice.dasac_c.argtypes = [c_int, c_int, c_int, c_void_p]
libspice.dasadc_c.argtypes = [c_int, c_int, c_int, c_int, c_int, c_void_p]
libspice.dasadd_c.argtypes = [
    c_int,
    c_int,
    POINTER(c_double),
]
libspice.dasadi_c.argtypes = [
    c_int,
    c_int,
    c_int_p,
]
libspice.dascls_c.argtypes = [c_int]
libspice.dasdc_c.argtypes = [c_int]
libspice.dasec_c.argtypes = [c_int, c_int, c_int, c_int_p, c_void_p, c_int_p]
libspice.dashfn_c.argtypes = [c_int, c_int, c_char_p]
libspice.dashfs_c.argtypes = [
    c_int,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int * 3,
    c_int * 3,
    c_int * 3,
]
libspice.daslla_c.argtypes = [c_int, c_int_p, c_int_p, c_int_p]
libspice.dasllc_c.argtypes = [
    c_int,
]
libspice.dasopr_c.argtypes = [c_char_p, c_int_p]
libspice.dasops_c.argtypes = [c_int_p]
libspice.dasopw_c.argtypes = [c_char_p, c_int_p]
libspice.dasonw_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_int,
    c_int_p,
]
libspice.dasrdc_c.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_void_p]
libspice.dasrdd_c.argtypes = [c_int, c_int, c_int, c_double_p]
libspice.dasrdi_c.argtypes = [c_int, c_int, c_int, c_int_p]
libspice.dasrfr_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_char_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
]
libspice.dasudc_c.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_void_p]
libspice.dasudd_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_double_p,
]
libspice.dasudi_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_int_p,
]
libspice.daswbr_c.argtypes = [
    c_int,
]
libspice.dazldr_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int,
    c_int,
    (c_double * 3) * 3,
]
libspice.dcyldr_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.deltet_c.argtypes = [c_double, c_char_p, c_double_p]
libspice.det_c.argtypes = [(c_double * 3) * 3]
libspice.det_c.restype = c_double
libspice.dgeodr_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    (c_double * 3) * 3,
]
libspice.diags2_c.argtypes = [
    (c_double * 2) * 2,
    (c_double * 2) * 2,
    (c_double * 2) * 2,
]
libspice.diff_c.argtypes = [s_cell_p, s_cell_p, s_cell_p]
libspice.dlabbs_c.argtypes = [c_int, s_dla_p, c_int_p]
libspice.dlabfs_c.argtypes = [c_int, s_dla_p, c_int_p]
libspice.dlabns_c.argtypes = [
    c_int,
]
libspice.dlaens_c.argtypes = [
    c_int,
]
libspice.dlafns_c.argtypes = [c_int, s_dla_p, s_dla_p, c_int_p]
libspice.dlafps_c.argtypes = [c_int, s_dla_p, s_dla_p, c_int_p]
libspice.dlaopn_c.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int_p]
libspice.dnearp_c.argtypes = [
    (c_double * 6),
    c_double,
    c_double,
    c_double,
    (c_double * 6),
    (c_double * 2),
    c_int_p,
]
libspice.dlatdr_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.dp2hx_c.argtypes = [c_double, c_int, c_char_p, c_int_p]
libspice.dpgrdr_c.argtypes = [
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    (c_double * 3) * 3,
]
libspice.dpmax_c.argtypes = None
libspice.dpmax_c.restype = c_double
libspice.dpmin_c.argtypes = None
libspice.dpmin_c.restype = c_double
libspice.dpr_c.restype = c_double
libspice.drdazl_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int,
    c_int,
    (c_double * 3) * 3,
]
libspice.drdcyl_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.drdgeo_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    (c_double * 3) * 3,
]
libspice.drdlat_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.drdpgr_c.argtypes = [
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    (c_double * 3) * 3,
]
libspice.drdsph_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.dskb02_c.argtypes = [
    c_int,
    s_dla_p,
    c_int_p,
    c_int_p,
    c_int_p,
    ((c_double * 3) * 2),
    c_double_p,
    (c_double * 3),
    (c_int * 3),
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
]
libspice.dskcls_c.argtypes = [c_int, c_int]
libspice.dskd02_c.argtypes = [c_int, s_dla_p, c_int, c_int, c_int, c_int_p, c_double_p]
libspice.dskgd_c.argtypes = [c_int, s_dla_p, s_dsk_p]
libspice.dskgtl_c.argtypes = [c_int, c_double_p]
libspice.dski02_c.argtypes = [c_int, s_dla_p, c_int, c_int, c_int, c_int_p, c_int_p]
libspice.dskmi2_c.argtypes = [
    c_int,
    POINTER(c_double * 3),
    c_int,
    POINTER(c_int * 3),
    c_double,
    c_int,
    c_int,
    c_int,
    c_int,
    c_int,
    c_int,
    POINTER(c_int * 2),
    c_double_p,
    c_int_p,
]
libspice.dskn02_c.argtypes = [c_int, s_dla_p, c_int, c_double_p]
libspice.dskobj_c.argtypes = [c_char_p, s_cell_p]
libspice.dskopn_c.argtypes = [c_char_p, c_char_p, c_int, c_int_p]
libspice.dskp02_c.argtypes = [c_int, s_dla_p, c_int, c_int, c_int_p, POINTER(c_int * 3)]
libspice.dskrb2_c.argtypes = [
    c_int,
    POINTER(c_double * 3),
    c_int,
    POINTER(c_int * 3),
    c_int,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.dsksrf_c.argtypes = [c_char_p, c_int, s_cell_p]
libspice.dskstl_c.argtypes = [c_int, c_double]
libspice.dskv02_c.argtypes = [
    c_int,
    s_dla_p,
    c_int,
    c_int,
    c_int_p,
    POINTER(c_double * 3),
]
libspice.dskw02_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_int,
    c_double_p,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_int,
    POINTER(c_double * 3),
    c_int,
    POINTER(c_int * 3),
    c_double_p,
    c_int_p,
]
libspice.dskx02_c.argtypes = [
    c_int,
    s_dla_p,
    c_double * 3,
    c_double * 3,
    c_int_p,
    c_double_p,
    c_int_p,
]
libspice.dskxsi_c.argtypes = [
    c_int,
    c_char_p,
    c_int,
    c_int_p,
    c_double,
    c_char_p,
    c_double * 3,
    c_double * 3,
    c_int,
    c_int,
    c_double * 3,
    c_int_p,
    s_dla_p,
    s_dsk_p,
    c_double_p,
    c_int_p,
    c_int_p,
]
libspice.dskxv_c.argtypes = [
    c_int,
    c_char_p,
    c_int,
    c_int_p,
    c_double,
    c_char_p,
    c_int,
    POINTER(c_double * 3),
    POINTER(c_double * 3),
    POINTER(c_double * 3),
    c_int_p,
]
libspice.dskz02_c.argtypes = [c_int, s_dla_p, c_int_p, c_int_p]
libspice.dsphdr_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.dtpool_c.argtypes = [c_char_p, c_int_p, c_int_p, c_char_p]
libspice.ducrss_c.argtypes = [c_double * 6, c_double * 6, c_double * 6]
libspice.dvcrss_c.argtypes = [c_double * 6, c_double * 6, c_double * 6]
libspice.dvdot_c.argtypes = [c_double * 6, c_double * 6]
libspice.dvdot_c.restype = c_double
libspice.dvhat_c.argtypes = [c_double * 6, c_double * 6]
libspice.dvnorm_c.argtypes = [c_double * 6]
libspice.dvnorm_c.restype = c_double
libspice.dvpool_c.argtypes = [c_char_p]
libspice.dvsep_c.argtypes = [c_double * 6, c_double * 6]
libspice.dvsep_c.restype = c_double
########################################################################################################################
# E

libspice.edlimb_c.argtypes = [c_double, c_double, c_double, (c_double * 3), s_elip_p]
libspice.ednmpt_c.argtypes = [
    c_double,
    c_double,
    c_double,
    (c_double * 3),
    (c_double * 3),
]
libspice.edpnt_c.argtypes = [
    (c_double * 3),
    c_double,
    c_double,
    c_double,
    (c_double * 3),
]
libspice.edterm_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    c_int,
    c_double_p,
    (c_double * 3),
    c_void_p,
]
libspice.ekacec_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_int,
    c_int,
    c_void_p,
    c_int,
]
libspice.ekaced_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, c_double_p, c_int]
libspice.ekacei_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, c_int_p, c_int]
libspice.ekaclc_c.argtypes = [
    c_int,
    c_int,
    c_char_p,
    c_int,
    c_void_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
]
libspice.ekacld_c.argtypes = [
    c_int,
    c_int,
    c_char_p,
    c_double_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
]
libspice.ekacli_c.argtypes = [
    c_int,
    c_int,
    c_char_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
]
libspice.ekappr_c.argtypes = [c_int, c_int, c_int_p]
libspice.ekbseg_c.argtypes = [
    c_int,
    c_char_p,
    c_int,
    c_int,
    c_void_p,
    c_int,
    c_void_p,
    c_int_p,
]
libspice.ekccnt_c.argtypes = [c_char_p, c_int_p]
libspice.ekcii_c.argtypes = [c_char_p, c_int, c_int, c_char_p, s_eka_p]
libspice.ekcls_c.argtypes = [c_int]
libspice.ekdelr_c.argtypes = [c_int, c_int, c_int]
libspice.ekffld_c.argtypes = [c_int, c_int, c_int_p]
libspice.ekfind_c.argtypes = [c_char_p, c_int, c_int_p, c_int_p, c_char_p]
libspice.ekgc_c.argtypes = [c_int, c_int, c_int, c_int, c_char_p, c_int_p, c_int_p]
libspice.ekgd_c.argtypes = [c_int, c_int, c_int, c_double_p, c_int_p, c_int_p]
libspice.ekgi_c.argtypes = [c_int, c_int, c_int, c_int_p, c_int_p, c_int_p]
libspice.ekifld_c.argtypes = [
    c_int,
    c_char_p,
    c_int,
    c_int,
    c_int,
    c_void_p,
    c_int,
    c_void_p,
    c_int_p,
    c_int_p,
]
libspice.ekinsr_c.argtypes = [c_int, c_int, c_int]
libspice.eklef_c.argtypes = [c_char_p, c_int_p]
libspice.eknelt_c.argtypes = [c_int, c_int]
libspice.eknelt_c.restype = c_int
libspice.eknseg_c.argtypes = [c_int]
libspice.eknseg_c.restype = c_int
libspice.ekntab_c.argtypes = [c_int_p]
libspice.ekopn_c.argtypes = [c_char_p, c_char_p, c_int, c_int_p]
libspice.ekopr_c.argtypes = [c_char_p, c_int_p]
libspice.ekops_c.argtypes = [c_int_p]
libspice.ekopw_c.argtypes = [c_char_p, c_int_p]
libspice.ekpsel_c.argtypes = [
    c_char_p,
    c_int,
    c_int,
    c_int,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_void_p,
    c_void_p,
    c_int_p,
    c_char_p,
]
#                              POINTER(stypes.SpiceEKDataType), POINTER(stypes.SpiceEKExprClass), c_void_p, c_void_p,
libspice.ekrcec_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_int,
    c_int_p,
    c_void_p,
    c_int_p,
]
libspice.ekrced_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_int_p,
    c_double_p,
    c_int_p,
]
libspice.ekrcei_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int_p, c_int_p, c_int_p]
libspice.ekssum_c.argtypes = [c_int, c_int, s_eks_p]
libspice.ektnam_c.argtypes = [c_int, c_int, c_char_p]
libspice.ekucec_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_int,
    c_int,
    c_void_p,
    c_int,
]
libspice.ekuced_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, c_double_p, c_int]
libspice.ekucei_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, c_int_p, c_int]
libspice.ekuef_c.argtypes = [c_int]
libspice.el2cgv_c.argtypes = [s_elip_p, (c_double * 3), (c_double * 3), (c_double * 3)]
libspice.elemc_c.argtypes = [c_char_p, s_cell_p]
libspice.elemc_c.restype = c_int
libspice.elemd_c.argtypes = [c_double, s_cell_p]
libspice.elemd_c.restype = c_int
libspice.elemi_c.argtypes = [c_int, s_cell_p]
libspice.elemi_c.restype = c_int
libspice.eqncpv_c.argtypes = [
    c_double,
    c_double,
    (c_double * 9),
    c_double,
    c_double,
    (c_double * 6),
]
libspice.eqstr_c.argtypes = [c_char_p, c_char_p]
libspice.eqstr_c.restype = c_int
libspice.erract_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.errch_c.argtypes = [c_char_p, c_char_p]
libspice.errdev_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.errdp_c.argtypes = [c_char_p, c_double]
libspice.errint_c.argtypes = [c_char_p, c_int]
libspice.errprt_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.esrchc_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.esrchc_c.restype = c_int
libspice.et2lst_c.argtypes = [
    c_double,
    c_int,
    c_double,
    c_char_p,
    c_int,
    c_int,
    c_int_p,
    c_int_p,
    c_int_p,
    c_char_p,
    c_char_p,
]
libspice.et2utc_c.argtypes = [c_double, c_char_p, c_int, c_int, c_char_p]
libspice.etcal_c.argtypes = [c_double, c_int, c_char_p]
libspice.eul2m_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int,
    c_int,
    c_int,
    (c_double * 3) * 3,
]
libspice.eul2xf_c.argtypes = [(c_double * 6), c_int, c_int, c_int, (c_double * 6) * 6]
libspice.ev2lin_.argtypes = [c_double_p, c_double_p, c_double_p, c_double_p]
libspice.evsgp4_c.argtypes = [c_double, c_double * 8, c_double * 10, c_double * 6]
libspice.exists_c.argtypes = [c_char_p]
libspice.exists_c.restype = c_int
libspice.expool_c.argtypes = [c_char_p, c_int_p]

########################################################################################################################
# F

libspice.failed_c.argtypes = None
libspice.failed_c.restype = c_int
libspice.fn2lun_.argtypes = [c_char_p, c_int_p, c_int]
libspice.fovray_c.argtypes = [
    c_char_p,
    (c_double * 3),
    c_char_p,
    c_char_p,
    c_char_p,
    c_double_p,
    c_int_p,
]
libspice.fovtrg_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double_p,
    c_int_p,
]
libspice.frame_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.frinfo_c.argtypes = [c_int, c_int_p, c_int_p, c_int_p, c_int_p]
libspice.frmnam_c.argtypes = [c_int, c_int, c_char_p]
libspice.ftncls_c.argtypes = [c_int]
libspice.furnsh_c.argtypes = [c_char_p]

########################################################################################################################
# G

libspice.gcpool_c.argtypes = [c_char_p, c_int, c_int, c_int, c_int_p, c_void_p, c_int_p]
libspice.gdpool_c.argtypes = [c_char_p, c_int, c_int, c_int_p, c_double_p, c_int_p]
libspice.georec_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    (c_double * 3),
]
libspice.getcml_c.argtypes = [c_int, c_char_p]
libspice.getelm_c.argtypes = [c_int, c_int, c_void_p, c_double_p, c_double_p]
libspice.getfat_c.argtypes = [c_char_p, c_int, c_int, c_char_p, c_char_p]
libspice.getfov_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_int_p,
    POINTER(c_double * 3),
]
libspice.getfvn_c.argtypes = [
    c_char_p,
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_int_p,
    POINTER(c_double * 3),
]
libspice.getmsg_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.gfbail_c.restype = c_int
libspice.gfclrh_c.argtypes = None
libspice.gfdist_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gfevnt_c.argtypes = [
    callbacks.UDSTEP,
    callbacks.UDREFN,
    c_char_p,
    c_int,
    c_int,
    c_void_p,
    c_void_p,
    c_double_p,
    c_int_p,
    c_int_p,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    callbacks.UDREPI,
    callbacks.UDREPU,
    callbacks.UDREPF,
    c_int,
    c_int,
    callbacks.UDBAIL,
    s_cell_p,
    s_cell_p,
]

libspice.gffove_c.argtypes = [
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    callbacks.UDSTEP,
    callbacks.UDREFN,
    c_int,
    callbacks.UDREPI,
    callbacks.UDREPU,
    callbacks.UDREPF,
    c_int,
    callbacks.UDBAIL,
    s_cell_p,
    s_cell_p,
]
libspice.gfinth_c.argtypes = [c_int]
libspice.gfilum_c.argtupes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gfocce_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    callbacks.UDSTEP,
    callbacks.UDREFN,
    c_int,
    callbacks.UDREPI,
    callbacks.UDREPU,
    callbacks.UDREPF,
    c_int,
    callbacks.UDBAIL,
    s_cell_p,
    s_cell_p,
]
libspice.gfoclt_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    s_cell_p,
    s_cell_p,
]
libspice.gfpa_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gfposc_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gfrefn_c.argtypes = [c_double, c_double, c_int, c_int, c_double_p]
libspice.gfrepf_c.argtypes = None
libspice.gfrepi_c.argtypes = [s_cell_p, c_char_p, c_char_p]
libspice.gfrepu_c.argtypes = [c_double, c_double, c_double]
libspice.gfrfov_c.argtypes = [
    c_char_p,
    (c_double * 3),
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    s_cell_p,
    s_cell_p,
]
libspice.gfrr_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gfsep_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gfsntc_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gfsstp_c.argtypes = [c_double]
libspice.gfstep_c.argtypes = [c_double, c_double_p]
libspice.gfstol_c.argtypes = [c_double]
libspice.gfsubc_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gftfov_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    s_cell_p,
    s_cell_p,
]
libspice.gfudb_c.argtypes = [
    callbacks.UDFUNS,
    callbacks.UDFUNB,
    c_double,
    s_cell_p,
    s_cell_p,
]
libspice.gfuds_c.argtypes = [
    callbacks.UDFUNS,
    callbacks.UDFUNB,
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_int,
    s_cell_p,
    s_cell_p,
]
libspice.gipool_c.argtypes = [c_char_p, c_int, c_int, c_int_p, c_int_p, c_int_p]
libspice.gnpool_c.argtypes = [c_char_p, c_int, c_int, c_int, c_int_p, c_void_p, c_int_p]

########################################################################################################################
# H

libspice.halfpi_c.restype = c_double
libspice.hrmesp_c.argtypes = [
    c_int,
    c_double,
    c_double,
    c_double_p,
    c_double,
    c_double_p,
    c_double_p,
]
libspice.hrmint_c.argtypes = [
    c_int,
    c_double_p,
    c_double_p,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.hx2dp_c.argtypes = [c_char_p, c_int, c_double_p, c_int_p, c_char_p]

########################################################################################################################
# I

libspice.ident_c.argtypes = [(c_double * 3) * 3]
libspice.illum_c.argtypes = [
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.ilumin_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double_p,
    (c_double * 3),
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.illumf_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double_p,
    (c_double * 3),
    c_double_p,
    c_double_p,
    c_double_p,
    c_int_p,
    c_int_p,
]
libspice.illumg_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double_p,
    (c_double * 3),
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.inedpl_c.argtypes = [c_double, c_double, c_double, s_plan_p, s_elip_p, c_int_p]
libspice.inelpl_c.argtypes = [
    s_elip_p,
    s_plan_p,
    c_int_p,
    (c_double * 3),
    (c_double * 3),
]

libspice.insrtc_c.argtypes = [c_char_p, s_cell_p]
libspice.insrtd_c.argtypes = [c_double, s_cell_p]
libspice.insrti_c.argtypes = [c_int, s_cell_p]
libspice.inter_c.argtypes = [s_cell_p, s_cell_p, s_cell_p]
libspice.inrypl_c.argtypes = [
    (c_double * 3),
    (c_double * 3),
    s_plan_p,
    c_int_p,
    (c_double * 3),
]
libspice.intmax_c.restype = c_int
libspice.intmin_c.restype = c_int
libspice.invert_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3]
libspice.invort_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3]
libspice.invstm_c.argtypes = [(c_double * 6) * 6, (c_double * 6) * 6]
libspice.irfnam_.argtypes = [c_int_p, c_char_p, c_int]
libspice.irfnum_.argtypes = [c_char_p, c_int_p, c_int]
libspice.irfrot_.argtypes = [c_int_p, c_int_p, (c_double * 3) * 3]
libspice.irftrn_.argtypes = [c_char_p, c_char_p, (c_double * 3) * 3, c_int, c_int]
libspice.isordv_c.argtypes = [c_int_p, c_int]
libspice.isordv_c.restype = c_int
libspice.isrchc_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.isrchc_c.restype = c_int
libspice.isrchd_c.argtypes = [c_double, c_int, c_double_p]
libspice.isrchd_c.restype = c_int
libspice.isrchi_c.argtypes = [c_int, c_int, c_int_p]
libspice.isrchi_c.restype = c_int
libspice.isrot_c.argtypes = [(c_double * 3) * 3, c_double, c_double]
libspice.isrot_c.restype = c_int
libspice.iswhsp_c.argtypes = [c_char_p]
libspice.iswhsp_c.restype = c_int
########################################################################################################################
# J

libspice.j1900_c.restype = c_double
libspice.j1950_c.restype = c_double
libspice.j2000_c.restype = c_double
libspice.j2100_c.restype = c_double
libspice.jyear_c.restype = c_double

########################################################################################################################
# K
libspice.kclear_c.restype = None
libspice.kdata_c.argtypes = [
    c_int,
    c_char_p,
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_char_p,
    c_char_p,
    c_int_p,
    c_int_p,
]
libspice.kepleq_.argtypes = [c_double_p, c_double_p, c_double_p]
libspice.kepleq_.restype = c_double
libspice.kinfo_c.argtypes = [
    c_char_p,
    c_int,
    c_int,
    c_char_p,
    c_char_p,
    c_int_p,
    c_int_p,
]
libspice.ktotal_c.argtypes = [c_char_p, c_int_p]
libspice.kplfrm_c.argtypes = [c_int, s_cell_p]
libspice.kpsolv_.argtypes = [c_double_p]
libspice.kpsolv_.restype = c_double
libspice.kxtrct_c.argtypes = [
    c_char_p,
    c_int,
    c_void_p,
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_int_p,
    c_char_p,
]

########################################################################################################################
# L
libspice.lastnb_c.argtypes = [c_char_p]
libspice.lastnb_c.restype = c_int
libspice.latcyl_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.latrec_c.argtypes = [c_double, c_double, c_double, (c_double) * 3]
libspice.latsph_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.latsrf_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_int,
    c_void_p,
    c_void_p,
]
libspice.lcase_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.ldpool_c.argtypes = [c_char_p]
libspice.lgresp_c.argtypes = [c_int, c_double, c_double, c_double_p, c_double]
libspice.lgresp_c.restype = c_double
libspice.lgrind_c.argtypes = [
    c_int,
    c_double_p,
    c_double_p,
    c_double_p,
    c_double,
    c_double_p,
    c_double_p,
]
libspice.lgrint_c.argtypes = [c_int, c_double_p, c_double_p, c_double]
libspice.lgrint_c.restype = c_double
libspice.limbpt_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double,
    c_int,
    c_double,
    c_double,
    c_int,
    c_int_p,
    c_void_p,
    c_double_p,
    c_void_p,
]
libspice.lmpool_c.argtypes = [c_void_p, c_int, c_int]
libspice.lparse_c.argtypes = [c_char_p, c_char_p, c_int, c_int, c_int_p, c_void_p]
libspice.lparsm_c.argtypes = [c_char_p, c_char_p, c_int, c_int, c_int_p, c_void_p]
libspice.lparss_c.argtypes = [c_char_p, c_char_p, s_cell_p]
libspice.lspcn_c.argtypes = [c_char_p, c_double, c_char_p]
libspice.lspcn_c.restype = c_double
libspice.ltime_c.argtypes = [c_double, c_int, c_char_p, c_int, c_double_p, c_double_p]
libspice.lstlec_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.lstlec_c.restype = c_int
libspice.lstled_c.argtypes = [c_double, c_int, c_double_p]
libspice.lstled_c.restype = c_int
libspice.lstlei_c.argtypes = [c_int, c_int, c_int_p]
libspice.lstlei_c.restype = c_int
libspice.lstltc_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.lstltc_c.restype = c_int
libspice.lstltd_c.argtypes = [c_double, c_int, c_double_p]
libspice.lstltd_c.restype = c_int
libspice.lstlti_c.argtypes = [c_int, c_int, c_int_p]
libspice.lstlti_c.restype = c_int
libspice.lx4dec_c.argtypes = [c_char_p, c_int, c_int_p, c_int_p]
libspice.lx4num_c.argtypes = [c_char_p, c_int, c_int_p, c_int_p]
libspice.lx4sgn_c.argtypes = [c_char_p, c_int, c_int_p, c_int_p]
libspice.lx4uns_c.argtypes = [c_char_p, c_int, c_int_p, c_int_p]
libspice.lxqstr_c.argtypes = [c_char_p, c_char, c_int, c_int_p, c_int_p]
########################################################################################################################
# M

libspice.m2eul_c.argtypes = [
    (c_double * 3) * 3,
    c_int,
    c_int,
    c_int,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.m2q_c.argtypes = [(c_double * 3) * 3, (c_double * 4)]
libspice.matchi_c.argtypes = [c_char_p, c_char_p, c_char, c_char]
libspice.matchi_c.restype = c_int
libspice.matchw_c.argtypes = [c_char_p, c_char_p, c_char, c_char]
libspice.matchw_c.restype = c_int
libspice.maxd_c.restype = c_double
libspice.mequ_c.argtypes = [
    (c_double * 3) * 3,
    (c_double * 3) * 3,
]
libspice.mequg_c.argtypes = [c_void_p, c_int, c_int, c_void_p]
libspice.mtxm_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3, (c_double * 3) * 3]
libspice.mtxmg_c.argtypes = [c_void_p, c_void_p, c_int, c_int, c_int, c_void_p]
libspice.mtxv_c.argtypes = [(c_double * 3) * 3, (c_double * 3), (c_double * 3)]
libspice.mtxvg_c.argtypes = [c_void_p, c_void_p, c_int, c_int, c_void_p]
libspice.mxm_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3, (c_double * 3) * 3]
libspice.mxmg_c.argtypes = [c_void_p, c_void_p, c_int, c_int, c_int, c_void_p]
libspice.mxmt_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3, (c_double * 3) * 3]
libspice.mxmtg_c.argtypes = [c_void_p, c_void_p, c_int, c_int, c_int, c_void_p]
libspice.mxv_c.argtypes = [(c_double * 3) * 3, (c_double * 3), (c_double * 3)]
libspice.mxvg_c.argtypes = [c_void_p, c_void_p, c_int, c_int, c_void_p]

########################################################################################################################
# N

libspice.namfrm_c.argtypes = [c_char_p, c_int_p]
libspice.ncpos_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.ncpos_c.restype = c_int
libspice.ncposr_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.ncposr_c.restype = c_int
libspice.nearpt_c.argtypes = [
    (c_double * 3),
    c_double,
    c_double,
    c_double,
    (c_double * 3),
    c_double_p,
]
libspice.npedln_c.argtypes = [
    c_double,
    c_double,
    c_double,
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
    c_double_p,
]
libspice.npelpt_c.argtypes = [(c_double * 3), s_elip_p, (c_double * 3), c_double_p]
libspice.nplnpt_c.argtypes = [
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
    c_double_p,
]
libspice.nvc2pl_c.argtypes = [(c_double * 3), c_double, s_plan_p]
libspice.nvp2pl_c.argtypes = [(c_double * 3), (c_double * 3), s_plan_p]

########################################################################################################################
# O
libspice.occult_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_int_p,
]
libspice.ordc_c.argtypes = [c_char_p, s_cell_p]
libspice.ordc_c.restype = c_int
libspice.ordd_c.argtypes = [c_double, s_cell_p]
libspice.ordd_c.restype = c_int
libspice.ordi_c.argtypes = [c_int, s_cell_p]
libspice.ordi_c.restype = c_int
libspice.orderc_c.argtypes = [c_int, c_void_p, c_int, c_int_p]
libspice.orderd_c.argtypes = [c_double_p, c_int, c_int_p]
libspice.orderi_c.argtypes = [c_int_p, c_int, c_int_p]
libspice.oscelt_c.argtypes = [c_double * 6, c_double, c_double, c_double * 8]
libspice.oscltx_c.argtypes = [(c_double * 6), c_double, c_double, c_double_p]

########################################################################################################################
# P

libspice.pckcls_c.argtypes = [c_int]
libspice.pckcov_c.argtypes = [c_char_p, c_int, s_cell_p]
libspice.pckfrm_c.argtypes = [c_char_p, s_cell_p]
libspice.pcklof_c.argtypes = [c_char_p, c_int_p]
libspice.pckopn_c.argtypes = [c_char_p, c_char_p, c_int, c_int_p]
libspice.pckuof_c.argtypes = [c_int]
libspice.pckw02_c.argtypes = [
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_double,
    c_int,
    c_int,
    c_double_p,
    c_double,
]
libspice.pcpool_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.pdpool_c.argtypes = [c_char_p, c_int, c_double_p]
libspice.pipool_c.argtypes = [c_char_p, c_int, c_int_p]
libspice.pgrrec_c.argtypes = [
    c_char_p,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    (c_double * 3),
]
libspice.phaseq_c.argtypes = [c_double, c_char_p, c_char_p, c_char_p, c_char_p]
libspice.phaseq_c.restype = c_double
libspice.pi_c.restype = c_double
libspice.pjelpl_c.argtypes = [s_elip_p, s_plan_p, s_elip_p]
libspice.pl2nvc_c.argtypes = [s_plan_p, (c_double * 3), c_double_p]
libspice.pl2nvp_c.argtypes = [s_plan_p, (c_double * 3), (c_double * 3)]
libspice.pl2psv_c.argtypes = [s_plan_p, (c_double * 3), (c_double * 3), (c_double * 3)]
libspice.pltar_c.argtypes = [c_int, c_void_p, c_int, c_void_p]
libspice.pltar_c.restype = c_double
libspice.pltexp_c.argtypes = [(c_double * 3) * 3, c_double, (c_double * 3) * 3]
libspice.pltnp_c.argtypes = [
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
    c_double_p,
]
libspice.pltnrm_c.argtypes = [
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
]
libspice.pltvol_c.argtypes = [c_int, c_void_p, c_int, c_void_p]
libspice.pltvol_c.restype = c_double
libspice.polyds_c.argtype = [c_double_p, c_int, c_int, c_double, c_double_p]
libspice.pos_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.pos_c.restype = c_int
libspice.posr_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.posr_c.restype = c_int
# libspice.prefix_c.argtypes = [c_char_p, c_int, c_int, c_char_p]
libspice.prop2b_c.argtypes = [c_double, (c_double * 6), c_double, (c_double * 6)]
libspice.prsdp_c.argtypes = [c_char_p, c_double_p]
libspice.prsint_c.argtypes = [c_char_p, c_int_p]
libspice.psv2pl_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3), s_plan_p]
libspice.putcml_c.argtypes = [c_int, c_char_p]
libspice.pxform_c.argtypes = [c_char_p, c_char_p, c_double, (c_double * 3) * 3]
libspice.pxfrm2_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_double,
    (c_double * 3) * 3,
]

########################################################################################################################
# Q

libspice.q2m_c.argtypes = [c_double * 4, (c_double * 3) * 3]
libspice.qcktrc_c.argtypes = [c_int, c_char_p]
libspice.qderiv_c.argtypes = [c_int, c_double_p, c_double_p, c_double, c_double_p]
libspice.qdq2av_c.argtypes = [c_double * 4, c_double * 4, c_double * 3]
libspice.qxq_c.argtypes = [c_double * 4, c_double * 4, c_double * 4]

########################################################################################################################
# R
libspice.radrec_c.argtypes = [c_double, c_double, c_double, (c_double * 3)]
libspice.rav2xf_c.argtypes = [(c_double * 3) * 3, (c_double * 3), (c_double * 6) * 6]
libspice.raxisa_c.argtypes = [(c_double * 3) * 3, (c_double * 3), c_double_p]
libspice.rdtext_c.argtypes = [c_char_p, c_int, c_char_p, c_int_p]
libspice.recazl_c.argtypes = [
    (c_double * 3),
    c_int,
    c_int,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.reccyl_c.argtypes = [(c_double * 3), c_double_p, c_double_p, c_double_p]
libspice.recgeo_c.argtypes = [
    (c_double * 3),
    c_double,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.reclat_c.argtypes = [(c_double * 3), c_double_p, c_double_p, c_double_p]
libspice.recpgr_c.argtypes = [
    c_char_p,
    (c_double * 3),
    c_double,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.recrad_c.argtypes = [(c_double * 3), c_double_p, c_double_p, c_double_p]
libspice.recsph_c.argtypes = [(c_double * 3), c_double_p, c_double_p, c_double_p]
libspice.reordc_c.argtypes = [c_int_p, c_int, c_int, c_void_p]
libspice.reordd_c.argtypes = [c_int_p, c_int, c_double_p]
libspice.reordi_c.argtypes = [c_int_p, c_int, c_int_p]
libspice.reordl_c.argtypes = [c_int_p, c_int, c_int_p]
libspice.removc_c.argtypes = [c_char_p, s_cell_p]
libspice.removd_c.argtypes = [c_double, s_cell_p]
libspice.removi_c.argtypes = [c_int, s_cell_p]
libspice.repmc_c.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p]
libspice.repmct_c.argtypes = [c_char_p, c_char_p, c_int, c_char, c_int, c_char_p]
libspice.repmd_c.argtypes = [c_char_p, c_char_p, c_double, c_int, c_int, c_char_p]
libspice.repmf_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_int,
    c_char,
    c_int,
    c_char_p,
]
libspice.repmi_c.argtypes = [c_char_p, c_char_p, c_int, c_int, c_char_p]
libspice.repmot_c.argtypes = [c_char_p, c_char_p, c_int, c_char, c_int, c_char_p]
libspice.reset_c.argtypes = None
libspice.return_c.argtypes = None
libspice.return_c.restype = c_int
libspice.rotate_c.argtypes = [c_double, c_int, (c_double * 3) * 3]
libspice.rotmat_c.argtypes = [(c_double * 3) * 3, c_double, c_int, (c_double * 3) * 3]
libspice.rotvec_c.argtypes = [(c_double * 3), c_double, c_int, (c_double * 3)]
libspice.rpd_c.restype = c_double
libspice.rquad_c.argtypes = [
    c_double,
    c_double,
    c_double,
    (c_double * 2),
    (c_double * 2),
]

########################################################################################################################
# S

libspice.saelgv_c.argtypes = [
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
    (c_double * 3),
]
libspice.scard_c.argtypes = [c_int, s_cell_p]
libspice.scdecd_c.argtypes = [c_int, c_double, c_int, c_char_p]
libspice.sce2c_c.argtypes = [c_int, c_double, c_double_p]
libspice.sce2s_c.argtypes = [c_int, c_double, c_int, c_char_p]
libspice.sce2t_c.argtypes = [c_int, c_double, c_double_p]
libspice.scencd_c.argtypes = [c_int, c_char_p, c_double_p]
libspice.scfmt_c.argtypes = [c_int, c_double, c_int, c_char_p]
libspice.scpart_c.argtypes = [c_int, c_int_p, c_double_p, c_double_p]
libspice.scs2e_c.argtypes = [c_int, c_char_p, c_double_p]
libspice.sct2e_c.argtypes = [c_int, c_double, c_double_p]
libspice.sctiks_c.argtypes = [c_int, c_char_p, c_double_p]
libspice.sdiff_c.argtypes = [s_cell_p, s_cell_p, s_cell_p]
libspice.set_c.argtypes = [s_cell_p, c_char_p, s_cell_p]
libspice.set_c.restype = c_int
libspice.setmsg_c.argtypes = [c_char_p]
libspice.shellc_c.argtypes = [c_int, c_int, c_void_p]
libspice.shelld_c.argtypes = [c_int, c_double_p]
libspice.shelli_c.argtypes = [c_int, c_int_p]
libspice.sigerr_c.argtypes = [c_char_p]
libspice.sincpt_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    (c_double * 3),
    c_double_p,
    (c_double * 3),
    c_int_p,
]
libspice.spd_c.restype = c_double
libspice.sphcyl_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.sphlat_c.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_p,
    c_double_p,
    c_double_p,
]
libspice.sphrec_c.argtypes = [c_double, c_double, c_double, (c_double * 3)]
libspice.spk14a_c.argtypes = [c_int, c_int, c_double_p, c_double_p]
libspice.spk14b_c.argtypes = [
    c_int,
    c_char_p,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_int,
]
libspice.spk14e_c.argtypes = [c_int]
libspice.spkacs_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    c_char_p,
    c_int,
    (c_double * 6),
    c_double_p,
    c_double_p,
]
libspice.spkapo_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    (c_double * 6),
    c_char_p,
    (c_double * 3),
    c_double_p,
]
libspice.spkapp_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    (c_double * 6),
    c_char_p,
    (c_double * 6),
    c_double_p,
]
libspice.spkaps_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    c_char_p,
    (c_double * 6),
    (c_double * 6),
    (c_double * 6),
    c_double_p,
    c_double_p,
]
libspice.spkcls_c.argtypes = [c_int]
libspice.spkcov_c.argtypes = [c_char_p, c_int, s_cell_p]
libspice.spkcpo_c.argtypes = [
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_char_p,
    c_char_p,
    (c_double * 6),
    c_double_p,
]
libspice.spkcpt_c.argtypes = [
    (c_double * 3),
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 6),
    c_double_p,
]
libspice.spkcvo_c.argtypes = [
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 6),
    c_double,
    c_char_p,
    c_char_p,
    (c_double * 6),
    c_double_p,
]
libspice.spkcvt_c.argtypes = [
    (c_double * 6),
    c_double,
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 6),
    c_double_p,
]
libspice.spkez_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    c_char_p,
    c_int,
    (c_double * 6),
    c_double_p,
]
libspice.spkezp_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    c_char_p,
    c_int,
    (c_double * 3),
    c_double_p,
]
libspice.spkezr_c.argtypes = [
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 6),
    c_double_p,
]
libspice.spkgeo_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    c_int,
    (c_double * 6),
    c_double_p,
]
libspice.spkgps_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    c_int,
    (c_double * 3),
    c_double_p,
]
libspice.spklef_c.argtypes = [c_char_p, c_int_p]
libspice.spkltc_c.argtypes = [
    c_int,
    c_double,
    c_char_p,
    c_char_p,
    (c_double * 6),
    (c_double * 6),
    c_double_p,
    c_double_p,
]
libspice.spkobj_c.argtypes = [c_char_p, s_cell_p]
libspice.spkopa_c.argtypes = [c_char_p, c_int_p]
libspice.spkopn_c.argtypes = [c_char_p, c_char_p, c_int, c_int_p]
libspice.spkpds_c.argtypes = [
    c_int,
    c_int,
    c_char_p,
    c_int,
    c_double,
    c_double,
    (c_double * 5),
]
libspice.spkpos_c.argtypes = [
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double_p,
]
libspice.spkpvn_c.argtypes = [
    c_int,
    (c_double * 5),
    c_double,
    c_int_p,
    (c_double * 6),
    c_int_p,
]
libspice.spksfs_c.argtypes = [
    c_int,
    c_double,
    c_int,
    c_int_p,
    (c_double * 5),
    c_char_p,
    c_int_p,
]
libspice.spkssb_c.argtypes = [c_int, c_double, c_char_p, (c_double * 6)]
libspice.spksub_c.argtypes = [
    c_int,
    (c_double * 5),
    c_char_p,
    c_double,
    c_double,
    c_int,
]
libspice.spkuds_c.argtypes = [
    (c_double * 5),
    c_int_p,
    c_int_p,
    c_int_p,
    c_int_p,
    c_double_p,
    c_double_p,
    c_int_p,
    c_int_p,
]
libspice.spkuef_c.argtypes = [c_int]
libspice.spkw02_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_double,
    c_int,
    c_int,
    c_double_p,
    c_double,
]
libspice.spkw03_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_double,
    c_int,
    c_int,
    c_double_p,
    c_double,
]
libspice.spkw05_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_double,
    c_int,
    POINTER(c_double * 6),
    c_double_p,
]
libspice.spkw08_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_int,
    c_int,
    POINTER(c_double * 6),
    c_double,
    c_double,
]
libspice.spkw09_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_int,
    c_int,
    POINTER(c_double * 6),
    c_double_p,
]
libspice.spkw10_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    (c_double * 8),
    c_int,
    c_double_p,
    c_double_p,
]
libspice.spkw12_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_int,
    c_int,
    POINTER(c_double * 6),
    c_double,
    c_double,
]
libspice.spkw13_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_int,
    c_int,
    POINTER(c_double * 6),
    c_double_p,
]
libspice.spkw15_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_double,
    (c_double * 3),
    (c_double * 3),
    c_double,
    c_double,
    c_double,
    (c_double * 3),
    c_double,
    c_double,
    c_double,
]
libspice.spkw17_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_double,
    (c_double * 9),
    c_double,
    c_double,
]
libspice.spkw18_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_int,
    c_int,
    c_void_p,
    c_double_p,
]
libspice.spkw20_c.argtypes = [
    c_int,
    c_int,
    c_int,
    c_char_p,
    c_double,
    c_double,
    c_char_p,
    c_double,
    c_int,
    c_int,
    c_double_p,
    c_double,
    c_double,
    c_double,
    c_double,
]
libspice.srfc2s_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int_p]
libspice.srfcss_c.argtypes = [c_int, c_char_p, c_int, c_char_p, c_int_p]
libspice.srfnrm_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_int,
    c_void_p,
    c_void_p,
]
libspice.srfrec_c.argtypes = [c_int, c_double, c_double, (c_double * 3)]
libspice.srfs2c_c.argtypes = [c_char_p, c_char_p, c_int_p, c_int_p]
libspice.srfscc_c.argtypes = [c_char_p, c_int, c_int_p, c_int_p]
libspice.size_c.argtypes = [s_cell_p]
libspice.size_c.restype = c_int
libspice.srfxpt_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    (c_double * 3),
    c_double_p,
    c_double_p,
    (c_double * 3),
    c_int_p,
]
libspice.ssize_c.argtypes = [c_int, s_cell_p]
libspice.stelab_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.stlabx_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.stpool_c.argtypes = [
    c_char_p,
    c_int,
    c_char_p,
    c_int,
    c_char_p,
    c_int_p,
    c_int_p,
]
libspice.str2et_c.argtypes = [c_char_p, c_double_p]
libspice.subpnt_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double_p,
    (c_double * 3),
]
libspice.subpt_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double_p,
]
libspice.subslr_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double_p,
    (c_double * 3),
]
libspice.subsol_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    (c_double * 3),
]
libspice.sumai_c.argtypes = [c_int_p, c_int]
libspice.sumai_c.restype = c_int
libspice.sumad_c.argtypes = [c_double_p, c_int]
libspice.sumad_c.restype = c_double
libspice.surfnm_c.argtypes = [
    c_double,
    c_double,
    c_double,
    (c_double * 3),
    (c_double * 3),
]
libspice.surfpt_c.argtypes = [
    (c_double * 3),
    (c_double * 3),
    c_double,
    c_double,
    c_double,
    (c_double * 3),
    c_int_p,
]
libspice.surfpv_c.argtypes = [
    (c_double * 6),
    (c_double * 6),
    c_double,
    c_double,
    c_double,
    (c_double * 6),
    c_int_p,
]
libspice.swpool_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.sxform_c.argtypes = [c_char_p, c_char_p, c_double, (c_double * 6) * 6]
libspice.szpool_c.argtypes = [c_char_p, c_int_p, c_int_p]

########################################################################################################################
# T
libspice.tangpt_c.argtypes = [
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    (c_double * 3),
    c_double_p,
    c_double_p,
    (c_double * 3),
    c_double_p,
    (c_double * 3),
]
libspice.termpt_c.argtypes = [
    c_char_p,
    c_char_p,
    c_char_p,
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 3),
    c_double,
    c_int,
    c_double,
    c_double,
    c_int,
    c_int_p,
    c_void_p,
    c_double_p,
    c_void_p,
]
libspice.timdef_c.argtypes = [c_char_p, c_char_p, c_int, c_char_p]
libspice.timout_c.argtypes = [c_double, c_char_p, c_int, c_char_p]
libspice.tipbod_c.argtypes = [c_char_p, c_int, c_double, (c_double * 3) * 3]
libspice.tisbod_c.argtypes = [c_char_p, c_int, c_double, (c_double * 6) * 6]
libspice.tkfram_.argtypes = [c_int_p, (c_double * 3) * 3, c_int_p, c_int_p]
libspice.tkvrsn_c.argtypes = [c_char_p]
libspice.tkvrsn_c.restype = c_char_p
libspice.tparch_c.argtypes = [c_char_p]
libspice.tparse_c.argtypes = [c_char_p, c_int, c_double_p, c_char_p]
libspice.tpictr_c.argtypes = [c_char_p, c_int, c_int, c_char_p, c_int_p, c_char_p]
libspice.trace_c.argtypes = [(c_double * 3) * 3]
libspice.trace_c.restype = c_double
libspice.trcdep_c.argtypes = [c_int_p]
libspice.trcnam_c.argtypes = [c_int, c_int, c_char_p]
libspice.trcoff_c.argtypes = None
libspice.trgsep_c.argtypes = [
    c_double,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
    c_char_p,
]
libspice.trgsep_c.restype = c_double
libspice.tsetyr_c.argtypes = [c_int]
libspice.twopi_c.restype = c_double
libspice.twovec_c.argtypes = [
    (c_double * 3),
    c_int,
    (c_double * 3),
    c_int,
    (c_double * 3) * 3,
]
libspice.twovxf_c.argtypes = [
    (c_double * 6),
    c_int,
    (c_double * 6),
    c_int,
    (c_double * 6) * 6,
]
libspice.txtopn_.argtypes = [c_char_p, c_int_p, c_int]
libspice.tyear_c.restype = c_double

########################################################################################################################
# U

libspice.ucase_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.ucrss_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.uddc_c.argtypes = [callbacks.UDFUNS, c_double, c_double, c_int_p]
libspice.uddc_c.restype = None
libspice.uddf_c.argtypes = [callbacks.UDFUNS, c_double, c_double, c_double_p]
libspice.uddf_c.restype = None
libspice.udf_c.argtypes = [c_double, c_double_p]
libspice.udf_c.restype = None
libspice.union_c.argtypes = [s_cell_p, s_cell_p, s_cell_p]
libspice.unitim_c.argtypes = [c_double, c_char_p, c_char_p]
libspice.unitim_c.restype = c_double
libspice.unload_c.argtypes = [c_char_p]
libspice.unorm_c.argtypes = [(c_double * 3), (c_double * 3), c_double_p]
libspice.unormg_c.argtypes = [c_double_p, c_int, c_double_p, c_double_p]
libspice.utc2et_c.argtypes = [c_char_p, c_double_p]
########################################################################################################################
# V

libspice.vadd_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vaddg_c.argtypes = [c_double_p, c_double_p, c_int, c_double_p]
libspice.valid_c.argtypes = [c_int, c_int, s_cell_p]
libspice.vcrss_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vdist_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.vdist_c.restype = c_double
libspice.vdistg_c.argtypes = [c_double_p, c_double_p, c_int]
libspice.vdistg_c.restype = c_double
libspice.vdot_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.vdot_c.restype = c_double
libspice.vdotg_c.argtypes = [c_double_p, c_double_p, c_int]
libspice.vdotg_c.restype = c_double
libspice.vequ_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.vequg_c.argtypes = [c_double_p, c_int, c_double_p]
libspice.vhat_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.vhatg_c.argtypes = [c_double_p, c_int, c_double_p]
libspice.vlcom_c.argtypes = [
    c_double,
    (c_double * 3),
    c_double,
    (c_double * 3),
    (c_double * 3),
]
libspice.vlcom3_c.argtypes = [
    c_double,
    (c_double * 3),
    c_double,
    (c_double * 3),
    c_double,
    (c_double * 3),
    (c_double * 3),
]
libspice.vlcomg_c.argtypes = [
    c_int,
    c_double,
    c_double_p,
    c_double,
    c_double_p,
    c_double_p,
]
libspice.vminug_c.argtypes = [c_double_p, c_int, c_double_p]
libspice.vminus_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.vnorm_c.restype = c_double
libspice.vnorm_c.argstype = [stypes.empty_double_vector(3)]
libspice.vnormg_c.restype = c_double
libspice.vnormg_c.argstype = [c_double_p, c_int]
libspice.vpack_c.argtypes = [c_double, c_double, c_double, (c_double * 3)]
libspice.vperp_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vprjp_c.argtypes = [(c_double * 3), s_plan_p, (c_double * 3)]
libspice.vprjpi_c.argtypes = [
    (c_double * 3),
    s_plan_p,
    s_plan_p,
    (c_double * 3),
    c_int_p,
]
libspice.vproj_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vprojg_c.argtypes = [c_double_p, c_double_p, c_int, c_double_p]
libspice.vrelg_c.argtypes = [c_double_p, c_double_p, c_int]
libspice.vrelg_c.restype = c_double
libspice.vrel_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.vrel_c.restype = c_double
libspice.vrotv_c.argtypes = [(c_double * 3), (c_double * 3), c_double, (c_double * 3)]
libspice.vscl_c.argtypes = [c_double, (c_double * 3), (c_double * 3)]
libspice.vsclg_c.argtypes = [c_double, c_double_p, c_int, c_double_p]
libspice.vsep_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.vsep_c.restype = c_double
libspice.vsepg_c.argtypes = [c_double_p, c_double_p, c_int]
libspice.vsepg_c.restype = c_double
libspice.vsub_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vsubg_c.argtypes = [c_double_p, c_double_p, c_int, c_double_p]
libspice.vtmv_c.argtypes = [(c_double * 3), (c_double * 3) * 3, (c_double * 3)]
libspice.vtmv_c.restype = c_double
libspice.vtmvg_c.argtypes = [c_double_p, c_void_p, c_double_p, c_int, c_int]
libspice.vtmvg_c.restype = c_double
libspice.vupack_c.argtypes = [(c_double * 3), c_double_p, c_double_p, c_double_p]
libspice.vzero_c.argtypes = [(c_double * 3)]
libspice.vzero_c.restype = c_int
libspice.vzerog_c.argtypes = [c_double_p, c_int]
libspice.vzerog_c.restype = c_int

########################################################################################################################
# W
libspice.wncard_c.argtypes = [s_cell_p]
libspice.wncard_c.restype = c_int
libspice.wncomd_c.argtypes = [c_double, c_double, s_cell_p, s_cell_p]
libspice.wncond_c.argtypes = [c_double, c_double, s_cell_p]
libspice.wndifd_c.argtypes = [s_cell_p, s_cell_p, s_cell_p]
libspice.wnelmd_c.argtypes = [c_double, s_cell_p]
libspice.wnelmd_c.restype = c_int
libspice.wnexpd_c.argtypes = [c_double, c_double, s_cell_p]
libspice.wnextd_c.argtypes = [c_char, s_cell_p]
libspice.wnfetd_c.argtypes = [s_cell_p, c_int, c_double_p, c_double_p]
libspice.wnfild_c.argtypes = [c_double, s_cell_p]
libspice.wnfltd_c.argtypes = [c_double, s_cell_p]
libspice.wnincd_c.argtypes = [c_double, c_double, s_cell_p]
libspice.wnincd_c.restype = c_int
libspice.wninsd_c.argtypes = [c_double, c_double, s_cell_p]
libspice.wnintd_c.argtypes = [s_cell_p, s_cell_p, s_cell_p]
libspice.wnreld_c.argtypes = [s_cell_p, c_char_p, s_cell_p]
libspice.wnreld_c.restype = c_int
libspice.wnsumd_c.argtypes = [
    s_cell_p,
    c_double_p,
    c_double_p,
    c_double_p,
    c_int_p,
    c_int_p,
]
libspice.wnunid_c.argtypes = [s_cell_p, s_cell_p, s_cell_p]
libspice.wnvald_c.argtypes = [c_int, c_int, s_cell_p]
libspice.writln_.argtypes = [c_char_p, c_int_p, c_int]
########################################################################################################################
# X

libspice.xf2eul_c.argtypes = [
    (c_double * 6) * 6,
    c_int,
    c_int,
    c_int,
    (c_double * 6),
    c_int_p,
]
libspice.xf2rav_c.argtypes = [(c_double * 6) * 6, (c_double * 3) * 3, (c_double * 3)]
libspice.xfmsta_c.argtypes = [
    (c_double * 6),
    c_char_p,
    c_char_p,
    c_char_p,
    (c_double * 6),
]
libspice.xpose_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3]
libspice.xpose6_c.argtypes = [(c_double * 6) * 6, (c_double * 6) * 6]
libspice.xposeg_c.argtypes = [c_void_p, c_int, c_int, c_void_p]
########################################################################################################################
# Z
libspice.zzdynrot_.argtypes = [
    c_int_p,
    c_int_p,
    c_double_p,
    (c_double * 3) * 3,
    c_int_p,
]
libspice.zzgetcml_c.argtypes = [c_int, c_char_p, c_int]
libspice.zzgfsavh_c.argtypes = [c_int]

# libspice.zzsynccl_c.argtypes = [None]
