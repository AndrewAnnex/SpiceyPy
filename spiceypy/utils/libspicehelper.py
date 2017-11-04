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

from ctypes import CDLL, POINTER, c_bool, c_int, c_double, c_char, c_char_p, c_void_p
import os
import platform
from . import support_types as stypes
from . import callbacks

host_OS = platform.system()
sharedLib = "cspice.dll" if host_OS == "Windows" else "spice.so"
sitePath = os.path.join(os.path.dirname(__file__), sharedLib)
libspice = CDLL(sitePath)

__author__ = 'AndrewAnnex'

# ######################################################################################################################
# A

libspice.appndc_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.appndd_c.argtypes = [c_double, POINTER(stypes.SpiceCell)]
libspice.appndi_c.argtypes = [c_int, POINTER(stypes.SpiceCell)]
libspice.axisar_c.argtypes = [(c_double * 3), c_double, (c_double * 3) * 3]

# #######################################################################################################################
# B
libspice.b1900_c.restype = c_double
libspice.b1950_c.restype = c_double
libspice.bodc2n_c.argtypes = [c_int, c_int, c_char_p, POINTER(c_bool)]
libspice.bodc2s_c.argtypes = [c_int, c_int, c_char_p]
libspice.boddef_c.argtypes = [c_char_p, c_int]
libspice.badkpv_c.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int, c_char]
libspice.badkpv_c.restype = c_bool
libspice.bltfrm_c.argtypes = [c_int, POINTER(stypes.SpiceCell)]
libspice.bodfnd_c.argtypes = [c_int, c_char_p]
libspice.bodfnd_c.restype = c_bool
libspice.bodn2c_c.argtypes = [c_char_p, POINTER(c_int), POINTER(c_bool)]
libspice.bods2c_c.argtypes = [c_char_p, POINTER(c_int), POINTER(c_bool)]
libspice.bodvar_c.argtypes = [c_int, c_char_p, POINTER(c_int), c_void_p]
libspice.bodvcd_c.argtypes = [c_int, c_char_p, c_int, POINTER(c_int), c_void_p]
libspice.bodvrd_c.argtypes = [c_char_p, c_char_p, c_int, POINTER(c_int), c_void_p]
libspice.brcktd_c.argtypes = [c_double, c_double, c_double]
libspice.brcktd_c.restype = c_double
libspice.brckti_c.argtypes = [c_int, c_int, c_int]
libspice.brckti_c.restype = c_int
libspice.bschoc_c.argtypes = [c_char_p, c_int, c_int, c_char_p, POINTER(c_int)]
libspice.bschoc_c.restype = c_int
libspice.bschoi_c.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int)]
libspice.bschoi_c.restype = c_int
libspice.bsrchc_c.argtypes = [c_char_p, c_int, c_int, c_char_p]
libspice.bsrchc_c.restype = c_int
libspice.bsrchd_c.argtypes = [c_double, c_int, POINTER(c_double)]
libspice.bsrchd_c.restype = c_int
libspice.bsrchi_c.argtypes = [c_int, c_int, POINTER(c_int)]
libspice.bsrchi_c.restype = c_int
########################################################################################################################
# C
libspice.card_c.argtypes = [POINTER(stypes.SpiceCell)]
libspice.card_c.restype = c_int
libspice.ccifrm_c.argtypes = [c_int, c_int, c_int, POINTER(c_int), c_char_p, POINTER(c_int), POINTER(c_bool)]
libspice.cgv2el_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3), POINTER(stypes.Ellipse)]
libspice.chbder_c.argtypes = [POINTER(c_double), c_int, (c_double*2), c_double, c_int, POINTER(c_double), POINTER(c_double)]
libspice.chkin_c.argtypes = [c_char_p]
libspice.chkout_c.argtypes = [c_char_p]
libspice.cidfrm_c.argtypes = [c_int, c_int, POINTER(c_int), c_char_p, POINTER(c_bool)]
libspice.ckcls_c.argtypes = [c_int]
libspice.ckcov_c.argtypes = [c_char_p, c_int, c_bool, c_char_p, c_double, c_char_p, POINTER(stypes.SpiceCell)]
libspice.ckobj_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.ckgp_c.argtypes = [c_int, c_double, c_double, c_char_p, ((c_double * 3) * 3), POINTER(c_double),
                            POINTER(c_bool)]
libspice.ckgpav_c.argtypes = [c_int, c_double, c_double, c_char_p, ((c_double * 3) * 3), (c_double * 3),
                              POINTER(c_double), POINTER(c_bool)]
libspice.cklpf_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.ckopn_c.argtypes = [c_char_p, c_char_p, c_int, POINTER(c_int)]
libspice.ckupf_c.argtypes = [c_int]
libspice.ckw01_c.argtypes = [c_int, c_double, c_double, c_int, c_char_p, c_bool, c_char_p, c_int, POINTER(c_double),
                             POINTER(c_double * 4), POINTER(c_double * 3)]
libspice.ckw02_c.argtypes = [c_int, c_double, c_double, c_int, c_char_p, c_char_p, c_int, POINTER(c_double),
                             POINTER(c_double), POINTER(c_double * 4), POINTER(c_double * 3), POINTER(c_double)]
libspice.ckw03_c.argtypes = [c_int, c_double, c_double, c_int, c_char_p, c_bool, c_char_p, c_int, POINTER(c_double),
                             POINTER(c_double * 4), POINTER(c_double * 3), c_int, POINTER(c_double)]
libspice.ckw05_c.argtypes = [c_int, c_int, c_int, c_double, c_double, c_int, c_char_p, c_bool, c_char_p, c_int,
                             POINTER(c_double), c_void_p, c_double, c_int, POINTER(c_double)]
libspice.clight_c.argtypes = None
libspice.clight_c.restype = c_double
libspice.clpool_c.argtypes = None
libspice.cltext_.argtypes = [c_char_p, c_int]
libspice.cmprss_c.argtypes = [c_char, c_int, c_char_p, c_int, c_char_p]
libspice.cnmfrm_c.argtypes = [c_char_p, c_int, POINTER(c_int), c_char_p, POINTER(c_bool)]
libspice.conics_c.argtypes = [(c_double * 8), c_double, (c_double * 6)]
libspice.convrt_c.argtypes = [c_double, c_char_p, c_char_p, POINTER(c_double)]
libspice.copy_c.argtypes = [POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.cpos_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.cpos_c.restype = c_int
libspice.cposr_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.cposr_c.restype = c_int
libspice.cvpool_c.argtypes = [c_char_p, POINTER(c_bool)]
libspice.cyllat_c.argtypes = [c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.cylrec_c.argtypes = [c_double, c_double, c_double, (c_double * 3)]
libspice.cylsph_c.argtypes = [c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]

########################################################################################################################
#D

libspice.dafac_c.argtypes = [c_int, c_int, c_int, c_void_p]
libspice.dafbbs_c.argtypes = [c_int]
libspice.dafbfs_c.argtypes = [c_int]
libspice.dafcls_c.argtypes = [c_int]
libspice.dafcs_c.argtypes = [c_int]
libspice.dafdc_c.argtypes = [c_int]
libspice.dafec_c.argtypes = [c_int, c_int, c_int, POINTER(c_int), c_void_p, POINTER(c_bool)]
libspice.daffna_c.argtypes = [POINTER(c_bool)]
libspice.daffpa_c.argtypes = [POINTER(c_bool)]
libspice.dafgda_c.argtypes = [c_int, c_int, c_int, POINTER(c_double)]
libspice.dafgh_c.argtypes = [POINTER(c_int)]
libspice.dafgn_c.argtypes = [c_int, c_char_p]
libspice.dafgs_c.argtypes = [POINTER(c_double)]
libspice.dafgsr_c.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_double), POINTER(c_bool)]
libspice.dafopr_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.dafopw_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.dafps_c.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_int), POINTER(c_double)]
libspice.dafrda_c.argtypes = [c_int, c_int, c_int, POINTER(c_double)]
libspice.dafrfr_c.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), c_char_p, POINTER(c_int), POINTER(c_int),
                              POINTER(c_int)]
libspice.dafrs_c.argtype = [POINTER(c_double)]
libspice.dafus_c.argtypes = [POINTER(c_double), c_int, c_int, POINTER(c_double), POINTER(c_int)]
libspice.dasac_c.argtypes = [c_int, c_int, c_int, c_void_p]
libspice.dascls_c.argtypes = [c_int]
libspice.dasdc_c.argtypes = [c_int]
libspice.dasec_c.argtypes = [c_int, c_int, c_int, POINTER(c_int), c_void_p, POINTER(c_bool)]
libspice.dashfn_c.argtypes = [c_int, c_int, c_char_p]
libspice.dasopr_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.dasopw_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.dasonw_.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), POINTER(c_int), c_int, c_int, c_int]
libspice.dasrfr_c.argtypes = [c_int, c_int, c_int, c_char_p, c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
libspice.dcyldr_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.deltet_c.argtypes = [c_double, c_char_p, POINTER(c_double)]
libspice.det_c.argtypes = [(c_double * 3) * 3]
libspice.det_c.restype = c_double
libspice.dgeodr_c.argtypes = [c_double, c_double, c_double, c_double, c_double, (c_double * 3) * 3]
libspice.diags2_c.argtypes = [(c_double * 2) * 2, (c_double * 2) * 2, (c_double * 2) * 2]
libspice.diff_c.argtypes = [POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.dlabbs_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), POINTER(c_bool)]
libspice.dlabfs_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), POINTER(c_bool)]
libspice.dlafns_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), POINTER(stypes.SpiceDLADescr), POINTER(c_bool)]
libspice.dlafps_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), POINTER(stypes.SpiceDLADescr), POINTER(c_bool)]
libspice.dlatdr_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.dp2hx_c.argtypes = [c_double, c_int, c_char_p, POINTER(c_int)]
libspice.dpgrdr_c.argtypes = [c_char_p, c_double, c_double, c_double, c_double, c_double, (c_double * 3) * 3]
libspice.dpmax_c.argtypes = None
libspice.dpmax_c.restype = c_double
libspice.dpmin_c.argtypes = None
libspice.dpmin_c.restype = c_double
libspice.dpr_c.restype = c_double
libspice.drdcyl_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.drdgeo_c.argtypes = [c_double, c_double, c_double, c_double, c_double, (c_double * 3) * 3]
libspice.drdlat_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.drdpgr_c.argtypes = [c_char_p, c_double, c_double, c_double, c_double, c_double, (c_double * 3) * 3]
libspice.drdsph_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.dskb02_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), POINTER(c_int), POINTER(c_int), POINTER(c_int), ((c_double * 3) * 2), POINTER(c_double), (c_double*3), (c_int*3), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
libspice.dskcls_c.argtypes = [c_int, c_bool]
libspice.dskd02_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), c_int, c_int, c_int, POINTER(c_int), POINTER(c_double)]
libspice.dskgd_c.argtypes  = [c_int, POINTER(stypes.SpiceDLADescr), POINTER(stypes.SpiceDSKDescr)]
libspice.dskgtl_c.argtypes = [c_int, POINTER(c_double)]
libspice.dski02_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), c_int, c_int, c_int, POINTER(c_int), POINTER(c_int)]
libspice.dskmi2_c.argtypes = [c_int, POINTER(c_double * 3), c_int, POINTER(c_int * 3), c_double, c_int, c_int, c_int, c_int, c_bool, c_int, POINTER(c_int * 2), POINTER(c_double), POINTER(c_int)]
libspice.dskn02_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), c_int, POINTER(c_double)]
libspice.dskobj_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.dskopn_c.argtypes = [c_char_p, c_char_p, c_int, POINTER(c_int)]
libspice.dskp02_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), c_int, c_int, POINTER(c_int), POINTER(c_int * 3)]
libspice.dskrb2_c.argtypes = [c_int, POINTER(c_double * 3), c_int, POINTER(c_int * 3), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.dsksrf_c.argtypes = [c_char_p, c_int, POINTER(stypes.SpiceCell)]
libspice.dskstl_c.argtypes = [c_int, c_double]
libspice.dskv02_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), c_int, c_int, POINTER(c_int), POINTER(c_double * 3)]
libspice.dskw02_c.argtypes = [c_int, c_int, c_int, c_int, c_char_p, c_int, POINTER(c_double), c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_int, POINTER(c_double * 3), c_int, POINTER(c_int * 3), POINTER(c_double), POINTER(c_int)]
libspice.dskx02_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), c_double * 3, c_double * 3, POINTER(c_int), POINTER(c_double), POINTER(c_bool)]
libspice.dskxsi_c.argtypes = [c_bool,  c_char_p, c_int, POINTER(c_int), c_double, c_char_p, c_double * 3, c_double * 3, c_int, c_int, c_double * 3, POINTER(c_int), POINTER(stypes.SpiceDLADescr), POINTER(stypes.SpiceDSKDescr), POINTER(c_double), POINTER(c_int), POINTER(c_bool)]
libspice.dskxv_c.argtypes  = [c_bool, c_char_p, c_int, POINTER(c_int), c_double, c_char_p, c_int, POINTER(c_double *3), POINTER(c_double * 3), POINTER(c_double * 3), POINTER(c_bool)]
libspice.dskz02_c.argtypes = [c_int, POINTER(stypes.SpiceDLADescr), POINTER(c_int), POINTER(c_int)]
libspice.dsphdr_c.argtypes = [c_double, c_double, c_double, (c_double * 3) * 3]
libspice.dtpool_c.argtypes = [c_char_p, POINTER(c_bool), POINTER(c_int), POINTER(c_char)]
libspice.ducrss_c.argtypes = [c_double * 6, c_double * 6, c_double * 6]
libspice.dvcrss_c.argtypes = [c_double * 6, c_double * 6, c_double * 6]
libspice.dvdot_c.argtypes  = [c_double * 6, c_double * 6]
libspice.dvdot_c.restype   = c_double
libspice.dvhat_c.argtypes  = [c_double * 6, c_double * 6]
libspice.dvnorm_c.argtypes = [c_double * 6]
libspice.dvnorm_c.restype  = c_double
libspice.dvpool_c.argtypes = [c_char_p]
libspice.dvsep_c.argtypes  = [c_double * 6, c_double * 6]
libspice.dvsep_c.restype   = c_double
########################################################################################################################
# E

libspice.edlimb_c.argtypes = [c_double, c_double, c_double, (c_double * 3), POINTER(stypes.Ellipse)]
libspice.edterm_c.argtypes = [c_char_p, c_char_p, c_char_p, c_double, c_char_p,
                              c_char_p, c_char_p, c_int, POINTER(c_double),
                              (c_double * 3), c_void_p]
libspice.ekacec_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, c_int, c_void_p, c_int]
libspice.ekaced_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, POINTER(c_double), c_int]
libspice.ekacei_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, POINTER(c_int), c_int]
libspice.ekaclc_c.argtypes = [c_int, c_int, c_char_p, c_int, c_void_p, POINTER(c_int), POINTER(c_bool), POINTER(c_int),
                              POINTER(c_int)]
libspice.ekacld_c.argtypes = [c_int, c_int, c_char_p, POINTER(c_double), POINTER(c_int), POINTER(c_int),
                              POINTER(c_int), POINTER(c_int)]
libspice.ekacli_c.argtypes = [c_int, c_int, c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int),
                              POINTER(c_int)]
libspice.ekappr_c.argtypes = [c_int, c_int, POINTER(c_int)]
libspice.ekbseg_c.argtypes = [c_int, c_char_p, c_int, c_int, c_void_p, c_int, c_void_p, POINTER(c_int)]
libspice.ekccnt_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.ekcii_c.argtypes = [c_char_p, c_int, c_int, c_char_p, POINTER(stypes.SpiceEKAttDsc)]
libspice.ekcls_c.argtypes = [c_int]
libspice.ekdelr_c.argtypes = [c_int, c_int, c_int]
libspice.ekffld_c.argtypes = [c_int, c_int, POINTER(c_int)]
libspice.ekfind_c.argtypes = [c_char_p, c_int, POINTER(c_int), POINTER(c_bool), c_char_p]
libspice.ekgc_c.argtypes = [c_int, c_int, c_int, c_int, c_char_p, POINTER(c_bool), POINTER(c_bool)]
libspice.ekgd_c.argtypes = [c_int, c_int, c_int, POINTER(c_double), POINTER(c_bool), POINTER(c_bool)]
libspice.ekgi_c.argtypes = [c_int, c_int, c_int, POINTER(c_int), POINTER(c_bool), POINTER(c_bool)]
libspice.ekifld_c.argtypes = [c_int, c_char_p, c_int, c_int, c_int, c_void_p, c_int, c_void_p, POINTER(c_int),
                              POINTER(c_int)]
libspice.ekinsr_c.argtypes = [c_int, c_int, c_int]
libspice.eklef_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.eknelt_c.argtypes = [c_int, c_int]
libspice.eknelt_c.restype = c_int
libspice.eknseg_c.argtypes = [c_int]
libspice.eknseg_c.restype = c_int
libspice.ekntab_c.argtypes = [POINTER(c_int)]
libspice.ekopn_c.argtypes = [c_char_p, c_char_p, c_int, POINTER(c_int)]
libspice.ekopr_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.ekops_c.argtypes = [POINTER(c_int)]
libspice.ekopw_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.ekpsel_c.argtypes = [c_char_p, c_int, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int),
                              POINTER(c_int), POINTER(c_int), c_void_p, c_void_p,
                              POINTER(c_bool), c_char_p]
#                              POINTER(stypes.SpiceEKDataType), POINTER(stypes.SpiceEKExprClass), c_void_p, c_void_p,
libspice.ekrcec_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, POINTER(c_int), c_void_p, POINTER(c_bool)]
libspice.ekrced_c.argtypes = [c_int, c_int, c_int, c_char_p, POINTER(c_int), POINTER(c_double), POINTER(c_bool)]
libspice.ekrcei_c.argtypes = [c_int, c_int, c_int, c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_bool)]
libspice.ekssum_c.argtypes = [c_int, c_int, POINTER(stypes.SpiceEKSegSum)]
libspice.ektnam_c.argtypes = [c_int, c_int, c_char_p]
libspice.ekucec_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, c_int, c_void_p, c_int]
libspice.ekuced_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, POINTER(c_double), c_int]
libspice.ekucei_c.argtypes = [c_int, c_int, c_int, c_char_p, c_int, POINTER(c_int), c_int]
libspice.ekuef_c.argtypes = [c_int]
libspice.el2cgv_c.argtypes = [POINTER(stypes.Ellipse), (c_double * 3), (c_double * 3), (c_double * 3)]
libspice.elemc_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.elemc_c.restype = c_bool
libspice.elemd_c.argtypes = [c_double, POINTER(stypes.SpiceCell)]
libspice.elemd_c.restype = c_bool
libspice.elemi_c.argtypes = [c_int, POINTER(stypes.SpiceCell)]
libspice.elemi_c.restype = c_bool
libspice.eqncpv_c.argtypes = [c_double, c_double, (c_double * 9), c_double, c_double,
                              (c_double * 6)]
libspice.eqstr_c.argtypes = [c_char_p, c_char_p]
libspice.eqstr_c.restype = c_bool
libspice.erract_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.errch_c.argtypes = [c_char_p, c_char_p]
libspice.errdev_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.errdp_c.argtypes = [c_char_p, c_double]
libspice.errint_c.argtypes = [c_char_p, c_int]
libspice.errprt_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.esrchc_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.esrchc_c.restype = c_int
libspice.et2lst_c.argtypes = [c_double, c_int, c_double, c_char_p, c_int, c_int, POINTER(c_int), POINTER(c_int),
                              POINTER(c_int), c_char_p, c_char_p]
libspice.et2utc_c.argtypes = [c_double, c_char_p, c_int, c_int, c_char_p]
libspice.etcal_c.argtypes = [c_double, c_int, c_char_p]
libspice.eul2m_c.argtypes = [c_double, c_double, c_double, c_int, c_int, c_int, (c_double * 3) * 3]
libspice.eul2xf_c.argtypes = [(c_double * 6), c_int, c_int, c_int, (c_double * 6) * 6]
libspice.exists_c.argtypes = [c_char_p]
libspice.exists_c.restype = c_bool
libspice.expool_c.argtypes = [c_char_p, POINTER(c_bool)]

########################################################################################################################
# F

libspice.failed_c.argtypes = None
libspice.failed_c.restype = c_bool
libspice.fn2lun_.argtypes = [c_char_p, POINTER(c_int), c_int]
libspice.fovray_c.argtypes = [c_char_p, (c_double * 3), c_char_p, c_char_p, c_char_p,
                              POINTER(c_double), POINTER(c_bool)]
libspice.fovtrg_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p,
                              c_char_p, POINTER(c_double), POINTER(c_bool)]
libspice.frame_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.frinfo_c.argtypes = [c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_bool)]
libspice.frmnam_c.argtypes = [c_int, c_int, c_char_p]
libspice.ftncls_c.argtypes = [c_int]
libspice.furnsh_c.argtypes = [c_char_p]

########################################################################################################################
# G

libspice.gcpool_c.argtypes = [c_char_p, c_int, c_int, c_int, POINTER(c_int), c_void_p, POINTER(c_bool)]
libspice.gdpool_c.argtypes = [c_char_p, c_int, c_int, POINTER(c_int), POINTER(c_double), POINTER(c_bool)]
libspice.georec_c.argtypes = [c_double, c_double, c_double, c_double, c_double, (c_double * 3)]
libspice.getcml_c.argtypes = [c_int, c_char_p]
libspice.getelm_c.argtypes = [c_int, c_int, c_void_p, POINTER(c_double), POINTER(c_double)]
libspice.getfat_c.argtypes = [c_char_p, c_int, c_int, c_char_p, c_char_p]
libspice.getfov_c.argtypes = [c_int, c_int, c_int, c_int, c_char_p, c_char_p, (c_double * 3), POINTER(c_int),
                              POINTER(c_double * 3)]
libspice.getmsg_c.argtypes = [c_char_p, c_int, c_char_p]
libspice.gfbail_c.restype  = c_bool
libspice.gfclrh_c.argtypes = None
libspice.gfdist_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_double, c_double, c_double, c_int,
                              POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
# libspice.gfevnt_c.argtypes = [c_double, c_double, c_double, c_double, c_bool, c_bool, c_double, c_char_p, c_int, c_int, c_char_p, c_double, c_double, c_double, c_bool, None, c_char_p, c_char_p, c_double, c_double, c_double, c_int, c_bool, c_bool, None, None]
# libspice.gffove_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_double, c_double, c_double, c_double,  c_double, c_bool, c_bool, c_double, c_bool, None,  c_char_p, c_char_p, c_double, c_double, c_double,  c_bool, c_bool, None, None]
libspice.gfinth_c.argtypes = [c_int]
libspice.gfilum_c.argtupes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, (c_double * 3), c_char_p, c_double, c_double, c_double, c_int, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
# libspice.gfocce_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_double, c_double, c_double, c_double, c_double, c_bool, c_bool, c_double, c_bool, None, c_char_p, c_char_p, c_double, c_double, c_double, c_bool, c_bool, None, None]
libspice.gfoclt_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p,
                              c_double, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gfpa_c.argtypes   = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_double, c_double,
                              c_double, c_int, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gfposc_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_double, c_double,
                              c_double, c_int, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gfrefn_c.argtypes = [c_double, c_double, c_bool, c_bool, POINTER(c_double)]
libspice.gfrepf_c.argtypes = None
libspice.gfrepi_c.argtypes = [POINTER(stypes.SpiceCell), c_char_p, c_char_p]
libspice.gfrepu_c.argtypes = [c_double, c_double, c_double]
libspice.gfrfov_c.argtypes = [c_char_p, (c_double * 3), c_char_p, c_char_p, c_char_p, c_double,
                              POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gfrr_c.argtypes   = [c_char_p, c_char_p, c_char_p, c_char_p, c_double, c_double, c_double, c_int,
                              POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gfsep_c.argtypes  = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p,
                              c_double, c_double, c_double, c_int, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gfsntc_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, (c_double * 3), c_char_p,
                              c_char_p, c_char_p, c_double, c_double, c_double, c_int, POINTER(stypes.SpiceCell),
                              POINTER(stypes.SpiceCell)]
libspice.gfsstp_c.argtypes = [c_double]
libspice.gfstep_c.argtypes = [c_double, POINTER(c_double)]
libspice.gfstol_c.argtypes = [c_double]
libspice.gfsubc_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_double,
                              c_double, c_double, c_int, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gftfov_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_double,
                              POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gfudb_c.argtypes  = [callbacks.UDFUNS, callbacks.UDFUNB, c_double, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gfuds_c.argtypes  = [callbacks.UDFUNS, callbacks.UDFUNB, c_char_p, c_double, c_double, c_double, c_int, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.gipool_c.argtypes = [c_char_p, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_bool)]
libspice.gnpool_c.argtypes = [c_char_p, c_int, c_int, c_int, POINTER(c_int), c_void_p, POINTER(c_bool)]

########################################################################################################################
# H

libspice.halfpi_c.restype = c_double
libspice.hrmint_c.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.hx2dp_c.argtypes = [c_char_p, c_int, POINTER(c_double), POINTER(c_bool), c_char_p]

########################################################################################################################
# I

libspice.ident_c.argtypes  = [(c_double * 3) * 3]
libspice.illum_c.argtypes  = [c_char_p, c_double, c_char_p, c_char_p, (c_double * 3), POINTER(c_double),
                             POINTER(c_double), POINTER(c_double)]
libspice.ilumin_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, (c_double * 3),
                              POINTER(c_double), (c_double * 3), POINTER(c_double), POINTER(c_double),
                              POINTER(c_double)]
libspice.illumf_c.argtypes = [c_char_p, c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, (c_double * 3), POINTER(c_double), (c_double * 3), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_bool), POINTER(c_bool)]
libspice.illumg_c.argtypes = [c_char_p, c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, (c_double * 3), POINTER(c_double), (c_double * 3), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.inedpl_c.argtypes = [c_double, c_double, c_double, POINTER(stypes.Plane), POINTER(stypes.Ellipse),
                              POINTER(c_bool)]
libspice.inelpl_c.argtypes = [POINTER(stypes.Ellipse), POINTER(stypes.Plane), POINTER(c_int), (c_double * 3),
                              (c_double * 3)]

libspice.insrtc_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.insrtd_c.argtypes = [c_double, POINTER(stypes.SpiceCell)]
libspice.insrti_c.argtypes = [c_int, POINTER(stypes.SpiceCell)]
libspice.inter_c.argtypes  = [POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.inrypl_c.argtypes = [(c_double * 3), (c_double * 3), POINTER(stypes.Plane), POINTER(c_int), (c_double * 3)]
libspice.intmax_c.restype  = c_int
libspice.intmin_c.restype  = c_int
libspice.invert_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3]
libspice.invort_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3]
libspice.isordv_c.argtypes = [POINTER(c_int), c_int]
libspice.isordv_c.restype  = c_bool
libspice.isrchc_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.isrchc_c.restype  = c_int
libspice.isrchd_c.argtypes = [c_double, c_int, POINTER(c_double)]
libspice.isrchd_c.restype  = c_int
libspice.isrchi_c.argtypes = [c_int, c_int, POINTER(c_int)]
libspice.isrchi_c.restype  = c_int
libspice.isrot_c.argtypes  = [(c_double * 3) * 3, c_double, c_double]
libspice.isrot_c.restype   = c_bool
libspice.iswhsp_c.argtypes = [c_char_p]
libspice.iswhsp_c.restype  = c_bool
########################################################################################################################
# J

libspice.j1900_c.restype = c_double
libspice.j1950_c.restype = c_double
libspice.j2000_c.restype = c_double
libspice.j2100_c.restype = c_double
libspice.jyear_c.restype = c_double

########################################################################################################################
# K
libspice.kclear_c.restype  = None
libspice.kdata_c.argtypes  = [c_int, c_char_p, c_int, c_int, c_int, c_char_p, c_char_p, c_char_p, POINTER(c_int),
                             POINTER(c_bool)]
libspice.kinfo_c.argtypes  = [c_char_p, c_int, c_int, c_char_p, c_char_p, POINTER(c_int), POINTER(c_bool)]
libspice.ktotal_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.kplfrm_c.argtypes = [c_int, POINTER(stypes.SpiceCell)]
libspice.kxtrct_c.argtypes = [c_char_p, c_int, c_void_p, c_int, c_int, c_int, c_char_p, POINTER(c_bool), c_char_p]

########################################################################################################################
# L
libspice.lastnb_c.argtypes = [c_char_p]
libspice.lastnb_c.restype  = c_int
libspice.latcyl_c.argtypes = [c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.latrec_c.argtypes = [c_double, c_double, c_double, (c_double) * 3]
libspice.latsph_c.argtypes = [c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.latsrf_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_int, c_void_p, c_void_p]
libspice.lcase_c.argtypes  = [c_char_p, c_int, c_char_p]
libspice.ldpool_c.argtypes = [c_char_p]
libspice.lgrind_c.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double, POINTER(c_double), POINTER(c_double)]
libspice.limbpt_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, c_char_p, (c_double * 3), c_double, c_int, c_double, c_double, c_int, POINTER(c_int), c_void_p, POINTER(c_double), c_void_p]
libspice.lmpool_c.argtypes = [c_void_p, c_int, c_int]
libspice.lparse_c.argtypes = [c_char_p, c_char_p, c_int, c_int, POINTER(c_int), c_void_p]
libspice.lparsm_c.argtypes = [c_char_p, c_char_p, c_int, c_int, POINTER(c_int), c_void_p]
libspice.lparss_c.argtypes = [c_char_p, c_char_p, POINTER(stypes.SpiceCell)]
libspice.lspcn_c.argtypes  = [c_char_p, c_double, c_char_p]
libspice.lspcn_c.restype   = c_double
libspice.ltime_c.argtypes  = [c_double, c_int, c_char_p, c_int, POINTER(c_double), POINTER(c_double)]
libspice.lstlec_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.lstlec_c.restype  = c_int
libspice.lstled_c.argtypes = [c_double, c_int, POINTER(c_double)]
libspice.lstled_c.restype  = c_int
libspice.lstlei_c.argtypes = [c_int, c_int, POINTER(c_int)]
libspice.lstlei_c.restype  = c_int
libspice.lstltc_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.lstltc_c.restype  = c_int
libspice.lstltd_c.argtypes = [c_double, c_int, POINTER(c_double)]
libspice.lstltd_c.restype  = c_int
libspice.lstlti_c.argtypes = [c_int, c_int, POINTER(c_int)]
libspice.lstlti_c.restype  = c_int
libspice.lx4dec_c.argtypes = [c_char_p, c_int, POINTER(c_int), POINTER(c_int)]
libspice.lx4num_c.argtypes = [c_char_p, c_int, POINTER(c_int), POINTER(c_int)]
libspice.lx4sgn_c.argtypes = [c_char_p, c_int, POINTER(c_int), POINTER(c_int)]
libspice.lx4uns_c.argtypes = [c_char_p, c_int, POINTER(c_int), POINTER(c_int)]
libspice.lxqstr_c.argtypes = [c_char_p, c_char, c_int, POINTER(c_int), POINTER(c_int)]
########################################################################################################################
# M

libspice.m2eul_c.argtypes = [(c_double * 3) * 3, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double),
                             POINTER(c_double)]
libspice.m2q_c.argtypes = [(c_double * 3) * 3, (c_double * 4)]
libspice.matchi_c.argtypes = [c_char_p, c_char_p, c_char, c_char]
libspice.matchi_c.restype = c_bool
libspice.matchw_c.argtypes = [c_char_p, c_char_p, c_char, c_char]
libspice.matchw_c.restype = c_bool
libspice.maxd_c.restype = c_double
libspice.mequ_c.argtypes = [(c_double * 3) * 3, (c_double * 3) * 3, ]
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

libspice.namfrm_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.ncpos_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.ncpos_c.restype = c_int
libspice.ncposr_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.ncposr_c.restype = c_int
libspice.nearpt_c.argtypes = [(c_double * 3), c_double, c_double, c_double, (c_double * 3), POINTER(c_double)]
libspice.npedln_c.argtypes = [c_double, c_double, c_double, (c_double * 3), (c_double * 3), (c_double * 3),
                              POINTER(c_double)]
libspice.npelpt_c.argtypes = [(c_double * 3), POINTER(stypes.Ellipse), (c_double * 3), POINTER(c_double)]
libspice.nplnpt_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3), (c_double * 3), POINTER(c_double)]
libspice.nvc2pl_c.argtypes = [(c_double * 3), c_double, POINTER(stypes.Plane)]
libspice.nvp2pl_c.argtypes = [(c_double * 3), (c_double * 3), POINTER(stypes.Plane)]

########################################################################################################################
# O
libspice.occult_c.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p,
                              c_char_p, c_char_p, c_char_p, c_double,
                              POINTER(c_int)]
libspice.ordc_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.ordc_c.restype = c_int
libspice.ordd_c.argtypes = [c_double, POINTER(stypes.SpiceCell)]
libspice.ordd_c.restype = c_int
libspice.ordi_c.argtypes = [c_int, POINTER(stypes.SpiceCell)]
libspice.ordi_c.restype = c_int
libspice.orderc_c.argtypes = [c_int, c_void_p, c_int, POINTER(c_int)]
libspice.orderd_c.argtypes = [POINTER(c_double), c_int, POINTER(c_int)]
libspice.orderi_c.argtypes = [POINTER(c_int), c_int, POINTER(c_int)]
libspice.oscelt_c.argtypes = [c_double * 6, c_double, c_double, c_double * 8]
libspice.oscltx_c.argtypes = [(c_double * 6), c_double, c_double, POINTER(c_double)]

########################################################################################################################
# P

libspice.pckcls_c.argtypes = [c_int]
libspice.pckcov_c.argtypes = [c_char_p, c_int, POINTER(stypes.SpiceCell)]
libspice.pckfrm_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.pcklof_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.pckopn_c.argtypes = [c_char_p, c_char_p, c_int, POINTER(c_int)]
libspice.pckuof_c.argtypes = [c_int]
libspice.pckw02_c.argtypes = [c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_double, c_int, c_int, POINTER(c_double), c_double]
libspice.pcpool_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.pdpool_c.argtypes = [c_char_p, c_int, POINTER(c_double)]
libspice.pipool_c.argtypes = [c_char_p, c_int, POINTER(c_int)]
libspice.pgrrec_c.argtypes = [c_char_p, c_double, c_double, c_double, c_double, c_double, (c_double * 3)]
libspice.phaseq_c.argtypes = [c_double, c_char_p, c_char_p, c_char_p, c_char_p]
libspice.phaseq_c.restype = c_double
libspice.pi_c.restype = c_double
libspice.pjelpl_c.argtypes = [POINTER(stypes.Ellipse), POINTER(stypes.Plane), POINTER(stypes.Ellipse)]
libspice.pl2nvc_c.argtypes = [POINTER(stypes.Plane), (c_double * 3), POINTER(c_double)]
libspice.pl2nvp_c.argtypes = [POINTER(stypes.Plane), (c_double * 3), (c_double * 3)]
libspice.pl2psv_c.argtypes = [POINTER(stypes.Plane), (c_double * 3), (c_double * 3), (c_double * 3)]
libspice.pltar_c.argtypes = [c_int, c_void_p, c_int, c_void_p]
libspice.pltar_c.restype = c_double
libspice.pltexp_c.argtypes = [(c_double * 3) * 3, c_double, (c_double * 3) * 3]
libspice.pltnp_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3), (c_double * 3), (c_double * 3), POINTER(c_double)]
libspice.pltnrm_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3), (c_double * 3)]
libspice.pltvol_c.argtypes = [c_int, c_void_p, c_int, c_void_p]
libspice.pltvol_c.restype = c_double
libspice.polyds_c.argtype = [POINTER(c_double), c_int, c_int, c_double, POINTER(c_double)]
libspice.pos_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.pos_c.restype = c_int
libspice.posr_c.argtypes = [c_char_p, c_char_p, c_int]
libspice.posr_c.restype = c_int
# libspice.prefix_c.argtypes = [c_char_p, c_int, c_int, c_char_p]
libspice.prop2b_c.argtypes = [c_double, (c_double * 6), c_double, (c_double * 6)]
libspice.prsdp_c.argtypes = [c_char_p, POINTER(c_double)]
libspice.prsint_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.psv2pl_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3), POINTER(stypes.Plane)]
libspice.putcml_c.argtypes = [c_int, c_char_p]
libspice.pxform_c.argtypes = [c_char_p, c_char_p, c_double, (c_double * 3) * 3]
libspice.pxfrm2_c.argtypes = [c_char_p, c_char_p, c_double, c_double, (c_double * 3) * 3]

########################################################################################################################
# Q

libspice.q2m_c.argtypes = [c_double * 4, (c_double * 3) * 3]
libspice.qcktrc_c.argtypes = [c_int, c_char_p]
libspice.qdq2av_c.argtypes = [c_double * 4, c_double * 4, c_double * 3]
libspice.qxq_c.argtypes = [c_double * 4, c_double * 4, c_double * 4]

########################################################################################################################
# R
libspice.radrec_c.argtypes = [c_double, c_double, c_double, (c_double * 3)]
libspice.rav2xf_c.argtypes = [(c_double * 3) * 3, (c_double * 3), (c_double * 6) * 6]
libspice.raxisa_c.argtypes = [(c_double * 3) * 3, (c_double * 3), POINTER(c_double)]
libspice.rdtext_c.argtypes = [c_char_p, c_int, c_char_p, POINTER(c_bool)]
libspice.reccyl_c.argtypes = [(c_double * 3), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.recgeo_c.argtypes = [(c_double * 3), c_double, c_double, POINTER(c_double), POINTER(c_double),
                              POINTER(c_double)]
libspice.reclat_c.argtypes = [(c_double * 3), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.recpgr_c.argtypes = [c_char_p, (c_double * 3), c_double, c_double, POINTER(c_double), POINTER(c_double),
                              POINTER(c_double)]
libspice.recrad_c.argtypes = [(c_double * 3), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.recsph_c.argtypes = [(c_double * 3), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.reordc_c.argtypes = [POINTER(c_int), c_int, c_int, c_void_p]
libspice.reordd_c.argtypes = [POINTER(c_int), c_int, POINTER(c_double)]
libspice.reordi_c.argtypes = [POINTER(c_int), c_int, POINTER(c_int)]
libspice.reordl_c.argtypes = [POINTER(c_int), c_int, POINTER(c_bool)]
libspice.removc_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.removd_c.argtypes = [c_double, POINTER(stypes.SpiceCell)]
libspice.removi_c.argtypes = [c_int, POINTER(stypes.SpiceCell)]
libspice.repmc_c.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p]
libspice.repmct_c.argtypes = [c_char_p, c_char_p, c_int, c_char, c_int, c_char_p]
libspice.repmd_c.argtypes = [c_char_p, c_char_p, c_double, c_int, c_int, c_char_p]
libspice.repmf_c.argtypes = [c_char_p, c_char_p, c_double, c_int, c_char, c_int, c_char_p]
libspice.repmi_c.argtypes = [c_char_p, c_char_p, c_int, c_int, c_char_p]
libspice.repmot_c.argtypes = [c_char_p, c_char_p, c_int, c_char, c_int, c_char_p]
libspice.reset_c.argtypes = None
libspice.return_c.argtypes = None
libspice.return_c.restype = c_bool
libspice.rotate_c.argtypes = [c_double, c_int, (c_double * 3) * 3]
libspice.rotmat_c.argtypes = [(c_double * 3) * 3, c_double, c_int, (c_double * 3) * 3]
libspice.rotvec_c.argtypes = [(c_double * 3), c_double, c_int, (c_double * 3)]
libspice.rpd_c.restype = c_double
libspice.rquad_c.argtypes = [c_double, c_double, c_double, (c_double * 2), (c_double * 2)]

########################################################################################################################
# S

libspice.saelgv_c.argtypes = [(c_double * 3), (c_double * 3), (c_double * 3), (c_double * 3)]
libspice.scard_c.argtypes  = [c_int, POINTER(stypes.SpiceCell)]
libspice.scdecd_c.argtypes = [c_int, c_double, c_int, c_char_p]
libspice.sce2c_c.argtypes  = [c_int, c_double, POINTER(c_double)]
libspice.sce2s_c.argtypes  = [c_int, c_double, c_int, c_char_p]
libspice.sce2t_c.argtypes  = [c_int, c_double, POINTER(c_double)]
libspice.scencd_c.argtypes = [c_int, c_char_p, POINTER(c_double)]
libspice.scfmt_c.argtypes  = [c_int, c_double, c_int, c_char_p]
libspice.scpart_c.argtypes = [c_int, POINTER(c_int), POINTER(c_double), POINTER(c_double)]
libspice.scs2e_c.argtypes  = [c_int, c_char_p, POINTER(c_double)]
libspice.sct2e_c.argtypes  = [c_int, c_double, POINTER(c_double)]
libspice.sctiks_c.argtypes = [c_int, c_char_p, POINTER(c_double)]
libspice.sdiff_c.argtypes  = [POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.set_c.argtypes    = [POINTER(stypes.SpiceCell), c_char_p, POINTER(stypes.SpiceCell)]
libspice.set_c.restype     = c_bool
libspice.setmsg_c.argtypes = [c_char_p]
libspice.shellc_c.argtypes = [c_int, c_int, c_void_p]
libspice.shelld_c.argtypes = [c_int, POINTER(c_double)]
libspice.shelli_c.argtypes = [c_int, POINTER(c_int)]
libspice.sigerr_c.argtypes = [c_char_p]
libspice.sincpt_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, c_char_p, (c_double * 3),
                              (c_double * 3), POINTER(c_double), (c_double * 3), POINTER(c_bool)]
libspice.spd_c.restype     = c_double
libspice.sphcyl_c.argtypes = [c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.sphlat_c.argtypes = [c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.sphrec_c.argtypes = [c_double, c_double, c_double, (c_double * 3)]
libspice.spk14a_c.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double)]
libspice.spk14b_c.argtypes = [c_int, c_char_p, c_int, c_int, c_char_p, c_double, c_double, c_int]
libspice.spk14e_c.argtypes = [c_int]
libspice.spkacs_c.argtypes = [c_int, c_double, c_char_p, c_char_p, c_int, (c_double * 6), POINTER(c_double),
                              POINTER(c_double)]
libspice.spkapo_c.argtypes = [c_int, c_double, c_char_p, (c_double * 6), c_char_p, (c_double * 3), POINTER(c_double)]
libspice.spkapp_c.argtypes = [c_int, c_double, c_char_p, (c_double * 6), c_char_p, (c_double * 6), POINTER(c_double)]
libspice.spkaps_c.argtypes = [c_int, c_double, c_char_p, c_char_p, (c_double * 6), (c_double * 6), (c_double * 6),
                              POINTER(c_double), POINTER(c_double)]
libspice.spkcls_c.argtypes = [c_int]
libspice.spkcov_c.argtypes = [c_char_p, c_int, POINTER(stypes.SpiceCell)]
libspice.spkcpo_c.argtypes = [c_char_p, c_double, c_char_p, c_char_p, c_char_p,
                              (c_double * 3), c_char_p, c_char_p, (c_double * 6),
                              POINTER(c_double)]
libspice.spkcpt_c.argtypes = [(c_double * 3), c_char_p, c_char_p, c_double, c_char_p,
                              c_char_p, c_char_p, c_char_p, (c_double * 6),
                              POINTER(c_double)]
libspice.spkcvo_c.argtypes = [c_char_p, c_double, c_char_p, c_char_p, c_char_p,
                              (c_double * 6), c_double, c_char_p, c_char_p,
                              (c_double * 6), POINTER(c_double)]
libspice.spkcvt_c.argtypes = [(c_double * 6), c_double, c_char_p, c_char_p, c_double,
                              c_char_p, c_char_p, c_char_p, c_char_p, (c_double * 6),
                              POINTER(c_double)]
libspice.spkez_c.argtypes  = [c_int, c_double, c_char_p, c_char_p, c_int, (c_double * 6), POINTER(c_double)]
libspice.spkezp_c.argtypes = [c_int, c_double, c_char_p, c_char_p, c_int, (c_double * 3), POINTER(c_double)]
libspice.spkezr_c.argtypes = [c_char_p, c_double, c_char_p, c_char_p, c_char_p, (c_double * 6), POINTER(c_double)]
libspice.spkgeo_c.argtypes = [c_int, c_double, c_char_p, c_int, (c_double * 6), POINTER(c_double)]
libspice.spkgps_c.argtypes = [c_int, c_double, c_char_p, c_int, (c_double * 3), POINTER(c_double)]
libspice.spklef_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.spkltc_c.argtypes = [c_int, c_double, c_char_p, c_char_p, (c_double * 6), (c_double * 6), POINTER(c_double),
                              POINTER(c_double)]
libspice.spkobj_c.argtypes = [c_char_p, POINTER(stypes.SpiceCell)]
libspice.spkopa_c.argtypes = [c_char_p, POINTER(c_int)]
libspice.spkopn_c.argtypes = [c_char_p, c_char_p, c_int, POINTER(c_int)]
libspice.spkpds_c.argtypes = [c_int, c_int, c_char_p, c_int, c_double, c_double, (c_double * 5)]
libspice.spkpos_c.argtypes = [c_char_p, c_double, c_char_p, c_char_p, c_char_p, (c_double * 3), POINTER(c_double)]
libspice.spkpvn_c.argtypes = [c_int, (c_double * 5), c_double, POINTER(c_int),
                              (c_double * 6), POINTER(c_int)]
libspice.spksfs_c.argtypes = [c_int, c_double, c_int, POINTER(c_int),
                              (c_double * 5), c_char_p, POINTER(c_bool)]
libspice.spkssb_c.argtypes = [c_int, c_double, c_char_p, (c_double * 6)]
libspice.spksub_c.argtypes = [c_int, (c_double * 5), c_char_p, c_double, c_double, c_int]
libspice.spkuds_c.argtypes = [(c_double * 5), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int),
                              POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_int)]
libspice.spkuef_c.argtypes = [c_int]
libspice.spkw02_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_double, c_int, c_int,
                              POINTER(c_double), c_double]
libspice.spkw03_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_double, c_int, c_int,
                              POINTER(c_double), c_double]
libspice.spkw05_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_double, c_int,
                              POINTER(c_double * 6), POINTER(c_double)]
libspice.spkw08_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_int, c_int,
                              POINTER(c_double * 6), c_double, c_double]
libspice.spkw09_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_int, c_int,
                              POINTER(c_double * 6), POINTER(c_double)]
libspice.spkw10_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, (c_double * 8), c_int,
                              POINTER(c_double), POINTER(c_double)]
libspice.spkw12_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_int, c_int,
                              POINTER(c_double * 6), c_double, c_double]
libspice.spkw13_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_int, c_int,
                              POINTER(c_double * 6), POINTER(c_double)]
libspice.spkw15_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_double, (c_double * 3),
                              (c_double * 3), c_double, c_double, c_double, (c_double * 3), c_double, c_double,
                              c_double]
libspice.spkw17_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_double, (c_double * 9),
                              c_double, c_double]
libspice.spkw18_c.argtypes = [c_int, c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_int, c_int, c_void_p, POINTER(c_double)]
libspice.spkw20_c.argtypes = [c_int, c_int, c_int, c_char_p, c_double, c_double, c_char_p, c_double, c_int, c_int, POINTER(c_double), c_double, c_double, c_double, c_double]
libspice.srfc2s_c.argtypes = [c_int, c_int, c_int, c_char_p, POINTER(c_bool)]
libspice.srfcss_c.argtypes = [c_int, c_char_p, c_int, c_char_p, POINTER(c_bool)]
libspice.srfnrm_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_int, c_void_p, c_void_p]
libspice.srfrec_c.argtypes = [c_int, c_double, c_double, (c_double * 3)]
libspice.srfs2c_c.argtypes = [c_char_p, c_char_p, POINTER(c_int), POINTER(c_bool)]
libspice.srfscc_c.argtypes = [c_char_p, c_int, POINTER(c_int), POINTER(c_bool)]
libspice.size_c.argtypes   = [POINTER(stypes.SpiceCell)]
libspice.size_c.restype    = c_int
libspice.srfxpt_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, (c_double * 3),
                              (c_double * 3), POINTER(c_double), POINTER(c_double), (c_double * 3), POINTER(c_bool)]
libspice.ssize_c.argtypes  = [c_int, POINTER(stypes.SpiceCell)]
libspice.stelab_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.stpool_c.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, POINTER(c_int), POINTER(c_bool)]
libspice.str2et_c.argtypes = [c_char_p, POINTER(c_double)]
libspice.subpnt_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, (c_double * 3),
                              POINTER(c_double), (c_double * 3)]
libspice.subpt_c.argtypes  = [c_char_p, c_char_p, c_double, c_char_p, c_char_p, (c_double * 3), POINTER(c_double)]
libspice.subslr_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, (c_double * 3),
                              POINTER(c_double), (c_double * 3)]
libspice.subsol_c.argtypes = [c_char_p, c_char_p, c_double, c_char_p, c_char_p, (c_double * 3)]
libspice.sumai_c.argtypes  = [POINTER(c_int), c_int]
libspice.sumai_c.restype   = c_int
libspice.sumad_c.argtypes  = [POINTER(c_double), c_int]
libspice.sumad_c.restype   = c_double
libspice.surfnm_c.argtypes = [c_double, c_double, c_double, (c_double * 3), (c_double * 3)]
libspice.surfpt_c.argtypes = [(c_double * 3), (c_double * 3), c_double, c_double,
                              c_double, (c_double * 3), POINTER(c_bool)]
libspice.surfpv_c.argtypes = [(c_double * 6), (c_double * 6), c_double, c_double, c_double, (c_double * 6),
                              POINTER(c_bool)]
libspice.swpool_c.argtypes = [c_char_p, c_int, c_int, c_void_p]
libspice.sxform_c.argtypes = [c_char_p, c_char_p, c_double, (c_double * 6) * 6]
libspice.szpool_c.argtypes = [c_char_p, POINTER(c_int), POINTER(c_bool)]

########################################################################################################################
# T

libspice.termpt_c.argtypes = [c_char_p, c_char_p, c_char_p, c_double, c_char_p, c_char_p, c_char_p, c_char_p, (c_double * 3), c_double, c_int, c_double, c_double, c_int, POINTER(c_int), c_void_p, POINTER(c_double), c_void_p]
libspice.timdef_c.argtypes = [c_char_p, c_char_p, c_int, c_char_p]
libspice.timout_c.argtypes = [c_double, c_char_p, c_int, c_char_p]
libspice.tipbod_c.argtypes = [c_char_p, c_int, c_double, (c_double * 3) * 3]
libspice.tisbod_c.argtypes = [c_char_p, c_int, c_double, (c_double * 6) * 6]
libspice.tkvrsn_c.argtypes = [c_char_p]
libspice.tkvrsn_c.restype  = c_char_p
libspice.tparse_c.argtypes = [c_char_p, c_int, POINTER(c_double), c_char_p]
libspice.tpictr_c.argtypes = [c_char_p, c_int, c_int, c_char_p, POINTER(c_bool), c_char_p]
libspice.trace_c.argtypes  = [(c_double * 3) * 3]
libspice.trace_c.restype   = c_double
libspice.trcdep_c.argtypes = [POINTER(c_int)]
libspice.trcnam_c.argtypes = [c_int, c_int, c_char_p]
libspice.trcoff_c.argtypes = None
libspice.tsetyr_c.argtypes = [c_int]
libspice.twopi_c.restype   = c_double
libspice.twovec_c.argtypes = [(c_double * 3), c_int, (c_double * 3), c_int, (c_double * 3) * 3]
libspice.txtopn_.argtypes   = [c_char_p, POINTER(c_int), c_int]
libspice.tyear_c.restype   = c_double

########################################################################################################################
# U

libspice.ucase_c.argtypes  = [c_char_p, c_int, c_char_p]
libspice.ucrss_c.argtypes  = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.uddc_c.argtypes   = [callbacks.UDFUNS, c_double, c_double, POINTER(c_bool)]
libspice.uddc_c.restype    = None
libspice.uddf_c.argtypes   = [callbacks.UDFUNS, c_double, c_double, POINTER(c_double)]
libspice.uddf_c.restype    = None
libspice.udf_c.argtypes    = [c_double, POINTER(c_double)]
libspice.udf_c.restype     = None
libspice.union_c.argtypes  = [POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.unitim_c.argtypes = [c_double, c_char_p, c_char_p]
libspice.unitim_c.restype  = c_double
libspice.unload_c.argtypes = [c_char_p]
libspice.unorm_c.argtypes  = [(c_double * 3), (c_double * 3), POINTER(c_double)]
libspice.unormg_c.argtypes = [POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double)]
libspice.utc2et_c.argtypes = [c_char_p, POINTER(c_double)]
########################################################################################################################
# V

libspice.vadd_c.argtypes   = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vaddg_c.argtypes  = [POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double)]
libspice.valid_c.argtypes  = [c_int, c_int, POINTER(stypes.SpiceCell)]
libspice.vcrss_c.argtypes  = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vdist_c.argtypes  = [(c_double * 3), (c_double * 3)]
libspice.vdist_c.restype   = c_double
libspice.vdistg_c.argtypes = [POINTER(c_double), POINTER(c_double), c_int]
libspice.vdistg_c.restype  = c_double
libspice.vdot_c.argtypes   = [(c_double * 3), (c_double * 3)]
libspice.vdot_c.restype    = c_double
libspice.vdotg_c.argtypes  = [POINTER(c_double), POINTER(c_double), c_int]
libspice.vdotg_c.restype   = c_double
libspice.vequ_c.argtypes   = [(c_double * 3), (c_double * 3)]
libspice.vequg_c.argtypes  = [POINTER(c_double), c_int, POINTER(c_double)]
libspice.vhat_c.argtypes   = [(c_double * 3), (c_double * 3)]
libspice.vhatg_c.argtypes  = [POINTER(c_double), c_int, POINTER(c_double)]
libspice.vlcom_c.argtypes  = [c_double, (c_double * 3), c_double, (c_double * 3), (c_double * 3)]
libspice.vlcom3_c.argtypes = [c_double, (c_double * 3), c_double, (c_double * 3), c_double, (c_double * 3),
                              (c_double * 3)]
libspice.vlcomg_c.argtypes = [c_int, c_double, POINTER(c_double), c_double, POINTER(c_double), POINTER(c_double)]
libspice.vminug_c.argtypes = [POINTER(c_double), c_int, POINTER(c_double)]
libspice.vminus_c.argtypes = [(c_double * 3), (c_double * 3)]
libspice.vnorm_c.restype   = c_double
libspice.vnorm_c.argstype  = [stypes.emptyDoubleVector(3)]
libspice.vnormg_c.restype  = c_double
libspice.vnormg_c.argstype = [POINTER(c_double), c_int]
libspice.vpack_c.argtypes  = [c_double, c_double, c_double, (c_double * 3)]
libspice.vperp_c.argtypes  = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vprjp_c.argtypes  = [(c_double * 3), POINTER(stypes.Plane), (c_double * 3)]
libspice.vprjpi_c.argtypes = [(c_double * 3), POINTER(stypes.Plane), POINTER(stypes.Plane), (c_double * 3),
                              POINTER(c_bool)]
libspice.vproj_c.argtypes  = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vrelg_c.argtypes  = [POINTER(c_double), POINTER(c_double), c_int]
libspice.vrelg_c.restype   = c_double
libspice.vrel_c.argtypes   = [(c_double * 3), (c_double * 3)]
libspice.vrel_c.restype    = c_double
libspice.vrotv_c.argtypes  = [(c_double * 3), (c_double * 3), c_double, (c_double * 3)]
libspice.vscl_c.argtypes   = [c_double, (c_double * 3), (c_double * 3)]
libspice.vsclg_c.argtypes  = [c_double, POINTER(c_double), c_int, POINTER(c_double)]
libspice.vsep_c.argtypes   = [(c_double * 3), (c_double * 3)]
libspice.vsep_c.restype    = c_double
libspice.vsepg_c.argtypes  = [POINTER(c_double), POINTER(c_double), c_int]
libspice.vsepg_c.restype   = c_double
libspice.vsub_c.argtypes   = [(c_double * 3), (c_double * 3), (c_double * 3)]
libspice.vsubg_c.argtypes  = [POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double)]
libspice.vtmv_c.argtypes   = [(c_double * 3), (c_double * 3) * 3, (c_double * 3)]
libspice.vtmv_c.restype    = c_double
libspice.vtmvg_c.argtypes  = [POINTER(c_double), c_void_p, POINTER(c_double), c_int, c_int]
libspice.vtmvg_c.restype   = c_double
libspice.vupack_c.argtypes = [(c_double * 3), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
libspice.vzero_c.argtypes  = [(c_double * 3)]
libspice.vzero_c.restype   = c_bool
libspice.vzerog_c.argtypes = [POINTER(c_double), c_int]
libspice.vzerog_c.restype  = c_bool

########################################################################################################################
# W
libspice.wncard_c.argtypes = [POINTER(stypes.SpiceCell)]
libspice.wncard_c.restype  = c_int
libspice.wncomd_c.argtypes = [c_double, c_double, POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.wncond_c.argtypes = [c_double, c_double, POINTER(stypes.SpiceCell)]
libspice.wndifd_c.argtypes = [POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.wnelmd_c.argtypes = [c_double, POINTER(stypes.SpiceCell)]
libspice.wnelmd_c.restype  = c_bool
libspice.wnexpd_c.argtypes = [c_double, c_double, POINTER(stypes.SpiceCell)]
libspice.wnextd_c.argtypes = [c_char, POINTER(stypes.SpiceCell)]
libspice.wnfetd_c.argtypes = [POINTER(stypes.SpiceCell), c_int, POINTER(c_double), POINTER(c_double)]
libspice.wnfild_c.argtypes = [c_double, POINTER(stypes.SpiceCell)]
libspice.wnfltd_c.argtypes = [c_double, POINTER(stypes.SpiceCell)]
libspice.wnincd_c.argtypes = [c_double, c_double, POINTER(stypes.SpiceCell)]
libspice.wnincd_c.restype  = c_bool
libspice.wninsd_c.argtypes = [c_double, c_double, POINTER(stypes.SpiceCell)]
libspice.wnintd_c.argtypes = [POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.wnreld_c.argtypes = [POINTER(stypes.SpiceCell), c_char_p, POINTER(stypes.SpiceCell)]
libspice.wnreld_c.restype  = c_bool
libspice.wnsumd_c.argtypes = [POINTER(stypes.SpiceCell), POINTER(c_double), POINTER(c_double), POINTER(c_double),
                              POINTER(c_int), POINTER(c_int)]
libspice.wnunid_c.argtypes = [POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell), POINTER(stypes.SpiceCell)]
libspice.wnvald_c.argtypes = [c_int, c_int, POINTER(stypes.SpiceCell)]
libspice.writln_.argtypes = [c_char_p, POINTER(c_int), c_int]
########################################################################################################################
# X

libspice.xf2eul_c.argtypes = [(c_double * 6) * 6, c_int, c_int, c_int, (c_double * 6), POINTER(c_bool)]
libspice.xf2rav_c.argtypes = [(c_double * 6) * 6, (c_double * 3) * 3, (c_double * 3)]
libspice.xfmsta_c.argtypes = [(c_double * 6), c_char_p, c_char_p, c_char_p, (c_double * 6)]
libspice.xpose_c.argtypes  = [(c_double * 3) * 3, (c_double * 3) * 3]
libspice.xpose6_c.argtypes = [(c_double * 6) * 6, (c_double * 6) * 6]
libspice.xposeg_c.argtypes = [c_void_p, c_int, c_int, c_void_p]
########################################################################################################################
# Z

libspice.zzgetcml_c.argtypes = [c_int, c_char_p, c_bool]
libspice.zzgfsavh_c.argtypes = [c_bool]
#libspice.zzsynccl_c.argtypes = [None]
