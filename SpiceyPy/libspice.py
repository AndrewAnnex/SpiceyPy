__author__ = 'Apollo117'
import ctypes
libspice = ctypes.CDLL('spice.so')

import SpiceyPy.SupportTypes as stypes

##########################################################################################################################################################
# A

#libspice.appndc_c.argtypes = [ctypes.c_char_p, None]
#libspice.appndd_c.argtypes = [ctypes.c_double, None]
#libspice.appndi_c.argtypes = [ctypes.c_int, None]
libspice.axisar_c.argtypes = [(ctypes.c_double * 3), ctypes.c_double, (ctypes.c_double * 3)*3]

##########################################################################################################################################################
# B
libspice.b1900_c.restype = ctypes.c_double
libspice.b1950_c.restype = ctypes.c_double
libspice.bodc2n_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)]
libspice.bodc2s_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.boddef_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.badkpv_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.badkpv_c.restype = ctypes.c_bool
libspice.bodfnd_c.argtypes = [ctypes.c_int, ctypes.c_char_p]
libspice.bodfnd_c.restype = ctypes.c_bool
libspice.bodn2c_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_bool)]
libspice.bods2c_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_bool)]
libspice.bodvar_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), (ctypes.c_double * 3)] # last one is some vector.. work on this
libspice.bodvcd_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_double]
libspice.bodvrd_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), (ctypes.c_double * 3)]
libspice.brcktd_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.brcktd_c.restype = ctypes.c_double
libspice.brckti_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.brckti_c.restype = ctypes.c_int
libspice.bschoc_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_int)]
libspice.bschoc_c.restype = ctypes.c_int
libspice.bschoi_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
libspice.bschoi_c.restype = ctypes.c_int
libspice.bsrchc_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
libspice.bsrchc_c.restype = ctypes.c_int
libspice.bsrchd_c.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.bsrchd_c.restype = ctypes.c_int
libspice.bsrchi_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
libspice.bsrchi_c.restype = ctypes.c_int
##########################################################################################################################################################
# C



#libspice.cgv2el_c.argtypes = []
libspice.chkin_c.argtypes = [ctypes.c_char_p]
libspice.chkout_c.argtypes = [ctypes.c_char_p]
libspice.cidfrm_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool]
libspice.ckcls_c.argtypes = [ctypes.c_int]
#libspice.ckcov_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, None]
#libspice.ckobj_c.argtypes = [ctypes.c_char_p, None]
libspice.ckgp_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_bool]
libspice.ckgpav_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool]
libspice.cklpf_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.ckopn_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
libspice.ckupf_c.argtypes = [ctypes.c_int]
libspice.ckw01_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p, ctypes.c_int]
libspice.ckw02_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
libspice.ckw03_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
libspice.ckw05_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_int]
#libspice.clpool_c.argtypes = []
libspice.cmprss_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.cnmfrm_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool]
libspice.conics_c.argtypes = [ctypes.c_double, ctypes.c_double]
libspice.convrt_c.argtypes = [ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double]
#libspice.copy_c.argtypes = [None, None]
libspice.cvpool_c.argtypes = [ctypes.c_char_p, ctypes.c_bool]
libspice.cyllat_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.cylrec_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.cylsph_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]

##########################################################################################################################################################
#D

libspice.dafac_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.dafbbs_c.argtypes = [ctypes.c_int]
libspice.dafbfs_c.argtypes = [ctypes.c_int]
libspice.dafcls_c.argtypes = [ctypes.c_int]
libspice.dafcs_c.argtypes = [ctypes.c_int]
libspice.dafdc_c.argtypes = [ctypes.c_int]
libspice.dafec_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
libspice.daffna_c.argtypes = [ctypes.c_bool]
libspice.daffpa_c.argtypes = [ctypes.c_bool]
libspice.dafgda_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double]
#libspice.dafgh_c.argtypes = [ctypes.c_int]
libspice.dafgn_c.argtypes = [ctypes.c_int, ctypes.c_char_p]
libspice.dafgs_c.argtypes = [ctypes.c_double]
libspice.dafgsr_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_bool]
libspice.dafopr_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.dafopw_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.dafps_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double]
libspice.dafrda_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double]
libspice.dafrfr_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
#libspice.dafrs_c.argtype = []
libspice.dafus_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_int]
libspice.dasac_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.dascls_c.argtypes = [ctypes.c_int]
libspice.dasec_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
libspice.dasopr_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.dcyldr_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.deltet_c.argtypes = [ctypes.c_double, ctypes.c_char_p, ctypes.c_double]
libspice.diags2_c.argtypes = [ctypes.c_double, ctypes.c_double]
#libspice.diff_c.argtypes = [None, None, None]
libspice.dgeodr_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.dlatdr_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.dp2hx_c.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
libspice.dpgrdr_c.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.dpr_c.restype = ctypes.c_double
libspice.drdcyl_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.drdgeo_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.drdlat_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.drdpgr_c.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.drdsph_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.dsphdr_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.dtpool_c.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_int, ctypes.c_char_p]
libspice.ducrss_c.argtypes = [ctypes.c_double]
libspice.dvcrss_c.argtypes = [ctypes.c_double]
libspice.dvhat_c.argtypes = [ctypes.c_double]
libspice.dvpool_c.argtypes = [ctypes.c_char_p]
##########################################################################################################################################################
# E

libspice.edlimb_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.ekacec_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
libspice.ekaced_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_bool]
libspice.ekacei_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_bool]
libspice.ekaclc_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
libspice.ekacld_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
libspice.ekacli_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
libspice.ekappr_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.ekbseg_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.ekccnt_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.ekcii_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.ekcls_c.argtypes = [ctypes.c_int]
libspice.ekdelr_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.ekffld_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.ekfind_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
libspice.ekgc_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool]
libspice.ekgd_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_bool, ctypes.c_bool]
libspice.ekgi_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_bool]
libspice.ekifld_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.ekinsr_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.eklef_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.ekntab_c.argtypes = [ctypes.c_int]
libspice.ekopn_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
libspice.ekopr_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.ekops_c.argtypes = [ctypes.c_int]
libspice.ekopw_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.ekpsel_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]
libspice.ekrcec_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
libspice.ekrced_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_bool]
libspice.ekrcei_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
libspice.ekssum_c.argtypes = [ctypes.c_int, ctypes.c_int]
libspice.ektnam_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.ekucec_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int,  ctypes.c_bool]
libspice.ekuced_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_bool]
libspice.ekucei_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_bool]
libspice.ekuef_c.argtypes = [ctypes.c_int]
libspice.el2cgv_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.erract_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.errch_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
libspice.errdev_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.errdp_c.argtypes = [ctypes.c_char_p, ctypes.c_double]
libspice.errint_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.errprt_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.etcal_c.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.c_char_p]
libspice.et2lst_c.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
libspice.et2utc_c.argtypes = [ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.eul2m_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double]
libspice.eul2xf_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double]
libspice.expool_c.argtypes = [ctypes.c_char_p, ctypes.c_bool]

##########################################################################################################################################################
# F

libspice.frame_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.frinfo_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
libspice.frmnam_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.ftncls_c.argtypes = [ctypes.c_int]
libspice.furnsh_c.argtypes = [ctypes.c_char_p]

##########################################################################################################################################################
# G

libspice.gcpool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
libspice.gdpool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_bool]
libspice.georec_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,  ctypes.c_double]
libspice.getcml_c.argtypes = [ctypes.c_int, ctypes.c_char_p]
libspice.getelm_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
libspice.getfat_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
libspice.getfov_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double * 3), ctypes.POINTER(ctypes.c_int), (ctypes.c_double * 3) * 4]
libspice.getmsg_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
#libspice.gfclrh_c.argtypes = []
#libspice.gfdist_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, None, None]
#libspice.gfevnt_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool, None, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_bool, ctypes.c_bool, None, None]
#libspice.gffove_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,  ctypes.c_double, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_bool, None,  ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double,  ctypes.c_bool, ctypes.c_bool, None, None]
#libspice.gfinth_c.argtypes = []
#libspice.gfocce_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool, ctypes.c_bool, ctypes.c_double, ctypes.c_bool, None, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool, ctypes.c_bool, None, None]
#libspice.gfoclt_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, None,None]
#libspice.gfposc_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double,  ctypes.c_int, None, None]
libspice.gfrefn_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_bool, ctypes.c_bool, ctypes.c_double]
#libspice.gfrepf_c.argtypes = []
#libspice.gfrepi_c.argtypes = [None, ctypes.c_char_p, ctypes.c_char_p]
libspice.gfrepu_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
# libspice.gfrfov_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, None,  None]
# libspice.gfrr_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, None, None]
# libspice.gfsep_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,  ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, None, None]
# libspice.gfsntc_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double,  ctypes.c_double, ctypes.c_double, ctypes.c_int, None, None]
libspice.gfsstp_c.argtypes = [ctypes.c_double]
libspice.gfstep_c.argtypes = [ctypes.c_double, ctypes.c_double]
# libspice.gfsubc_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, None, None]
# libspice.gftfov_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, None, None]
# libspice.gfuds_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, None, None]
libspice.gipool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool]
libspice.gnpool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_bool]

##########################################################################################################################################################
# H

libspice.halfpi_c.restype = ctypes.c_double
libspice.hx2dp_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_bool), ctypes.c_char_p]

##########################################################################################################################################################
# I

libspice.ident_c.argtypes = [(ctypes.c_double*3)*3]
libspice.illum_c.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.ilumin_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double * 3), ctypes.POINTER(ctypes.c_double), (ctypes.c_double * 3), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.inedpl_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool]
libspice.inelpl_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double]
# libspice.insrtc_c.argtypes = [ctypes.c_char_p, None]
# libspice.insrtd_c.argtypes = [ctypes.c_double, None]
# libspice.insrti_c.argtypes = [ctypes.c_int, None]
# libspice.inter_c.argtypes = [None, None, None]
libspice.inrypl_c.argtypes = [ctypes.c_int, ctypes.c_double]
libspice.intmax_c.restype = ctypes.c_int
libspice.intmin_c.restype = ctypes.c_int
libspice.invert_c.argtypes = [(ctypes.c_double*3)*3, (ctypes.c_double*3)*3]
libspice.invort_c.argtypes = [(ctypes.c_double*3)*3, (ctypes.c_double*3)*3]
libspice.isordv_c.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
libspice.isordv_c.restype = ctypes.c_bool
libspice.isrchd_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.isrchd_c.restype = ctypes.c_int
libspice.isrchi_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
libspice.isrchi_c.restype = ctypes.c_int
libspice.isrot_c.argtypes = [(ctypes.c_double*3)*3, ctypes.c_double, ctypes.c_double]
libspice.isrot_c.restype = ctypes.c_bool
libspice.iswhsp_c.argtypes = [ctypes.c_char_p]
libspice.iswhsp_c.restype = ctypes.c_bool
##########################################################################################################################################################
# J

libspice.j1900_c.restype = ctypes.c_double
libspice.j1950_c.restype = ctypes.c_double
libspice.j2000_c.restype = ctypes.c_double
libspice.j2100_c.restype = ctypes.c_double
libspice.jyear_c.restype = ctypes.c_double

##########################################################################################################################################################
# K
libspice.kclear_c.restype = None
libspice.kdata_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_bool)]
libspice.kinfo_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_bool)]
libspice.ktotal_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
libspice.kxtrct_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p]

##########################################################################################################################################################
# L
libspice.lastnb_c.argtypes = [ctypes.c_char_p]
libspice.lastnb_c.restype = ctypes.c_int
libspice.latcyl_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.latrec_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.latsph_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.lcase_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.ldpool_c.argtypes = [ctypes.c_char_p]
libspice.lmpool_c.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
libspice.lparse_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
libspice.lparsm_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
#libspice.lparss_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, None]
libspice.lspcn_c.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p]
libspice.lspcn_c.restype = ctypes.c_double
libspice.ltime_c.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

libspice.lstlec_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.lstlec_c.restype = ctypes.c_int


libspice.lx4dec_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
libspice.lx4num_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
libspice.lx4sgn_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
libspice.lx4uns_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
libspice.lxqstr_c.argtypes = [ctypes.c_char_p, ctypes.c_char, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
##########################################################################################################################################################
# M

libspice.m2eul_c.argtypes = [(ctypes.c_double * 3)*3, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.m2q_c.argtypes = [(ctypes.c_double * 3)*3, (ctypes.c_double*4)]
libspice.matchi_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char, ctypes.c_char]
libspice.matchi_c.restype = ctypes.c_bool
libspice.matchw_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char, ctypes.c_char]
libspice.matchw_c.restype = ctypes.c_bool
libspice.mequ_c.argtypes = [(ctypes.c_double * 3)*3,(ctypes.c_double * 3)*3,]
libspice.mequg_c.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.mtxm_c.argtypes = [(ctypes.c_double * 3)*3, (ctypes.c_double * 3)*3, (ctypes.c_double * 3)*3]
libspice.mtxmg_c.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.mtxv_c.argtypes = [(ctypes.c_double*3)*3, (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.mtxvg_c.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.mxm_c.argtypes = [(ctypes.c_double*3)*3, (ctypes.c_double*3)*3, (ctypes.c_double*3)*3]
libspice.mxmg_c.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.mxmt_c.argtypes = [(ctypes.c_double*3)*3, (ctypes.c_double*3)*3, (ctypes.c_double*3)*3]
libspice.mxmtg_c.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.mxv_c.argtypes = [(ctypes.c_double*3)*3, (ctypes.c_double*3), (ctypes.c_double*3)]
libspice.mxvg_c.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]

##########################################################################################################################################################
# N

libspice.namfrm_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
libspice.ncpos_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
libspice.ncpos_c.restype = ctypes.c_int
libspice.ncposr_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
libspice.ncposr_c.restype = ctypes.c_int
libspice.nearpt_c.argtypes = [(ctypes.c_double*3), ctypes.c_double, ctypes.c_double, ctypes.c_double, (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double)]
libspice.npedln_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, (ctypes.c_double*3), (ctypes.c_double*3), (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double)]
libspice.npelpt_c.argtypes = [ctypes.c_double, ctypes.c_double]
libspice.nplnpt_c.argtypes = [(ctypes.c_double*3), (ctypes.c_double*3), (ctypes.c_double*3), (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double)]
libspice.nvc2pl_c.argtypes = [ctypes.c_double]
#libspice.nvp2pl_c.argtypes = []

##########################################################################################################################################################
# O
#ordc_c
#ordd_c
#ordi_c
libspice.orderc_c.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
libspice.orderd_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
libspice.orderi_c.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
libspice.oscelt_c.argtypes = [ctypes.c_double*6, ctypes.c_double, ctypes.c_double, ctypes.c_double*8]

##########################################################################################################################################################
# P

#libspice.pckcov_c.argtypes = [ctypes.c_char_p, ctypes.c_int, None]
#libspice.pckfrm_c.argtypes = [ctypes.c_char_p, None]
libspice.pcklof_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
libspice.pckuof_c.argtypes = [ctypes.c_int]
libspice.pcpool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.pdpool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.pipool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
libspice.pgrrec_c.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, (ctypes.c_double*3)]
libspice.pi_c.restype = ctypes.c_double
#libspice.pjelpl_c.argtypes = []
libspice.pl2nvc_c.argtypes = [ctypes.POINTER(stypes.Plane), (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double)]
libspice.pl2nvp_c.argtypes = [ctypes.c_double, ctypes.c_double]
libspice.pl2psv_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.pos_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
libspice.pos_c.restype = ctypes.c_int
libspice.posr_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
libspice.posr_c.restype = ctypes.c_int
#libspice.prefix_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.prop2b_c.argtypes = [ctypes.c_double, (ctypes.c_double*6), ctypes.c_double, (ctypes.c_double*6)]
libspice.prsdp_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
libspice.prsint_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
#libspice.psv2pl_c.argtypes = []
libspice.putcml_c.argtypes = [ctypes.c_int, ctypes.c_char_p]
libspice.pxform_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, (ctypes.c_double*3)*3]

##########################################################################################################################################################
# Q

libspice.q2m_c.argtypes = [ctypes.c_double * 4, (ctypes.c_double * 3)*3]
libspice.qdq2av_c.argtypes = [ctypes.c_double * 4, ctypes.c_double * 4, ctypes.c_double * 3]
libspice.qxq_c.argtypes = [ctypes.c_double]

##########################################################################################################################################################
# R
libspice.radrec_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, (ctypes.c_double*3)]
libspice.rav2xf_c.argtypes = [(ctypes.c_double * 3)*3, (ctypes.c_double * 3), (ctypes.c_double * 6)*6]
libspice.raxisa_c.argtypes = [(ctypes.c_double * 3)*3, (ctypes.c_double * 3), ctypes.POINTER(ctypes.c_double)]
libspice.rdtext_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool)]
libspice.reccyl_c.argtypes = [(ctypes.c_double * 3), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.recgeo_c.argtypes = [(ctypes.c_double * 3), ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.reclat_c.argtypes = [(ctypes.c_double * 3), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.recpgr_c.argtypes = [ctypes.c_char_p, (ctypes.c_double * 3), ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.recrad_c.argtypes = [(ctypes.c_double*3), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.recsph_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.reordc_c.argtypes = [ctypes.c_int, ctypes.c_int]
libspice.reordd_c.argtypes = [ctypes.c_int, ctypes.c_double]
libspice.reordi_c.argtypes = [ctypes.c_int, ctypes.c_int]
libspice.reordl_c.argtypes = [ctypes.c_int, ctypes.c_bool]
#libspice.removc_c.argtypes = [ctypes.c_char_p, None]
#libspice.removd_c.argtypes = [ctypes.c_double, None]
#libspice.removi_c.argtypes = [ctypes.c_int, None]
libspice.repmc_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.repmct_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.repmd_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.repmf_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.repmi_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
libspice.repmot_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.reset_c.argtypes = None
#skipping return_c
libspice.rotate_c.argtypes = [ctypes.c_double, ctypes.c_int, (ctypes.c_double*3)*3]
libspice.rotmat_c.argtypes = [(ctypes.c_double*3)*3, ctypes.c_double, ctypes.c_int, (ctypes.c_double*3)*3]
libspice.rotvec_c.argtypes = [(ctypes.c_double*3), ctypes.c_double, ctypes.c_int, (ctypes.c_double*3)]
libspice.rpd_c.restype = ctypes.c_double
libspice.rquad_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, (ctypes.c_double*2), (ctypes.c_double*2)]

##########################################################################################################################################################
# S

libspice.saelgv_c.argtypes = [(ctypes.c_double*3), (ctypes.c_double*3), (ctypes.c_double*3), (ctypes.c_double*3)]
#libspice.scard_c.argtypes = [ctypes.c_int, None]
libspice.scdecd_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_char_p]
libspice.sce2c_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
libspice.sce2s_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_char_p]
libspice.sce2t_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
libspice.scencd_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
libspice.scfmt_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_char_p]
libspice.scpart_c.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

libspice.scs2e_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
libspice.sct2e_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
libspice.sctiks_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
#libspice.sdiff_c.argtypes = [None, None, None]
libspice.setmsg_c.argtypes = [ctypes.c_char_p]
libspice.shellc_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.shelld_c.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.shelli_c.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
libspice.sigerr_c.argtypes = [ctypes.c_char_p]
libspice.sincpt_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double * 3), (ctypes.c_double * 3), ctypes.POINTER(ctypes.c_double), (ctypes.c_double * 3), ctypes.POINTER(ctypes.c_bool)]
libspice.spd_c.restype = ctypes.c_double
libspice.sphcyl_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.sphlat_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.sphrec_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, (ctypes.c_double*3)]
libspice.spk14a_c.argtypes = [ctypes.c_int, ctypes.c_int]
libspice.spk14b_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_int]
libspice.spk14e_c.argtypes = [ctypes.c_int]
libspice.spkapo_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double]
libspice.spkapp_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double]
libspice.spkcls_c.argtypes = [ctypes.c_int]
#libspice.spkcov_c.argtypes = [ctypes.c_char_p, ctypes.c_int, None]
libspice.spkacs_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.spkaps_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.spkez_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_double]
libspice.spkezp_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_double]
libspice.spkezr_c.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double]
libspice.spkgeo_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_double]
libspice.spkgps_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_double,ctypes.c_double]
libspice.spklef_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.spkltc_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]
#libspice.spkobj_c.argtypes = [ctypes.c_char_p, None]
libspice.spkopa_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
libspice.spkopn_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
libspice.spkpds_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.spkpos_c.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,  ctypes.c_double, ctypes.c_double]
libspice.spkssb_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_double]
libspice.spksub_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_double,  ctypes.c_int]
libspice.spkuds_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double,   ctypes.c_int, ctypes.c_int]
libspice.spkuef_c.argtypes = [ctypes.c_int]
libspice.spkw02_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double,  ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_int, ctypes.c_int,  ctypes.c_double]
libspice.spkw03_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double,  ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_int, ctypes.c_int,  ctypes.c_double]
libspice.spkw05_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double,  ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_int]
libspice.spkw08_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double,ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_double,  ctypes.c_double]
libspice.spkw09_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
libspice.spkw10_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_char_p, ctypes.c_int]
libspice.spkw12_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double,  ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_double,  ctypes.c_double]
libspice.spkw13_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double,  ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
libspice.spkw15_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double,  ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.spkw17_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]
libspice.spkw18_c.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
libspice.srfrec_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double]

libspice.srfxpt_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double*3), (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), (ctypes.c_double*3), ctypes.POINTER(ctypes.c_bool)]
#libspice.ssize_c.argtypes = [ctypes.c_int, None]
libspice.stelab_c.argtypes = [(ctypes.c_double*3), (ctypes.c_double*3)]
libspice.stpool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_bool)]
libspice.str2et_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
libspice.subpnt_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double), (ctypes.c_double*3)]
libspice.subpt_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double)]
libspice.subslr_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double*3), ctypes.POINTER(ctypes.c_double), (ctypes.c_double*3)]
libspice.subsol_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p, (ctypes.c_double*3)]
libspice.sumai_c.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
libspice.sumai_c.restype = ctypes.c_int
libspice.sumad_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
libspice.sumad_c.restype = ctypes.c_double
libspice.surfnm_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double,(ctypes.c_double*3), (ctypes.c_double*3)]
libspice.surfpt_c.argtypes = [(ctypes.c_double*3), (ctypes.c_double*3), ctypes.c_double, (ctypes.c_double*3), ctypes.POINTER(ctypes.c_bool)]
libspice.surfpv_c.argtypes = [(ctypes.c_double*6), (ctypes.c_double*6), ctypes.c_double, (ctypes.c_double*6), ctypes.POINTER(ctypes.c_bool)]
libspice.swpool_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
libspice.sxform_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, (ctypes.c_double*6)*6]
libspice.szpool_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_bool)]

##########################################################################################################################################################
# T

libspice.timdef_c.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.timout_c.argtypes = [ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.tipbod_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_double, ctypes.c_double]
libspice.tisbod_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_double, (ctypes.c_double * 6)*6]
libspice.tkvrsn_c.argtypes = [ctypes.c_char_p]
libspice.tkvrsn_c.restype = ctypes.c_char_p
libspice.tparse_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_char_p]
libspice.tpictr_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_bool), ctypes.c_char_p]
libspice.trace_c.argtypes = [ctypes.c_double * 3]
libspice.trace_c.restype = ctypes.c_double
libspice.trcoff_c.argtypes = None
libspice.tsetyr_c.argtypes = [ctypes.c_int]
libspice.twopi_c.restype = ctypes.c_double
libspice.twovec_c.argtypes = [(ctypes.c_double * 3), ctypes.c_int, (ctypes.c_double * 3), ctypes.c_int, (ctypes.c_double * 3)*3]
libspice.tyear_c.restype = ctypes.c_double

##########################################################################################################################################################
# U

libspice.ucase_c.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
libspice.ucrss_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.uddc_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_bool]
libspice.uddf_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
#libspice.union_c.argtypes = [None, None, None]
libspice.unitim_c.argtypes = [ctypes.c_double, ctypes.c_char_p, ctypes.c_char_p]
libspice.unitim_c.restype = ctypes.c_double
libspice.unload_c.argtypes = [ctypes.c_char_p]
libspice.unorm_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), ctypes.POINTER(ctypes.c_double)]
libspice.unormg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.utc2et_c.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
##########################################################################################################################################################
# V

libspice.vadd_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vaddg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
#libspice.valid_c.argtypes = [ctypes.c_int, ctypes.c_int, None]
libspice.vcrss_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vdist_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vdist_c.restype = ctypes.c_double
libspice.vdistg_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), ctypes.c_int]
libspice.vdistg_c.restype = ctypes.c_double
libspice.vdot_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vdot_c.restype = ctypes.c_double
libspice.vdotg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
libspice.vdotg_c.restype = ctypes.c_double
libspice.vequ_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vequg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.vhat_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vhatg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.vlcom_c.argtypes = [ctypes.c_double, (ctypes.c_double * 3), ctypes.c_double, (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vlcom3_c.argtypes = [ctypes.c_double, (ctypes.c_double * 3), ctypes.c_double, (ctypes.c_double * 3), ctypes.c_double, (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vlcomg_c.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.vminug_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.vminus_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vnorm_c.restype = ctypes.c_double
libspice.vnorm_c.argstype = [stypes.doubleVector(3)]
libspice.vnormg_c.restype = ctypes.c_double
libspice.vnormg_c.argstype = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
libspice.vpack_c.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, (ctypes.c_double * 3)]
libspice.vperp_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vprjp_c.argtypes = [ctypes.c_double]
libspice.vprjpi_c.argtypes = [ctypes.c_double, ctypes.c_bool]
libspice.vproj_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vrelg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
libspice.vrelg_c.restype = ctypes.c_double
libspice.vrel_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vrel_c.restype = ctypes.c_double
libspice.vrotv_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), ctypes.c_double, (ctypes.c_double * 3)]
libspice.vscl_c.argtypes = [ctypes.c_double, (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vsclg_c.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.vsep_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vsep_c.restype = ctypes.c_double
libspice.vsepg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
libspice.vsepg_c.restype = ctypes.c_double
libspice.vsub_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3), (ctypes.c_double * 3)]
libspice.vsubg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
libspice.vtmv_c.argtypes = [(ctypes.c_double * 3), (ctypes.c_double * 3)*3, (ctypes.c_double * 3)]
libspice.vtmv_c.restype = ctypes.c_double
libspice.vtmvg_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
libspice.vtmvg_c.restype = ctypes.c_double
libspice.vupack_c.argtypes = [(ctypes.c_double * 3), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
libspice.vzero_c.argtypes = [(ctypes.c_double * 3)]
libspice.vzero_c.restype = ctypes.c_bool
libspice.vzerog_c.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
libspice.vzerog_c.restype = ctypes.c_bool

##########################################################################################################################################################
# W

#libspice.wncomd_c.argtypes = [ctypes.c_double, ctypes.c_double, None, None]
#libspice.wncond_c.argtypes = [ctypes.c_double, ctypes.c_double, None]
#libspice.wndifd_c.argtypes = [None, None, None]
#libspice.wnexpd_c.argtypes = [ctypes.c_double, ctypes.c_double, None]
#libspice.wnextd_c.argtypes = [ctypes.c_char_p, None]
#libspice.wnfetd_c.argtypes = [None, ctypes.c_int, ctypes.c_double, ctypes.c_double]
#libspice.wnfild_c.argtypes = [ctypes.c_double, None]
#libspice.wnfltd_c.argtypes = [ctypes.c_double, None]
#libspice.wninsd_c.argtypes = [ctypes.c_double, ctypes.c_double, None]
#libspice.wnintd_c.argtypes = [None, None, None]
#libspice.wnsumd_c.argtypes = [None, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int]
#libspice.wnunid_c.argtypes = [None, None, None]
#libspice.wnvald_c.argtypes = [ctypes.c_int, ctypes.c_int, None]
##########################################################################################################################################################
# X

libspice.xf2eul_c.argtypes = [(ctypes.c_double * 6)*6, ctypes.c_int, ctypes.c_int, ctypes.c_int, (ctypes.c_double * 6), ctypes.POINTER(ctypes.c_bool)]
libspice.xf2rav_c.argtypes = [(ctypes.c_double * 6)*6, (ctypes.c_double * 3)*3, (ctypes.c_double * 3)]
libspice.xpose_c.argtypes = [(ctypes.c_double * 3)*3, (ctypes.c_double * 3)*3]
libspice.xpose6_c.argtypes = [(ctypes.c_double * 6)*6, (ctypes.c_double * 6)*6]
libspice.xposeg_c.argtypes = [ctypes.c_int, ctypes.c_int]
##########################################################################################################################################################
# Z

libspice.zzgetcml_c.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_bool]
libspice.zzgfsavh_c.argtypes = [ctypes.c_bool]
#libspice.zzsynccl_c.argtypes = [None]
