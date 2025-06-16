"""
The MIT License (MIT)

Copyright (c) [2015-2025] [Andrew Annex]

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

from typing import Union, Iterable, Type
from .libspicehelper import _tkversion

errorformat = """
================================================================================

Toolkit version: {tkvsn}

{short} --
{explain}
{long}

{traceback}

================================================================================\
"""


class SpiceyError(Exception):
    """
    SpiceyError wraps CSPICE errors for use in Python.
    """

    def __init__(
        self,
        short: str = "",
        explain: str = "",
        long: str = "",
        traceback: str = "",
        found: Union[bool, Iterable[bool], Iterable[int]] = False,
    ) -> None:
        """
        Base python exception type for SpiceyPy, maintained for backwards compatibilty.

        More information regarding the error system internal to spice can be found at the naif website.

        https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/error.html

        :param short: A short, descriptive message.
        :param explain: An expanded form of the short message if present.
        :param long: Optionally, a long message, possibly containing data.
        :param traceback: the internal spice sequence of calls leading to the routine that detected the error.
        :param found: if present
        """
        self.tkvsn = _tkversion
        self.short = short
        self.explain = explain
        self.long = long
        self.traceback = traceback
        self.found = found
        self.message = errorformat.format(
            tkvsn=self.tkvsn,
            short=short,
            explain=explain,
            long=long,
            traceback=traceback,
        )

    def __str__(self) -> str:
        return self.message


class SpiceyPyError(SpiceyError):
    """
    Thin wrapping exception for SpiceyError.

    In SpiceyPy versions 3.0.2 and prior, the base exception was a SpiceyError
    SpiceyPyError is a slightly more verbose and correct error name.
    """

    pass


class NotFoundError(SpiceyPyError):
    """
    A NotFound Error from Spice
    """

    def __init__(
        self, message=None, found: Union[bool, Iterable[bool], Iterable[int]] = False
    ):
        self.found = found
        self.message = message


class SpiceyPyIOError(SpiceyPyError, IOError):
    """
    SpiceyPyError mixed with IOError
    """

    pass


class SpiceyPyMemoryError(SpiceyPyError, MemoryError):
    """
    SpiceyPyError mixed with MemoryError
    """

    pass


class SpiceyPyTypeError(SpiceyPyError, TypeError):
    """
    SpiceyPyError mixed with TypeError
    """

    pass


class SpiceyPyKeyError(SpiceyPyError, KeyError):
    """
    SpiceyPyError mixed with KeyError
    """

    pass


class SpiceyPyIndexError(SpiceyPyError, IndexError):
    """
    SpiceyPyError mixed with IndexError
    """

    pass


class SpiceyPyRuntimeError(SpiceyPyError, RuntimeError):
    """
    SpiceyPyError mixed with RuntimeError
    """

    pass


class SpiceyPyValueError(SpiceyPyError, ValueError):
    """
    SpiceyPyError mixed with ValueError
    """

    pass


class SpiceyPyZeroDivisionError(SpiceyPyError, ZeroDivisionError):
    """
    SpiceyPyError mixed with ZeroDivisionError
    """

    pass


# ioerrors
class SpiceBADARCHTYPE(SpiceyPyIOError):
    pass


class SpiceBADATTRIBUTES(SpiceyPyIOError):
    pass


class SpiceBADCOMMENTAREA(SpiceyPyIOError):
    pass


class SpiceBADCOORDSYSTEM(SpiceyPyIOError):
    pass


class SpiceBADDASCOMMENTAREA(SpiceyPyIOError):
    pass


class SpiceBADFILETYPE(SpiceyPyIOError):
    pass


class SpiceBADVARNAME(SpiceyPyIOError):
    pass


class SpiceBLANKFILENAME(SpiceyPyIOError):
    pass


class SpiceCKINSUFFDATA(SpiceyPyIOError):
    pass


class SpiceCOVERAGEGAP(SpiceyPyIOError):
    pass


class SpiceDAFBEGGTEND(SpiceyPyIOError):
    pass


class SpiceDAFFRNOTFOUND(SpiceyPyIOError):
    pass


class SpiceDAFIMPROPOPEN(SpiceyPyIOError):
    pass


class SpiceDAFNEGADDR(SpiceyPyIOError):
    pass


class SpiceDAFNOSEARCH(SpiceyPyIOError):
    pass


class SpiceDAFOPENFAIL(SpiceyPyIOError):
    pass


class SpiceDAFRWCONFLICT(SpiceyPyIOError):
    pass


class SpiceDASFILEREADFAILED(SpiceyPyIOError):
    pass


class SpiceDASIMPROPOPEN(SpiceyPyIOError):
    pass


class SpiceDASNOSUCHHANDLE(SpiceyPyIOError):
    pass


class SpiceDASOPENCONFLICT(SpiceyPyIOError):
    pass


class SpiceDASOPENFAIL(SpiceyPyIOError):
    pass


class SpiceDASRWCONFLICT(SpiceyPyIOError):
    pass


class SpiceEKNOSEGMENTS(SpiceyPyIOError):
    pass


class SpiceFILECURRENTLYOPEN(SpiceyPyIOError):
    pass


class SpiceFILEDOESNOTEXIST(SpiceyPyIOError):
    pass


class SpiceFILEISNOTSPK(SpiceyPyIOError):
    pass


class SpiceFILENOTFOUND(SpiceyPyIOError):
    pass


class SpiceFILEOPENFAILED(SpiceyPyIOError):
    pass


class SpiceFILEREADFAILED(SpiceyPyIOError):
    pass


class SpiceINQUIREERROR(SpiceyPyIOError):
    pass


class SpiceINQUIREFAILED(SpiceyPyIOError):
    pass


class SpiceINVALIDARCHTYPE(SpiceyPyIOError):
    pass


class SpiceNOCURRENTARRAY(SpiceyPyIOError):
    pass


class SpiceNOLOADEDFILES(SpiceyPyIOError):
    pass


class SpiceNOSEGMENTSFOUND(SpiceyPyIOError):
    pass


class SpiceNOSUCHFILE(SpiceyPyIOError):
    pass


class SpiceNOTADAFFILE(SpiceyPyIOError):
    pass


class SpiceNOTADASFILE(SpiceyPyIOError):
    pass


class SpiceRECURSIVELOADING(SpiceyPyIOError):
    pass


class SpiceSPKINSUFFDATA(SpiceyPyIOError):
    pass


class SpiceSPKINVALIDOPTION(SpiceyPyIOError):
    pass


class SpiceSPKNOTASUBSET(SpiceyPyIOError):
    pass


class SpiceSPKTYPENOTSUPP(SpiceyPyIOError):
    pass


class SpiceTABLENOTLOADED(SpiceyPyIOError):
    pass


class SpiceTOOMANYFILESOPEN(SpiceyPyIOError):
    pass


class SpiceUNKNOWNSPKTYPE(SpiceyPyIOError):
    pass


class SpiceUNSUPPORTEDBFF(SpiceyPyIOError):
    pass


class SpiceUNSUPPORTEDSPEC(SpiceyPyIOError):
    pass


# memoryerrors
class SpiceARRAYTOOSMALL(SpiceyPyMemoryError):
    pass


class SpiceBADARRAYSIZE(SpiceyPyMemoryError):
    pass


class SpiceBOUNDARYTOOBIG(SpiceyPyMemoryError):
    pass


class SpiceBUFFEROVERFLOW(SpiceyPyMemoryError):
    pass


class SpiceCELLTOOSMALL(SpiceyPyMemoryError):
    pass


class SpiceCKTOOMANYFILES(SpiceyPyMemoryError):
    pass


class SpiceCOLUMNTOOSMALL(SpiceyPyMemoryError):
    pass


class SpiceCOMMENTTOOLONG(SpiceyPyMemoryError):
    pass


class SpiceDAFFTFULL(SpiceyPyMemoryError):
    pass


class SpiceDASFTFULL(SpiceyPyMemoryError):
    pass


class SpiceDEVICENAMETOOLONG(SpiceyPyMemoryError):
    pass


class SpiceEKCOLATTRTABLEFULL(SpiceyPyMemoryError):
    pass


class SpiceEKCOLDESCTABLEFULL(SpiceyPyMemoryError):
    pass


class SpiceEKFILETABLEFULL(SpiceyPyMemoryError):
    pass


class SpiceEKIDTABLEFULL(SpiceyPyMemoryError):
    pass


class SpiceEKSEGMENTTABLEFULL(SpiceyPyMemoryError):
    pass


class SpiceGRIDTOOLARGE(SpiceyPyMemoryError):
    pass


class SpiceINSUFFLEN(SpiceyPyMemoryError):
    pass


class SpiceKERNELPOOLFULL(SpiceyPyMemoryError):
    pass


class SpiceMALLOCFAILED(SpiceyPyMemoryError):
    pass


class SpiceMALLOCFAILURE(SpiceyPyMemoryError):
    pass


class SpiceMEMALLOCFAILED(SpiceyPyMemoryError):
    pass


class SpiceMESSAGETOOLONG(SpiceyPyMemoryError):
    pass


class SpiceNOMOREROOM(SpiceyPyMemoryError):
    pass


class SpiceOUTOFROOM(SpiceyPyMemoryError):
    pass


class SpicePCKFILETABLEFULL(SpiceyPyMemoryError):
    pass


class SpiceSETEXCESS(SpiceyPyMemoryError):
    pass


class SpiceSPKFILETABLEFULL(SpiceyPyMemoryError):
    pass


class SpiceTRACEBACKOVERFLOW(SpiceyPyMemoryError):
    pass


class SpiceWINDOWEXCESS(SpiceyPyMemoryError):
    pass


class SpiceWORKSPACETOOSMALL(SpiceyPyMemoryError):
    pass


# typeerrors
class SpiceBADVARIABLETYPE(SpiceyPyTypeError):
    pass


class SpiceINVALIDTYPE(SpiceyPyTypeError):
    pass


class SpiceINVALIDARRAYTYPE(SpiceyPyTypeError):
    pass


class SpiceNOTASET(SpiceyPyTypeError):
    pass


class SpiceTYPEMISMATCH(SpiceyPyTypeError):
    pass


class SpiceWRONGDATATYPE(SpiceyPyTypeError):
    pass


# keyerrors
class SpiceBODYIDNOTFOUND(SpiceyPyKeyError):
    pass


class SpiceBODYNAMENOTFOUND(SpiceyPyKeyError):
    pass


class SpiceCANTFINDFRAME(SpiceyPyKeyError):
    pass


class SpiceFRAMEIDNOTFOUND(SpiceyPyKeyError):
    pass


class SpiceFRAMENAMENOTFOUND(SpiceyPyKeyError):
    pass


class SpiceIDCODENOTFOUND(SpiceyPyKeyError):
    pass


class SpiceKERNELVARNOTFOUND(SpiceyPyKeyError):
    pass


class SpiceNOTRANSLATION(SpiceyPyKeyError):
    pass


class SpiceUNKNOWNFRAME(SpiceyPyKeyError):
    pass


class SpiceVARIABLENOTFOUND(SpiceyPyKeyError):
    pass


# indexerrors
class SpiceBADVERTEXINDEX(SpiceyPyIndexError):
    pass


class SpiceINDEXOUTOFRANGE(SpiceyPyIndexError):
    pass


class SpiceINVALDINDEX(SpiceyPyIndexError):
    pass


class SpiceINVALIDINDEX(SpiceyPyIndexError):
    pass


# zerodivisionerrors
class SpiceDIVIDEBYZERO(SpiceyPyZeroDivisionError):
    pass


# runtimeerrors
class SpiceBADINITSTATE(SpiceyPyRuntimeError):
    pass


class SpiceBUG(SpiceyPyRuntimeError):
    pass


class SpiceIMMUTABLEVALUE(SpiceyPyRuntimeError):
    pass


class SpiceINVALIDSIGNAL(SpiceyPyRuntimeError):
    pass


class SpiceNOTINITIALIZED(SpiceyPyRuntimeError):
    pass


class SpiceSIGNALFAILED(SpiceyPyRuntimeError):
    pass


class SpiceSIGNALFAILURE(SpiceyPyRuntimeError):
    pass


class SpiceTRACESTACKEMPTY(SpiceyPyRuntimeError):
    pass


# valueerrors
class SpiceARRAYSHAPEMISMATCH(SpiceyPyValueError):
    pass


class SpiceBADACTION(SpiceyPyValueError):
    pass


class SpiceBADAXISLENGTH(SpiceyPyValueError):
    pass


class SpiceBADAXISNUMBERS(SpiceyPyValueError):
    pass


class SpiceBADBORESIGHTSPEC(SpiceyPyValueError):
    pass


class SpiceBADBOUNDARY(SpiceyPyValueError):
    pass


class SpiceBADCOARSEVOXSCALE(SpiceyPyValueError):
    pass


class SpiceBADDEFAULTVALUE(SpiceyPyValueError):
    pass


class SpiceBADDESCRTIMES(SpiceyPyValueError):
    pass


class SpiceBADDIRECTION(SpiceyPyValueError):
    pass


class SpiceBADECCENTRICITY(SpiceyPyValueError):
    pass


class SpiceBADENDPOINTS(SpiceyPyValueError):
    pass


class SpiceBADFINEVOXELSCALE(SpiceyPyValueError):
    pass


class SpiceBADFRAME(SpiceyPyValueError):
    pass


class SpiceBADFRAMECLASS(SpiceyPyValueError):
    pass


class SpiceBADGM(SpiceyPyValueError):
    pass


class SpiceBADINDEX(SpiceyPyValueError):
    pass


class SpiceBADLATUSRECTUM(SpiceyPyValueError):
    pass


class SpiceBADLIMBLOCUSMIX(SpiceyPyValueError):
    pass


class SpiceBADPARTNUMBER(SpiceyPyValueError):
    pass


class SpiceBADPERIAPSEVALUE(SpiceyPyValueError):
    pass


class SpiceBADPLATECOUNT(SpiceyPyValueError):
    pass


class SpiceBADRADIUS(SpiceyPyValueError):
    pass


class SpiceBADRADIUSCOUNT(SpiceyPyValueError):
    pass


class SpiceBADREFVECTORSPEC(SpiceyPyValueError):
    pass


class SpiceBADSEMIAXIS(SpiceyPyValueError):
    pass


class SpiceBADSTOPTIME(SpiceyPyValueError):
    pass


class SpiceBADTIMEITEM(SpiceyPyValueError):
    pass


class SpiceBADTIMESTRING(SpiceyPyValueError):
    pass


class SpiceBADTIMETYPE(SpiceyPyValueError):
    pass


class SpiceBADVARIABLESIZE(SpiceyPyValueError):
    pass


class SpiceBADVECTOR(SpiceyPyValueError):
    pass


class SpiceBADVERTEXCOUNT(SpiceyPyValueError):
    pass


class SpiceBARYCENTEREPHEM(SpiceyPyValueError):
    pass


class SpiceBLANKMODULENAME(SpiceyPyValueError):
    pass


class SpiceBODIESNOTDISTINCT(SpiceyPyValueError):
    pass


class SpiceBODYANDCENTERSAME(SpiceyPyValueError):
    pass


class SpiceBORESIGHTMISSING(SpiceyPyValueError):
    pass


class SpiceBOUNDARYMISSING(SpiceyPyValueError):
    pass


class SpiceBOUNDSOUTOFORDER(SpiceyPyValueError):
    pass


class SpiceCOORDSYSNOTREC(SpiceyPyValueError):
    pass


class SpiceCROSSANGLEMISSING(SpiceyPyValueError):
    pass


class SpiceDEGENERATECASE(SpiceyPyValueError):
    pass


class SpiceDEGENERATEINTERVAL(SpiceyPyValueError):
    pass


class SpiceDEGENERATESURFACE(SpiceyPyValueError):
    pass


class SpiceDEGREEOUTOFRANGE(SpiceyPyValueError):
    pass


class SpiceDEPENDENTVECTORS(SpiceyPyValueError):
    pass


class SpiceNONCONTIGUOUSARRAY(SpiceyPyValueError):
    pass


class SpiceDSKTARGETMISMATCH(SpiceyPyValueError):
    pass


class SpiceDTOUTOFRANGE(SpiceyPyValueError):
    pass


class SpiceDUBIOUSMETHOD(SpiceyPyValueError):
    pass


class SpiceECCOUTOFRANGE(SpiceyPyValueError):
    pass


class SpiceELEMENTSTOOSHORT(SpiceyPyValueError):
    pass


class SpiceEMPTYSEGMENT(SpiceyPyValueError):
    pass


class SpiceEMPTYSTRING(SpiceyPyValueError):
    pass


class SpiceFRAMEMISSING(SpiceyPyValueError):
    pass


class SpiceILLEGALCHARACTER(SpiceyPyValueError):
    pass


class SpiceINCOMPATIBLESCALE(SpiceyPyValueError):
    pass


class SpiceINCOMPATIBLEUNITS(SpiceyPyValueError):
    pass


class SpiceINPUTOUTOFRANGE(SpiceyPyValueError):
    pass


class SpiceINPUTSTOOLARGE(SpiceyPyValueError):
    pass


class SpiceINSUFFICIENTANGLES(SpiceyPyValueError):
    pass


class SpiceINTINDEXTOOSMALL(SpiceyPyValueError):
    pass


class SpiceINTLENNOTPOS(SpiceyPyValueError):
    pass


class SpiceINTOUTOFRANGE(SpiceyPyValueError):
    pass


class SpiceINVALIDACTION(SpiceyPyValueError):
    pass


class SpiceINVALIDARGUMENT(SpiceyPyValueError):
    pass


class SpiceINVALIDARRAYRANK(SpiceyPyValueError):
    pass


class SpiceINVALIDARRAYSHAPE(SpiceyPyValueError):
    pass


class SpiceINVALIDAXISLENGTH(SpiceyPyValueError):
    pass


class SpiceINVALIDCARDINALITY(SpiceyPyValueError):
    pass


class SpiceINVALIDCOUNT(SpiceyPyValueError):
    pass


class SpiceINVALIDDEGREE(SpiceyPyValueError):
    pass


class SpiceINVALIDDESCRTIME(SpiceyPyValueError):
    pass


class SpiceINVALIDDIMENSION(SpiceyPyValueError):
    pass


class SpiceINVALIDELLIPSE(SpiceyPyValueError):
    pass


class SpiceINVALIDENDPNTSPEC(SpiceyPyValueError):
    pass


class SpiceINVALIDEPOCH(SpiceyPyValueError):
    pass


class SpiceINVALIDFORMAT(SpiceyPyValueError):
    pass


class SpiceINVALIDFRAME(SpiceyPyValueError):
    pass


class SpiceINVALIDFRAMEDEF(SpiceyPyValueError):
    pass


class SpiceINVALIDLIMBTYPE(SpiceyPyValueError):
    pass


class SpiceINVALIDLISTITEM(SpiceyPyValueError):
    pass


class SpiceINVALIDLOCUS(SpiceyPyValueError):
    pass


class SpiceINVALIDLONEXTENT(SpiceyPyValueError):
    pass


class SpiceINVALIDMETHOD(SpiceyPyValueError):
    pass


class SpiceINVALIDMSGTYPE(SpiceyPyValueError):
    pass


class SpiceINVALIDNUMINTS(SpiceyPyValueError):
    pass


class SpiceINVALIDNUMRECS(SpiceyPyValueError):
    pass


class SpiceINVALIDOCCTYPE(SpiceyPyValueError):
    pass


class SpiceINVALIDOPERATION(SpiceyPyValueError):
    pass


class SpiceINVALIDOPTION(SpiceyPyValueError):
    pass


class SpiceINVALIDPLANE(SpiceyPyValueError):
    pass


class SpiceINVALIDPOINT(SpiceyPyValueError):
    pass


class SpiceINVALIDRADIUS(SpiceyPyValueError):
    pass


class SpiceINVALIDREFFRAME(SpiceyPyValueError):
    pass


class SpiceINVALIDROLLSTEP(SpiceyPyValueError):
    pass


class SpiceINVALIDSCLKSTRING(SpiceyPyValueError):
    pass


class SpiceINVALIDSCLKTIME(SpiceyPyValueError):
    pass


class SpiceINVALIDSEARCHSTEP(SpiceyPyValueError):
    pass


class SpiceINVALIDSIZE(SpiceyPyValueError):
    pass


class SpiceINVALIDSTARTTIME(SpiceyPyValueError):
    pass


class SpiceINVALIDSTATE(SpiceyPyValueError):
    pass


class SpiceINVALIDSTEP(SpiceyPyValueError):
    pass


class SpiceINVALIDSTEPSIZE(SpiceyPyValueError):
    pass


class SpiceINVALIDSUBTYPE(SpiceyPyValueError):
    pass


class SpiceINVALIDTARGET(SpiceyPyValueError):
    pass


class SpiceINVALIDTERMTYPE(SpiceyPyValueError):
    pass


class SpiceINVALIDTIMEFORMAT(SpiceyPyValueError):
    pass


class SpiceINVALIDTIMESTRING(SpiceyPyValueError):
    pass


class SpiceINVALIDTOL(SpiceyPyValueError):
    pass


class SpiceINVALIDTOLERANCE(SpiceyPyValueError):
    pass


class SpiceINVALIDVALUE(SpiceyPyValueError):
    pass


class SpiceINVALIDVERTEX(SpiceyPyValueError):
    pass


class SpiceMISSINGDATA(SpiceyPyValueError):
    pass


class SpiceMISSINGTIMEINFO(SpiceyPyValueError):
    pass


class SpiceMISSINGVALUE(SpiceyPyValueError):
    pass


class SpiceNAMESDONOTMATCH(SpiceyPyValueError):
    pass


class SpiceNOCLASS(SpiceyPyValueError):
    pass


class SpiceNOCOLUMN(SpiceyPyValueError):
    pass


class SpiceNOFRAME(SpiceyPyValueError):
    pass


class SpiceNOFRAMEINFO(SpiceyPyValueError):
    pass


class SpiceNOINTERCEPT(SpiceyPyValueError):
    pass


class SpiceNOINTERVAL(SpiceyPyValueError):
    pass


class SpiceNONCONICMOTION(SpiceyPyValueError):
    pass


class SpiceNONPOSITIVEMASS(SpiceyPyValueError):
    pass


class SpiceNONPOSITIVESCALE(SpiceyPyValueError):
    pass


class SpiceNONPRINTABLECHARS(SpiceyPyValueError):
    pass


class SpiceNOPARTITION(SpiceyPyValueError):
    pass


class SpiceNOPATHVALUE(SpiceyPyValueError):
    pass


class SpiceNOPRIORITIZATION(SpiceyPyValueError):
    pass


class SpiceNOSEPARATION(SpiceyPyValueError):
    pass


class SpiceNOTADPNUMBER(SpiceyPyValueError):
    pass


class SpiceNOTANINTEGER(SpiceyPyValueError):
    pass


class SpiceNOTAROTATION(SpiceyPyValueError):
    pass


class SpiceNOTINPART(SpiceyPyValueError):
    pass


class SpiceNOTPRINTABLECHARS(SpiceyPyValueError):
    pass


class SpiceNOTRECOGNIZED(SpiceyPyValueError):
    pass


class SpiceNOTSUPPORTED(SpiceyPyValueError):
    pass


class SpiceNULLPOINTER(SpiceyPyValueError):
    pass


class SpiceNUMCOEFFSNOTPOS(SpiceyPyValueError):
    pass


class SpiceNUMERICOVERFLOW(SpiceyPyValueError):
    pass


class SpiceNUMPARTSUNEQUAL(SpiceyPyValueError):
    pass


class SpiceNUMSTATESNOTPOS(SpiceyPyValueError):
    pass


class SpicePLATELISTTOOSMALL(SpiceyPyValueError):
    pass


class SpicePOINTNOTONSURFACE(SpiceyPyValueError):
    pass


class SpicePOINTONZAXIS(SpiceyPyValueError):
    pass


class SpicePTRARRAYTOOSMALL(SpiceyPyValueError):
    pass


class SpiceREFANGLEMISSING(SpiceyPyValueError):
    pass


class SpiceREFVECTORMISSING(SpiceyPyValueError):
    pass


class SpiceSCLKTRUNCATED(SpiceyPyValueError):
    pass


class SpiceSEGIDTOOLONG(SpiceyPyValueError):
    pass


class SpiceSHAPEMISSING(SpiceyPyValueError):
    pass


class SpiceSHAPENOTSUPPORTED(SpiceyPyValueError):
    pass


class SpiceSINGULARMATRIX(SpiceyPyValueError):
    pass


class SpiceSTRINGTOOLSHORT(SpiceyPyValueError):
    pass


class SpiceSTRINGTOOSHORT(SpiceyPyValueError):
    pass


class SpiceSUBPOINTNOTFOUND(SpiceyPyValueError):
    pass


class SpiceTARGETMISMATCH(SpiceyPyValueError):
    pass


class SpiceTIMECONFLICT(SpiceyPyValueError):
    pass


class SpiceTIMESDONTMATCH(SpiceyPyValueError):
    pass


class SpiceTIMESOUTOFORDER(SpiceyPyValueError):
    pass


class SpiceTOOFEWPACKETS(SpiceyPyValueError):
    pass


class SpiceTOOFEWPLATES(SpiceyPyValueError):
    pass


class SpiceTOOFEWSTATES(SpiceyPyValueError):
    pass


class SpiceTOOFEWVERTICES(SpiceyPyValueError):
    pass


class SpiceTOOMANYPARTS(SpiceyPyValueError):
    pass


class SpiceUNDEFINEDFRAME(SpiceyPyValueError):
    pass


class SpiceUNITSMISSING(SpiceyPyValueError):
    pass


class SpiceUNITSNOTREC(SpiceyPyValueError):
    pass


class SpiceUNKNOWNCOMPARE(SpiceyPyValueError):
    pass


class SpiceUNKNOWNSYSTEM(SpiceyPyValueError):
    pass


class SpiceUNMATCHENDPTS(SpiceyPyValueError):
    pass


class SpiceUNORDEREDTIMES(SpiceyPyValueError):
    pass


class SpiceUNPARSEDTIME(SpiceyPyValueError):
    pass


class SpiceVALUEOUTOFRANGE(SpiceyPyValueError):
    pass


class SpiceVECTORTOOBIG(SpiceyPyValueError):
    pass


class SpiceWINDOWTOOSMALL(SpiceyPyValueError):
    pass


class SpiceYEAROUTOFRANGE(SpiceyPyValueError):
    pass


class SpiceZEROBOUNDSEXTENT(SpiceyPyValueError):
    pass


class SpiceZEROLENGTHCOLUMN(SpiceyPyValueError):
    pass


class SpiceZEROPOSITION(SpiceyPyValueError):
    pass


class SpiceZEROQUATERNION(SpiceyPyValueError):
    pass


class SpiceZEROVECTOR(SpiceyPyValueError):
    pass


class SpiceZEROVELOCITY(SpiceyPyValueError):
    pass


class Spice1NODATAFORBODY(SpiceyPyError):
    pass


class SpiceADDRESSOUTOFBOUNDS(SpiceyPyError):
    pass


class SpiceAGENTLISTOVERFLOW(SpiceyPyError):
    pass


class SpiceALLGONE(SpiceyPyError):
    pass


class SpiceAMBIGTEMPL(SpiceyPyError):
    pass


class SpiceARRAYSIZEMISMATCH(SpiceyPyError):
    pass


class SpiceAVALOUTOFRANGE(SpiceyPyError):
    pass


class SpiceAXISUNDERFLOW(SpiceyPyError):
    pass


class SpiceBADADDRESS(SpiceyPyError):
    pass


class SpiceBADANGLE(SpiceyPyError):
    pass


class SpiceBADANGLEUNITS(SpiceyPyError):
    pass


class SpiceBADANGRATEERROR(SpiceyPyError):
    pass


class SpiceBADANGULARRATE(SpiceyPyError):
    pass


class SpiceBADANGULARRATEFLAG(SpiceyPyError):
    pass


class SpiceBADARCHITECTURE(SpiceyPyError):
    pass


class SpiceBADATTIME(SpiceyPyError):
    pass


class SpiceBADATTRIBUTE(SpiceyPyError):
    pass


class SpiceBADAUVALUE(SpiceyPyError):
    pass


class SpiceBADAVFLAG(SpiceyPyError):
    pass


class SpiceBADAVFRAMEFLAG(SpiceyPyError):
    pass


class SpiceBADAXIS(SpiceyPyError):
    pass


class SpiceBADBLOCKSIZE(SpiceyPyError):
    pass


class SpiceBADBODY1SPEC(SpiceyPyError):
    pass


class SpiceBADBODY2SPEC(SpiceyPyError):
    pass


class SpiceBADBODYID(SpiceyPyError):
    pass


class SpiceBADBODYID1(SpiceyPyError):
    pass


class SpiceBADBODYID2(SpiceyPyError):
    pass


class SpiceBADCATALOGFILE(SpiceyPyError):
    pass


class SpiceBADCENTER1SPEC(SpiceyPyError):
    pass


class SpiceBADCENTER2SPEC(SpiceyPyError):
    pass


class SpiceBADCENTERNAME(SpiceyPyError):
    pass


class SpiceBADCHECKFLAG(SpiceyPyError):
    pass


class SpiceBADCK1SEGMENT(SpiceyPyError):
    pass


class SpiceBADCK3SEGMENT(SpiceyPyError):
    pass


class SpiceBADCKTYPESPEC(SpiceyPyError):
    pass


class SpiceBADCOLUMDECL(SpiceyPyError):
    pass


class SpiceBADCOLUMNCOUNT(SpiceyPyError):
    pass


class SpiceBADCOLUMNDECL(SpiceyPyError):
    pass


class SpiceBADCOMPNUMBER(SpiceyPyError):
    pass


class SpiceBADCOORDBOUNDS(SpiceyPyError):
    pass


class SpiceBADCOORDSYS(SpiceyPyError):
    pass


class SpiceBADCOVFRAME1SPEC1(SpiceyPyError):
    pass


class SpiceBADCOVFRAME1SPEC2(SpiceyPyError):
    pass


class SpiceBADCOVFRAME1SPEC4(SpiceyPyError):
    pass


class SpiceBADCOVFRAME1SPEC5(SpiceyPyError):
    pass


class SpiceBADCOVFRAME1SPEC6(SpiceyPyError):
    pass


class SpiceBADCOVFRAME2SPEC1(SpiceyPyError):
    pass


class SpiceBADCOVFRAME2SPEC2(SpiceyPyError):
    pass


class SpiceBADCOVFRAME2SPEC4(SpiceyPyError):
    pass


class SpiceBADCOVFRAME2SPEC5(SpiceyPyError):
    pass


class SpiceBADCOVFRAME2SPEC6(SpiceyPyError):
    pass


class SpiceBADCURVETYPE(SpiceyPyError):
    pass


class SpiceBADDAFTRANSFERFILE(SpiceyPyError):
    pass


class SpiceBADDASDIRECTORY(SpiceyPyError):
    pass


class SpiceBADDASFILE(SpiceyPyError):
    pass


class SpiceBADDASTRANSFERFILE(SpiceyPyError):
    pass


class SpiceBADDATALINE(SpiceyPyError):
    pass


class SpiceBADDATAORDERTOKEN(SpiceyPyError):
    pass


class SpiceBADDATATYPE(SpiceyPyError):
    pass


class SpiceBADDATATYPEFLAG(SpiceyPyError):
    pass


class SpiceBADDECIMALSCLK1(SpiceyPyError):
    pass


class SpiceBADDECIMALSCLK2(SpiceyPyError):
    pass


class SpiceBADDIMENSION(SpiceyPyError):
    pass


class SpiceBADDIMENSIONS(SpiceyPyError):
    pass


class SpiceBADDOUBLEPRECISION(SpiceyPyError):
    pass


class SpiceBADDOWNSAMPLINGTOL(SpiceyPyError):
    pass


class SpiceBADDPSCLK1(SpiceyPyError):
    pass


class SpiceBADDPSCLK2(SpiceyPyError):
    pass


class SpiceBADET1(SpiceyPyError):
    pass


class SpiceBADET2(SpiceyPyError):
    pass


class SpiceBADEULERANGLEUNITS(SpiceyPyError):
    pass


class SpiceBADFILEFORMAT(SpiceyPyError):
    pass


class SpiceBADFILENAME(SpiceyPyError):
    pass


class SpiceBADFORMATSPECIFIER(SpiceyPyError):
    pass


class SpiceBADFORMATSTRING(SpiceyPyError):
    pass


class SpiceBADFRAME1NAME(SpiceyPyError):
    pass


class SpiceBADFRAME2NAME(SpiceyPyError):
    pass


class SpiceBADFRAMECOUNT(SpiceyPyError):
    pass


class SpiceBADFRAMESPEC(SpiceyPyError):
    pass


class SpiceBADFRAMESPEC2(SpiceyPyError):
    pass


class SpiceBADFROMFRAME1SP1(SpiceyPyError):
    pass


class SpiceBADFROMFRAME1SP2(SpiceyPyError):
    pass


class SpiceBADFROMFRAME2SP1(SpiceyPyError):
    pass


class SpiceBADFROMFRAME2SP2(SpiceyPyError):
    pass


class SpiceBADFROMTIME(SpiceyPyError):
    pass


class SpiceBADFROMTIMESYSTEM(SpiceyPyError):
    pass


class SpiceBADFROMTIMETYPE(SpiceyPyError):
    pass


class SpiceBADGEFVERSION(SpiceyPyError):
    pass


class SpiceBADGEOMETRY(SpiceyPyError):
    pass


class SpiceBADHARDSPACE(SpiceyPyError):
    pass


class SpiceBADHERMITDEGREE(SpiceyPyError):
    pass


class SpiceBADINPUTDATALINE(SpiceyPyError):
    pass


class SpiceBADINPUTETTIME(SpiceyPyError):
    pass


class SpiceBADINPUTTYPE(SpiceyPyError):
    pass


class SpiceBADINPUTUTCTIME(SpiceyPyError):
    pass


class SpiceBADINSTRUMENTID(SpiceyPyError):
    pass


class SpiceBADINTEGER(SpiceyPyError):
    pass


class SpiceBADKERNELTYPE(SpiceyPyError):
    pass


class SpiceBADKERNELVARTYPE(SpiceyPyError):
    pass


class SpiceBADLAGRANGEDEGREE(SpiceyPyError):
    pass


class SpiceBADLATITUDEBOUNDS(SpiceyPyError):
    pass


class SpiceBADLATITUDERANGE(SpiceyPyError):
    pass


class SpiceBADLEAPSECONDS(SpiceyPyError):
    pass


class SpiceBADLINEPERRECCOUNT(SpiceyPyError):
    pass


class SpiceBADLISTFILENAME(SpiceyPyError):
    pass


class SpiceBADLONGITUDERANGE(SpiceyPyError):
    pass


class SpiceBADMATRIX(SpiceyPyError):
    pass


class SpiceBADMEANMOTION(SpiceyPyError):
    pass


class SpiceBADMECCENTRICITY(SpiceyPyError):
    pass


class SpiceBADMETHODSYNTAX(SpiceyPyError):
    pass


class SpiceBADMIDNIGHTTYPE(SpiceyPyError):
    pass


class SpiceBADMSEMIMAJOR(SpiceyPyError):
    pass


class SpiceBADMSOPQUATERNION(SpiceyPyError):
    pass


class SpiceBADNOFDIGITS(SpiceyPyError):
    pass


class SpiceBADNOFSTATES(SpiceyPyError):
    pass


class SpiceBADNUMBEROFPOINTS(SpiceyPyError):
    pass


class SpiceBADOBJECTID(SpiceyPyError):
    pass


class SpiceBADOBJECTNAME(SpiceyPyError):
    pass


class SpiceBADOFFSETANGLES(SpiceyPyError):
    pass


class SpiceBADOFFSETANGUNITS(SpiceyPyError):
    pass


class SpiceBADOFFSETAXESFORMAT(SpiceyPyError):
    pass


class SpiceBADOFFSETAXIS123(SpiceyPyError):
    pass


class SpiceBADOFFSETAXISXYZ(SpiceyPyError):
    pass


class SpiceBADOPTIONNAME(SpiceyPyError):
    pass


class SpiceBADORBITALPERIOD(SpiceyPyError):
    pass


class SpiceBADOUTPUTSPKTYPE(SpiceyPyError):
    pass


class SpiceBADOUTPUTTYPE(SpiceyPyError):
    pass


class SpiceBADPCKVALUE(SpiceyPyError):
    pass


class SpiceBADPECCENTRICITY(SpiceyPyError):
    pass


class SpiceBADPICTURE(SpiceyPyError):
    pass


class SpiceBADPODLOCATION(SpiceyPyError):
    pass


class SpiceBADPRECVALUE(SpiceyPyError):
    pass


class SpiceBADPRIORITYSPEC(SpiceyPyError):
    pass


class SpiceBADQUATSIGN(SpiceyPyError):
    pass


class SpiceBADQUATTHRESHOLD(SpiceyPyError):
    pass


class SpiceBADRATEFRAMEFLAG(SpiceyPyError):
    pass


class SpiceBADRATETHRESHOLD(SpiceyPyError):
    pass


class SpiceBADRECORDCOUNT(SpiceyPyError):
    pass


class SpiceBADROTATIONAXIS123(SpiceyPyError):
    pass


class SpiceBADROTATIONAXISXYZ(SpiceyPyError):
    pass


class SpiceBADROTATIONORDER1(SpiceyPyError):
    pass


class SpiceBADROTATIONORDER2(SpiceyPyError):
    pass


class SpiceBADROTATIONORDER3(SpiceyPyError):
    pass


class SpiceBADROTATIONSORDER(SpiceyPyError):
    pass


class SpiceBADROTATIONTYPE(SpiceyPyError):
    pass


class SpiceBADROTAXESFORMAT(SpiceyPyError):
    pass


class SpiceBADROWCOUNT(SpiceyPyError):
    pass


class SpiceBADSCID(SpiceyPyError):
    pass


class SpiceBADSCLKDATA1(SpiceyPyError):
    pass


class SpiceBADSCLKDATA2(SpiceyPyError):
    pass


class SpiceBADSCLKDATA3(SpiceyPyError):
    pass


class SpiceBADSEMILATUS(SpiceyPyError):
    pass


class SpiceBADSHAPE(SpiceyPyError):
    pass


class SpiceBADSOLDAY(SpiceyPyError):
    pass


class SpiceBADSOLINDEX(SpiceyPyError):
    pass


class SpiceBADSOLTIME(SpiceyPyError):
    pass


class SpiceBADSOURCERADIUS(SpiceyPyError):
    pass


class SpiceBADSPICEQUATERNION(SpiceyPyError):
    pass


class SpiceBADSTARINDEX(SpiceyPyError):
    pass


class SpiceBADSTARTTIME(SpiceyPyError):
    pass


class SpiceBADSTDIONAME(SpiceyPyError):
    pass


class SpiceBADSUBSCRIPT(SpiceyPyError):
    pass


class SpiceBADSUBSTR(SpiceyPyError):
    pass


class SpiceBADSUBSTRINGBOUNDS(SpiceyPyError):
    pass


class SpiceBADSURFACEMAP(SpiceyPyError):
    pass


class SpiceBADTABLEFLAG(SpiceyPyError):
    pass


class SpiceBADTERMLOCUSMIX(SpiceyPyError):
    pass


class SpiceBADTIMEBOUNDS(SpiceyPyError):
    pass


class SpiceBADTIMECASE(SpiceyPyError):
    pass


class SpiceBADTIMECOUNT(SpiceyPyError):
    pass


class SpiceBADTIMEFORMAT(SpiceyPyError):
    pass


class SpiceBADTIMEOFFSET(SpiceyPyError):
    pass


class SpiceBADTIMESPEC(SpiceyPyError):
    pass


class SpiceBADTIMETYPEFLAG(SpiceyPyError):
    pass


class SpiceBADTLE(SpiceyPyError):
    pass


class SpiceBADTLECOVERAGEPAD(SpiceyPyError):
    pass


class SpiceBADTLECOVERAGEPAD2(SpiceyPyError):
    pass


class SpiceBADTLECOVERAGEPAD3(SpiceyPyError):
    pass


class SpiceBADTLEPADS(SpiceyPyError):
    pass


class SpiceBADTOFRAME1SPEC1(SpiceyPyError):
    pass


class SpiceBADTOFRAME1SPEC2(SpiceyPyError):
    pass


class SpiceBADTOFRAME2SPEC1(SpiceyPyError):
    pass


class SpiceBADTOFRAME2SPEC2(SpiceyPyError):
    pass


class SpiceBADTOTIME(SpiceyPyError):
    pass


class SpiceBADTOTIMESYSTEM(SpiceyPyError):
    pass


class SpiceBADTOTIMETYPE(SpiceyPyError):
    pass


class SpiceBADTYPESHAPECOMBO(SpiceyPyError):
    pass


class SpiceBADUNITS(SpiceyPyError):
    pass


class SpiceBADVARASSIGN(SpiceyPyError):
    pass


class SpiceBADWINDOWSIZE(SpiceyPyError):
    pass


class SpiceBARRAYTOOSMALL(SpiceyPyError):
    pass


class SpiceBARYCENTERIDCODE(SpiceyPyError):
    pass


class SpiceBEFOREBEGSTR(SpiceyPyError):
    pass


class SpiceBLANKCOMMANDLINE(SpiceyPyError):
    pass


class SpiceBLANKFILETYPE(SpiceyPyError):
    pass


class SpiceBLANKINPUTFILENAME(SpiceyPyError):
    pass


class SpiceBLANKINPUTTIME(SpiceyPyError):
    pass


class SpiceBLANKNAMEASSIGNED(SpiceyPyError):
    pass


class SpiceBLANKOUTPTFILENAME(SpiceyPyError):
    pass


class SpiceBLANKSCLKSTRING(SpiceyPyError):
    pass


class SpiceBLANKTIMEFORMAT(SpiceyPyError):
    pass


class SpiceBLOCKSNOTEVEN(SpiceyPyError):
    pass


class SpiceBOGUSENTRY(SpiceyPyError):
    pass


class SpiceBOUNDSDISAGREE(SpiceyPyError):
    pass


class SpiceBUFFEROVERRUN1(SpiceyPyError):
    pass


class SpiceBUFFEROVERRUN2(SpiceyPyError):
    pass


class SpiceBUFFEROVERRUN3(SpiceyPyError):
    pass


class SpiceBUFFEROVERRUN4(SpiceyPyError):
    pass


class SpiceBUFFERSIZESMISMATCH(SpiceyPyError):
    pass


class SpiceBUFFERTOOSMALL(SpiceyPyError):
    pass


class SpiceBUG0(SpiceyPyError):
    pass


class SpiceBUG1(SpiceyPyError):
    pass


class SpiceBUG2(SpiceyPyError):
    pass


class SpiceBUG3(SpiceyPyError):
    pass


class SpiceBUG4(SpiceyPyError):
    pass


class SpiceBUG5(SpiceyPyError):
    pass


class SpiceBUGWRITEFAILED(SpiceyPyError):
    pass


class SpiceCALLCKBSSFIRST(SpiceyPyError):
    pass


class SpiceCALLEDOUTOFORDER(SpiceyPyError):
    pass


class SpiceCALLZZDSKBSSFIRST(SpiceyPyError):
    pass


class SpiceCANNOTFINDGRP(SpiceyPyError):
    pass


class SpiceCANNOTGETDEFAULTS1(SpiceyPyError):
    pass


class SpiceCANNOTGETDEFAULTS2(SpiceyPyError):
    pass


class SpiceCANNOTGETPACKET(SpiceyPyError):
    pass


class SpiceCANNOTMAKEFILE(SpiceyPyError):
    pass


class SpiceCANNOTPICKFRAME(SpiceyPyError):
    pass


class SpiceCANTGETROTATIONTYPE(SpiceyPyError):
    pass


class SpiceCANTPICKDEFAULTS1(SpiceyPyError):
    pass


class SpiceCANTPICKDEFAULTS2(SpiceyPyError):
    pass


class SpiceCANTPICKDEFAULTS3(SpiceyPyError):
    pass


class SpiceCANTPICKDEFAULTS4(SpiceyPyError):
    pass


class SpiceCANTUSEPERIAPEPOCH(SpiceyPyError):
    pass


class SpiceCBNOSUCHSTR(SpiceyPyError):
    pass


class SpiceCELLARRAYTOOSMALL(SpiceyPyError):
    pass


class SpiceCHRONOSBUG1(SpiceyPyError):
    pass


class SpiceCHRONOSBUG10(SpiceyPyError):
    pass


class SpiceCHRONOSBUG2(SpiceyPyError):
    pass


class SpiceCHRONOSBUG3(SpiceyPyError):
    pass


class SpiceCHRONOSBUG4(SpiceyPyError):
    pass


class SpiceCHRONOSBUG5(SpiceyPyError):
    pass


class SpiceCHRONOSBUG6(SpiceyPyError):
    pass


class SpiceCHRONOSBUG7(SpiceyPyError):
    pass


class SpiceCHRONOSBUG8(SpiceyPyError):
    pass


class SpiceCHRONOSBUG9(SpiceyPyError):
    pass


class SpiceCK3SDNBUG(SpiceyPyError):
    pass


class SpiceCKBOGUSENTRY(SpiceyPyError):
    pass


class SpiceCKDOESNTEXIST(SpiceyPyError):
    pass


class SpiceCKFILE(SpiceyPyError):
    pass


class SpiceCKNONEXISTREC(SpiceyPyError):
    pass


class SpiceCKUNKNOWNDATATYPE(SpiceyPyError):
    pass


class SpiceCKWRONGDATATYPE(SpiceyPyError):
    pass


class SpiceCLIBCALLFAILED(SpiceyPyError):
    pass


class SpiceCLUSTERWRITEERROR(SpiceyPyError):
    pass


class SpiceCMDERROR(SpiceyPyError):
    pass


class SpiceCMDPARSEERROR(SpiceyPyError):
    pass


class SpiceCOARSEGRIDOVERFLOW(SpiceyPyError):
    pass


class SpiceCOLDESCTABLEFULL(SpiceyPyError):
    pass


class SpiceCOMMANDTOOLONG(SpiceyPyError):
    pass


class SpiceCOMMFILENOTEXIST(SpiceyPyError):
    pass


class SpiceCOMPETINGEPOCHSPEC(SpiceyPyError):
    pass


class SpiceCOMPETINGFRAMESPEC(SpiceyPyError):
    pass


class SpiceCOUNTMISMATCH(SpiceyPyError):
    pass


class SpiceCOUNTTOOLARGE(SpiceyPyError):
    pass


class SpiceCOVFRAME1MISMATCH(SpiceyPyError):
    pass


class SpiceCOVFRAME1NODATA1(SpiceyPyError):
    pass


class SpiceCOVFRAME1NODATA2(SpiceyPyError):
    pass


class SpiceCOVFRAME2MISMATCH(SpiceyPyError):
    pass


class SpiceCOVFRAME2NODATA1(SpiceyPyError):
    pass


class SpiceCOVFRAME2NODATA2(SpiceyPyError):
    pass


class SpiceDAFBADCRECLEN(SpiceyPyError):
    pass


class SpiceDAFBADRECLEN(SpiceyPyError):
    pass


class SpiceDAFCRNOTFOUND(SpiceyPyError):
    pass


class SpiceDAFDPWRITEFAIL(SpiceyPyError):
    pass


class SpiceDAFILLEGWRITE(SpiceyPyError):
    pass


class SpiceDAFINVALIDACCESS(SpiceyPyError):
    pass


class SpiceDAFINVALIDPARAMS(SpiceyPyError):
    pass


class SpiceDAFNEWCONFLICT(SpiceyPyError):
    pass


class SpiceDAFNOIDWORD(SpiceyPyError):
    pass


class SpiceDAFNOIFNMATCH(SpiceyPyError):
    pass


class SpiceDAFNONAMEMATCH(SpiceyPyError):
    pass


class SpiceDAFNORESV(SpiceyPyError):
    pass


class SpiceDAFNOSUCHADDR(SpiceyPyError):
    pass


class SpiceDAFNOSUCHFILE(SpiceyPyError):
    pass


class SpiceDAFNOSUCHHANDLE(SpiceyPyError):
    pass


class SpiceDAFNOSUCHUNIT(SpiceyPyError):
    pass


class SpiceDAFNOWRITE(SpiceyPyError):
    pass


class SpiceDAFOVERFLOW(SpiceyPyError):
    pass


class SpiceDAFREADFAIL(SpiceyPyError):
    pass


class SpiceDAFWRITEFAIL(SpiceyPyError):
    pass


class SpiceDASFILEWRITEFAILED(SpiceyPyError):
    pass


class SpiceDASIDWORDNOTKNOWN(SpiceyPyError):
    pass


class SpiceDASINVALIDACCESS(SpiceyPyError):
    pass


class SpiceDASINVALIDCOUNT(SpiceyPyError):
    pass


class SpiceDASINVALIDTYPE(SpiceyPyError):
    pass


class SpiceDASNOIDWORD(SpiceyPyError):
    pass


class SpiceDASNOSUCHADDRESS(SpiceyPyError):
    pass


class SpiceDASNOSUCHFILE(SpiceyPyError):
    pass


class SpiceDASNOSUCHUNIT(SpiceyPyError):
    pass


class SpiceDASNOTEMPTY(SpiceyPyError):
    pass


class SpiceDASREADFAIL(SpiceyPyError):
    pass


class SpiceDASWRITEFAIL(SpiceyPyError):
    pass


class SpiceDATAITEMLIMITEXCEEDED(SpiceyPyError):
    pass


class SpiceDATAREADFAILED(SpiceyPyError):
    pass


class SpiceDATATYPENOTRECOG(SpiceyPyError):
    pass


class SpiceDATAWIDTHERROR(SpiceyPyError):
    pass


class SpiceDATEEXPECTED(SpiceyPyError):
    pass


class SpiceDECODINGERROR(SpiceyPyError):
    pass


class SpiceDIFFLINETOOLARGE(SpiceyPyError):
    pass


class SpiceDIFFLINETOOSMALL(SpiceyPyError):
    pass


class SpiceDIMENSIONTOOSMALL(SpiceyPyError):
    pass


class SpiceDISARRAY(SpiceyPyError):
    pass


class SpiceDISORDER(SpiceyPyError):
    pass


class SpiceDSKBOGUSENTRY(SpiceyPyError):
    pass


class SpiceDSKDATANOTFOUND(SpiceyPyError):
    pass


class SpiceDSKTOOMANYFILES(SpiceyPyError):
    pass


class SpiceDUPLICATETIMES(SpiceyPyError):
    pass


class SpiceECCOUTOFBOUNDS(SpiceyPyError):
    pass


class SpiceEKCOLNUMMISMATCH(SpiceyPyError):
    pass


class SpiceEKFILE(SpiceyPyError):
    pass


class SpiceEKMISSINGCOLUMN(SpiceyPyError):
    pass


class SpiceEKSEGTABLEFULL(SpiceyPyError):
    pass


class SpiceEKTABLELISTFULL(SpiceyPyError):
    pass


class SpiceEMBEDDEDBLANK(SpiceyPyError):
    pass


class SpiceEMPTYINPUTFILE(SpiceyPyError):
    pass


class SpiceENDOFFILE(SpiceyPyError):
    pass


class SpiceENDPOINTSMATCH(SpiceyPyError):
    pass


class SpiceERROREXIT(SpiceyPyError):
    pass


class SpiceEVECOUTOFRANGE(SpiceyPyError):
    pass


class SpiceEVENHERMITDEGREE(SpiceyPyError):
    pass


class SpiceEVILBOGUSENTRY(SpiceyPyError):
    pass


class SpiceEXTERNALOPEN(SpiceyPyError):
    pass


class SpiceFACENOTFOUND(SpiceyPyError):
    pass


class SpiceFAKESCLKEXISTS(SpiceyPyError):
    pass


class SpiceFILARCHMISMATCH(SpiceyPyError):
    pass


class SpiceFILARCMISMATCH(SpiceyPyError):
    pass


class SpiceFILEALREADYEXISTS(SpiceyPyError):
    pass


class SpiceFILEALREADYOPEN(SpiceyPyError):
    pass


class SpiceFILEDELETEFAILED(SpiceyPyError):
    pass


class SpiceFILEDOESNTEXIST1(SpiceyPyError):
    pass


class SpiceFILEDOESNTEXIST2(SpiceyPyError):
    pass


class SpiceFILEDOESNTEXIST3(SpiceyPyError):
    pass


class SpiceFILEEXISTS(SpiceyPyError):
    pass


class SpiceFILENAMETOOLONG(SpiceyPyError):
    pass


class SpiceFILENOTCONNECTED(SpiceyPyError):
    pass


class SpiceFILENOTOPEN(SpiceyPyError):
    pass


class SpiceFILEOPENCONFLICT(SpiceyPyError):
    pass


class SpiceFILEOPENERROR(SpiceyPyError):
    pass


class SpiceFILEOPENFAIL(SpiceyPyError):
    pass


class SpiceFILEREADERROR(SpiceyPyError):
    pass


class SpiceFILETABLEFULL(SpiceyPyError):
    pass


class SpiceFILETRUNCATED(SpiceyPyError):
    pass


class SpiceFILEWRITEFAILED(SpiceyPyError):
    pass


class SpiceFIRSTRECORDMISMATCH(SpiceyPyError):
    pass


class SpiceFKDOESNTEXIST(SpiceyPyError):
    pass


class SpiceFMTITEMLIMITEXCEEDED(SpiceyPyError):
    pass


class SpiceFORMATDATAMISMATCH(SpiceyPyError):
    pass


class SpiceFORMATDOESNTAPPLY(SpiceyPyError):
    pass


class SpiceFORMATERROR(SpiceyPyError):
    pass


class SpiceFORMATITEMLIMITEXCEEDED(SpiceyPyError):
    pass


class SpiceFORMATNOTAPPLICABLE(SpiceyPyError):
    pass


class SpiceFORMATSTRINGTOOLONG(SpiceyPyError):
    pass


class SpiceFOVTOOWIDE(SpiceyPyError):
    pass


class SpiceFRAMEAIDCODENOTFOUND(SpiceyPyError):
    pass


class SpiceFRAMEBIDCODENOTFOUND(SpiceyPyError):
    pass


class SpiceFRAMEDATANOTFOUND(SpiceyPyError):
    pass


class SpiceFRAMEDEFERROR(SpiceyPyError):
    pass


class SpiceFRAMEINFONOTFOUND(SpiceyPyError):
    pass


class SpiceFRAMENOTFOUND(SpiceyPyError):
    pass


class SpiceFRAMENOTRECOGNIZED(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG1(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG2(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG3(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG4(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG5(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG6(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG7(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG8(SpiceyPyError):
    pass


class SpiceFRMDIFFBUG9(SpiceyPyError):
    pass


class SpiceFTFULL(SpiceyPyError):
    pass


class SpiceFTPXFERERROR(SpiceyPyError):
    pass


class SpiceHANDLENOTFOUND(SpiceyPyError):
    pass


class SpiceHASHISFULL(SpiceyPyError):
    pass


class SpiceHLULOCKFAILED(SpiceyPyError):
    pass


class SpiceIDENTICALTIMES1(SpiceyPyError):
    pass


class SpiceIDENTICALTIMES2(SpiceyPyError):
    pass


class SpiceIDSTRINGTOOLONG(SpiceyPyError):
    pass


class SpiceIDWORDNOTKNOWN(SpiceyPyError):
    pass


class SpiceILLEGALOPTIONNAME(SpiceyPyError):
    pass


class SpiceILLEGSHIFTDIR(SpiceyPyError):
    pass


class SpiceILLEGTEMPL(SpiceyPyError):
    pass


class SpiceIMPROPERFILE(SpiceyPyError):
    pass


class SpiceIMPROPEROPEN(SpiceyPyError):
    pass


class SpiceINACTIVEOBJECT(SpiceyPyError):
    pass


class SpiceINCOMPATIBLEEOL(SpiceyPyError):
    pass


class SpiceINCOMPATIBLENUMREF(SpiceyPyError):
    pass


class SpiceINCOMPLETEELEMENTS(SpiceyPyError):
    pass


class SpiceINCOMPLETEFRAME(SpiceyPyError):
    pass


class SpiceINCOMPLETFRAME(SpiceyPyError):
    pass


class SpiceINCONSISTCENTERID(SpiceyPyError):
    pass


class SpiceINCONSISTELEMENTS(SpiceyPyError):
    pass


class SpiceINCONSISTENTTIMES(SpiceyPyError):
    pass


class SpiceINCONSISTENTTIMES1(SpiceyPyError):
    pass


class SpiceINCONSISTENTTIMES2(SpiceyPyError):
    pass


class SpiceINCONSISTFRAME(SpiceyPyError):
    pass


class SpiceINCONSISTSTARTTIME(SpiceyPyError):
    pass


class SpiceINCONSISTSTOPTIME(SpiceyPyError):
    pass


class SpiceINCORRECTUSAGE(SpiceyPyError):
    pass


class SpiceINDEFINITELOCALSECOND(SpiceyPyError):
    pass


class SpiceINDEXTOOLARGE(SpiceyPyError):
    pass


class SpiceINDICESOUTOFORDER(SpiceyPyError):
    pass


class SpiceINPUTDOESNOTEXIST(SpiceyPyError):
    pass


class SpiceINPUTFILENOTEXIST(SpiceyPyError):
    pass


class SpiceINPUTOUTOFBOUNDS(SpiceyPyError):
    pass


class SpiceINSIDEBODY(SpiceyPyError):
    pass


class SpiceINSUFFICIENTDATA(SpiceyPyError):
    pass


class SpiceINSUFFICIENTDATA2(SpiceyPyError):
    pass


class SpiceINSUFPTRSIZE(SpiceyPyError):
    pass


class SpiceINTERVALSTARTNOTFOUND(SpiceyPyError):
    pass


class SpiceINVALDDEGREE(SpiceyPyError):
    pass


class SpiceINVALIDACCESS(SpiceyPyError):
    pass


class SpiceINVALIDADD(SpiceyPyError):
    pass


class SpiceINVALIDADDRESS(SpiceyPyError):
    pass


class SpiceINVALIDANGLE(SpiceyPyError):
    pass


class SpiceINVALIDAXES(SpiceyPyError):
    pass


class SpiceINVALIDAXIS(SpiceyPyError):
    pass


class SpiceINVALIDBOUNDS(SpiceyPyError):
    pass


class SpiceINVALIDCASE(SpiceyPyError):
    pass


class SpiceINVALIDCHECKOUT(SpiceyPyError):
    pass


class SpiceINVALIDCLUSTERNUM(SpiceyPyError):
    pass


class SpiceINVALIDCOLUMN(SpiceyPyError):
    pass


class SpiceINVALIDCONSTSTEP(SpiceyPyError):
    pass


class SpiceINVALIDDATA(SpiceyPyError):
    pass


class SpiceINVALIDDATACOUNT(SpiceyPyError):
    pass


class SpiceINVALIDDATATYPE(SpiceyPyError):
    pass


class SpiceINVALIDDIRECTION(SpiceyPyError):
    pass


class SpiceINVALIDDIVISOR(SpiceyPyError):
    pass


class SpiceINVALIDENDPTS(SpiceyPyError):
    pass


class SpiceINVALIDFILETYPE(SpiceyPyError):
    pass


class SpiceINVALIDFIXREF(SpiceyPyError):
    pass


class SpiceINVALIDFLAG(SpiceyPyError):
    pass


class SpiceINVALIDFOV(SpiceyPyError):
    pass


class SpiceINVALIDGEOMETRY(SpiceyPyError):
    pass


class SpiceINVALIDHANDLE(SpiceyPyError):
    pass


class SpiceINVALIDINPUT1(SpiceyPyError):
    pass


class SpiceINVALIDINPUT2(SpiceyPyError):
    pass


class SpiceINVALIDINTEGER(SpiceyPyError):
    pass


class SpiceINVALIDMETADATA(SpiceyPyError):
    pass


class SpiceINVALIDNAME(SpiceyPyError):
    pass


class SpiceINVALIDNODE(SpiceyPyError):
    pass


class SpiceINVALIDNUMBEROFINTERVALS(SpiceyPyError):
    pass


class SpiceINVALIDNUMBEROFRECORDS(SpiceyPyError):
    pass


class SpiceINVALIDNUMINT(SpiceyPyError):
    pass


class SpiceINVALIDNUMREC(SpiceyPyError):
    pass


class SpiceINVALIDRADII(SpiceyPyError):
    pass


class SpiceINVALIDREFVAL(SpiceyPyError):
    pass


class SpiceINVALIDSCALE(SpiceyPyError):
    pass


class SpiceINVALIDSCLKRATE(SpiceyPyError):
    pass


class SpiceINVALIDSCLKSTRING1(SpiceyPyError):
    pass


class SpiceINVALIDSCLKSTRING2(SpiceyPyError):
    pass


class SpiceINVALIDSELECTION(SpiceyPyError):
    pass


class SpiceINVALIDSHADOW(SpiceyPyError):
    pass


class SpiceINVALIDSHAPE(SpiceyPyError):
    pass


class SpiceINVALIDSHAPECOMBO(SpiceyPyError):
    pass


class SpiceINVALIDSUBLIST(SpiceyPyError):
    pass


class SpiceINVALIDTABLENAME(SpiceyPyError):
    pass


class SpiceINVALIDTABLESIZE(SpiceyPyError):
    pass


class SpiceINVALIDTEXT(SpiceyPyError):
    pass


class SpiceINVALIDTLEORDER(SpiceyPyError):
    pass


class SpiceINVALIDUNITS(SpiceyPyError):
    pass


class SpiceINVALIDVALUE1(SpiceyPyError):
    pass


class SpiceINVALIDVALUE2(SpiceyPyError):
    pass


class SpiceINVERSTARTSTOPTIME(SpiceyPyError):
    pass


class SpiceINVERSTIMES2(SpiceyPyError):
    pass


class SpiceIRFNOTREC(SpiceyPyError):
    pass


class SpiceITEMNOTFOUND(SpiceyPyError):
    pass


class SpiceITEMNOTRECOGNIZED(SpiceyPyError):
    pass


class SpiceITERATIONEXCEEDED(SpiceyPyError):
    pass


class SpiceJEOPARDIZEDRUN0(SpiceyPyError):
    pass


class SpiceJEOPARDIZEDRUN1(SpiceyPyError):
    pass


class SpiceJEOPARDIZEDRUN2(SpiceyPyError):
    pass


class SpiceJEOPARDIZEDRUN3(SpiceyPyError):
    pass


class SpiceJEOPARDIZEDRUN4(SpiceyPyError):
    pass


class SpiceJEOPARDIZEDRUN5(SpiceyPyError):
    pass


class SpiceKERNELNOTLOADED(SpiceyPyError):
    pass


class SpiceKERVARSETOVERFLOW(SpiceyPyError):
    pass


class SpiceKERVARTOOBIG(SpiceyPyError):
    pass


class SpiceKEYWORDNOTFOUND(SpiceyPyError):
    pass


class SpiceKEYWORDSMISMATCH1(SpiceyPyError):
    pass


class SpiceKEYWORDSMISMATCH2(SpiceyPyError):
    pass


class SpiceKEYWORDSMISMATCH3(SpiceyPyError):
    pass


class SpiceLBCORRUPTED(SpiceyPyError):
    pass


class SpiceLBINSUFPTRSIZE(SpiceyPyError):
    pass


class SpiceLBLINETOOLONG(SpiceyPyError):
    pass


class SpiceLBNOSUCHLINE(SpiceyPyError):
    pass


class SpiceLBTOOMANYLINES(SpiceyPyError):
    pass


class SpiceLOWERBOUNDTOOLOW(SpiceyPyError):
    pass


class SpiceLSKDOESNTEXIST(SpiceyPyError):
    pass


class SpiceMALFORMEDSEGMENT(SpiceyPyError):
    pass


class SpiceMALLOCCOUNT(SpiceyPyError):
    pass


class SpiceMARKERNOTFOUND(SpiceyPyError):
    pass


class SpiceMETA2DEFERR(SpiceyPyError):
    pass


class SpiceMETA2TOOMANYKEYS(SpiceyPyError):
    pass


class SpiceMISMATCHFROMTIMETYPE(SpiceyPyError):
    pass


class SpiceMISMATCHOUTPUTFORMAT(SpiceyPyError):
    pass


class SpiceMISMATCHTOTIMETYPE(SpiceyPyError):
    pass


class SpiceMISSINGARGUMENTS(SpiceyPyError):
    pass


class SpiceMISSINGCENTER(SpiceyPyError):
    pass


class SpiceMISSINGCOLSTEP(SpiceyPyError):
    pass


class SpiceMISSINGCOORDBOUND(SpiceyPyError):
    pass


class SpiceMISSINGCOORDSYS(SpiceyPyError):
    pass


class SpiceMISSINGDATACLASS(SpiceyPyError):
    pass


class SpiceMISSINGDATAORDERTK(SpiceyPyError):
    pass


class SpiceMISSINGDATATYPE(SpiceyPyError):
    pass


class SpiceMISSINGEOT(SpiceyPyError):
    pass


class SpiceMISSINGEPOCHTOKEN(SpiceyPyError):
    pass


class SpiceMISSINGFILENAMES1(SpiceyPyError):
    pass


class SpiceMISSINGFILENAMES2(SpiceyPyError):
    pass


class SpiceMISSINGFILENAMES3(SpiceyPyError):
    pass


class SpiceMISSINGFRAME(SpiceyPyError):
    pass


class SpiceMISSINGFRAMEVAR(SpiceyPyError):
    pass


class SpiceMISSINGGEOCONSTS(SpiceyPyError):
    pass


class SpiceMISSINGHEIGHTREF(SpiceyPyError):
    pass


class SpiceMISSINGHSCALE(SpiceyPyError):
    pass


class SpiceMISSINGKPV(SpiceyPyError):
    pass


class SpiceMISSINGLEFTCOR(SpiceyPyError):
    pass


class SpiceMISSINGLEFTRTFLAG(SpiceyPyError):
    pass


class SpiceMISSINGNCAPFLAG(SpiceyPyError):
    pass


class SpiceMISSINGNCOLS(SpiceyPyError):
    pass


class SpiceMISSINGNROWS(SpiceyPyError):
    pass


class SpiceMISSINGPLATETYPE(SpiceyPyError):
    pass


class SpiceMISSINGROWMAJFLAG(SpiceyPyError):
    pass


class SpiceMISSINGROWSTEP(SpiceyPyError):
    pass


class SpiceMISSINGSCAPFLAG(SpiceyPyError):
    pass


class SpiceMISSINGSURFACE(SpiceyPyError):
    pass


class SpiceMISSINGTLEIDKEYWORD(SpiceyPyError):
    pass


class SpiceMISSINGTLEKEYWORD(SpiceyPyError):
    pass


class SpiceMISSINGTOPCOR(SpiceyPyError):
    pass


class SpiceMISSINGTOPDOWNFLAG(SpiceyPyError):
    pass


class SpiceMISSINGVOXELSCALE(SpiceyPyError):
    pass


class SpiceMISSINGWRAPFLAG(SpiceyPyError):
    pass


class SpiceMKSPKBUG3(SpiceyPyError):
    pass


class SpiceMKSPKBUGSETUP1(SpiceyPyError):
    pass


class SpiceMKSPKBUGSETUP2(SpiceyPyError):
    pass


class SpiceMKSPKBUGSETUP3(SpiceyPyError):
    pass


class SpiceMKSPKBUGSETUP4(SpiceyPyError):
    pass


class SpiceMKSPKBUGSETUP5(SpiceyPyError):
    pass


class SpiceMKSPKTLE2SPKBUG0(SpiceyPyError):
    pass


class SpiceMKSPKTLE2SPKBUG1(SpiceyPyError):
    pass


class SpiceMKSPKTLE2SPKBUG2(SpiceyPyError):
    pass


class SpiceMKSPKTLE2SPKBUG3(SpiceyPyError):
    pass


class SpiceMKSPKTLE2SPKBUG4(SpiceyPyError):
    pass


class SpiceMSGNAME(SpiceyPyError):
    pass


class SpiceNAMENOTFOUND(SpiceyPyError):
    pass


class SpiceNAMENOTRECOGNIZED(SpiceyPyError):
    pass


class SpiceNAMENOTUNIQUE(SpiceyPyError):
    pass


class SpiceNAMESNOTRESOLVED(SpiceyPyError):
    pass


class SpiceNAMETABLEFULL(SpiceyPyError):
    pass


class SpiceNARATESFLAG(SpiceyPyError):
    pass


class SpiceNEGATIVEHASHVALUE1(SpiceyPyError):
    pass


class SpiceNEGATIVEHASHVALUE2(SpiceyPyError):
    pass


class SpiceNEGATIVETOL(SpiceyPyError):
    pass


class SpiceNOACCEPTABLEDATA(SpiceyPyError):
    pass


class SpiceNOANGULARRATEFLAG(SpiceyPyError):
    pass


class SpiceNOARRAYSTARTED(SpiceyPyError):
    pass


class SpiceNOATTIME(SpiceyPyError):
    pass


class SpiceNOAVDATA(SpiceyPyError):
    pass


class SpiceNOBODYID(SpiceyPyError):
    pass


class SpiceNOCANDOSPKSPCKS(SpiceyPyError):
    pass


class SpiceNOCENTERIDORNAME(SpiceyPyError):
    pass


class SpiceNOCKSEGMENTTYPE(SpiceyPyError):
    pass


class SpiceNOCOMMENTSFILE(SpiceyPyError):
    pass


class SpiceNOCONVERG(SpiceyPyError):
    pass


class SpiceNOCONVERGENCE(SpiceyPyError):
    pass


class SpiceNODATA(SpiceyPyError):
    pass


class SpiceNODATAORDER(SpiceyPyError):
    pass


class SpiceNODATATYPEFLAG(SpiceyPyError):
    pass


class SpiceNODELIMCHARACTER(SpiceyPyError):
    pass


class SpiceNODETOOFULL(SpiceyPyError):
    pass


class SpiceNODSKSEGMENT(SpiceyPyError):
    pass


class SpiceNODSKSEGMENTS(SpiceyPyError):
    pass


class SpiceNOENVVARIABLE(SpiceyPyError):
    pass


class SpiceNOEULERANGLEUNITS(SpiceyPyError):
    pass


class SpiceNOFILENAMES(SpiceyPyError):
    pass


class SpiceNOFILES(SpiceyPyError):
    pass


class SpiceNOFILESPEC(SpiceyPyError):
    pass


class SpiceNOFRAMECONNECT(SpiceyPyError):
    pass


class SpiceNOFRAMEDATA(SpiceyPyError):
    pass


class SpiceNOFRAMENAME(SpiceyPyError):
    pass


class SpiceNOFRAMESKERNELNAME(SpiceyPyError):
    pass


class SpiceNOFREELOGICALUNIT(SpiceyPyError):
    pass


class SpiceNOFREENODES(SpiceyPyError):
    pass


class SpiceNOFROMTIME(SpiceyPyError):
    pass


class SpiceNOFROMTIMESYSTEM(SpiceyPyError):
    pass


class SpiceNOHEADNODE(SpiceyPyError):
    pass


class SpiceNOINFO(SpiceyPyError):
    pass


class SpiceNOINPUTDATATYPE(SpiceyPyError):
    pass


class SpiceNOINPUTFILENAME(SpiceyPyError):
    pass


class SpiceNOINSTRUMENTID(SpiceyPyError):
    pass


class SpiceNOKERNELLOADED(SpiceyPyError):
    pass


class SpiceNOLANDINGTIME(SpiceyPyError):
    pass


class SpiceNOLEAPSECONDS(SpiceyPyError):
    pass


class SpiceNOLINESPERRECCOUNT(SpiceyPyError):
    pass


class SpiceNOLISTFILENAME(SpiceyPyError):
    pass


class SpiceNOLOADEDDSKFILES(SpiceyPyError):
    pass


class SpiceNOLSKFILENAME(SpiceyPyError):
    pass


class SpiceNONAPPLICABLETYPE1(SpiceyPyError):
    pass


class SpiceNONAPPLICABLETYPE2(SpiceyPyError):
    pass


class SpiceNONDISTINCTPAIR(SpiceyPyError):
    pass


class SpiceNONEMPTYENTRY(SpiceyPyError):
    pass


class SpiceNONEMPTYTREE(SpiceyPyError):
    pass


class SpiceNONEXISTELEMENTS(SpiceyPyError):
    pass


class SpiceNONINTEGERFIELD(SpiceyPyError):
    pass


class SpiceNONNUMERICSTRING(SpiceyPyError):
    pass


class SpiceNONPOSBUFLENGTH(SpiceyPyError):
    pass


class SpiceNONPOSITIVEAXIS(SpiceyPyError):
    pass


class SpiceNONPOSITIVERADIUS(SpiceyPyError):
    pass


class SpiceNONPOSITIVEVALUE(SpiceyPyError):
    pass


class SpiceNONPOSPACKETSIZE(SpiceyPyError):
    pass


class SpiceNONPRINTINGCHAR(SpiceyPyError):
    pass


class SpiceNONPRINTINGCHARS(SpiceyPyError):
    pass


class SpiceNONUNITNORMAL(SpiceyPyError):
    pass


class SpiceNONUNITQUATERNION(SpiceyPyError):
    pass


class SpiceNOOBJECTIDORNAME(SpiceyPyError):
    pass


class SpiceNOOFFSETANGLEAXES(SpiceyPyError):
    pass


class SpiceNOOFFSETANGLEUNITS(SpiceyPyError):
    pass


class SpiceNOOUTPUTFILENAME(SpiceyPyError):
    pass


class SpiceNOOUTPUTSPKTYPE(SpiceyPyError):
    pass


class SpiceNOPICTURE(SpiceyPyError):
    pass


class SpiceNOPLATES(SpiceyPyError):
    pass


class SpiceNOPOLYNOMIALDEGREE(SpiceyPyError):
    pass


class SpiceNOPRECESSIONTYPE(SpiceyPyError):
    pass


class SpiceNOPRODUCERID(SpiceyPyError):
    pass


class SpiceNORATESFORTYPE2CK(SpiceyPyError):
    pass


class SpiceNOROTATIONORDER(SpiceyPyError):
    pass


class SpiceNOSCID(SpiceyPyError):
    pass


class SpiceNOSCLKFILENAMES(SpiceyPyError):
    pass


class SpiceNOSECONDLINE(SpiceyPyError):
    pass


class SpiceNOSECONDLINE2(SpiceyPyError):
    pass


class SpiceNOSEGMENT(SpiceyPyError):
    pass


class SpiceNOSLKFILENAME(SpiceyPyError):
    pass


class SpiceNOSOLMARKER(SpiceyPyError):
    pass


class SpiceNOSPACECRAFTID(SpiceyPyError):
    pass


class SpiceNOSTARTTIME(SpiceyPyError):
    pass


class SpiceNOSTARTTIME4SPK15(SpiceyPyError):
    pass


class SpiceNOSTARTTIME4SPK17(SpiceyPyError):
    pass


class SpiceNOSTOPTIME(SpiceyPyError):
    pass


class SpiceNOSTOPTIME4SPK15(SpiceyPyError):
    pass


class SpiceNOSTOPTIME4SPK17(SpiceyPyError):
    pass


class SpiceNOSUCHHANDLE(SpiceyPyError):
    pass


class SpiceNOSUCHSYMBOL(SpiceyPyError):
    pass


class SpiceNOSUNGM(SpiceyPyError):
    pass


class SpiceNOSURFACENAME(SpiceyPyError):
    pass


class SpiceNOTABINARYKERNEL(SpiceyPyError):
    pass


class SpiceNOTACKFILE(SpiceyPyError):
    pass


class SpiceNOTAKERNELFILE1(SpiceyPyError):
    pass


class SpiceNOTAKERNELFILE2(SpiceyPyError):
    pass


class SpiceNOTANDPNUMBER(SpiceyPyError):
    pass


class SpiceNOTANINTEGERNUMBER(SpiceyPyError):
    pass


class SpiceNOTANINTNUMBER(SpiceyPyError):
    pass


class SpiceNOTANINTNUMBER2(SpiceyPyError):
    pass


class SpiceNOTAPCKFILE(SpiceyPyError):
    pass


class SpiceNOTATEXTFILE(SpiceyPyError):
    pass


class SpiceNOTATRANSFERFILE(SpiceyPyError):
    pass


class SpiceNOTCOMPUTABLE(SpiceyPyError):
    pass


class SpiceNOTDIMENSIONALLYEQUIV(SpiceyPyError):
    pass


class SpiceNOTDISJOINT(SpiceyPyError):
    pass


class SpiceNOTDISTINCT(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA0(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA1(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA2(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA3(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA4(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA5(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA6(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA7(SpiceyPyError):
    pass


class SpiceNOTENOUGHDATA8(SpiceyPyError):
    pass


class SpiceNOTENOUGHPEAS(SpiceyPyError):
    pass


class SpiceNOTFOUND(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS1(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS10(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS11(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS12(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS4(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS5(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS6(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS7(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS8(SpiceyPyError):
    pass


class SpiceNOTIMEBOUNDS9(SpiceyPyError):
    pass


class SpiceNOTIMETYPEFLAG(SpiceyPyError):
    pass


class SpiceNOTINDEXED(SpiceyPyError):
    pass


class SpiceNOTINTEGERNUMBER2(SpiceyPyError):
    pass


class SpiceNOTISOFORMAT(SpiceyPyError):
    pass


class SpiceNOTLEDATAFOROBJECT(SpiceyPyError):
    pass


class SpiceNOTLEGALCB(SpiceyPyError):
    pass


class SpiceNOTOTIME(SpiceyPyError):
    pass


class SpiceNOTOTIMESYSTEM(SpiceyPyError):
    pass


class SpiceNOTPOSITIVE(SpiceyPyError):
    pass


class SpiceNOTSEMCHECKED(SpiceyPyError):
    pass


class SpiceNOTTWOFIELDSCLK(SpiceyPyError):
    pass


class SpiceNOTTWOMODULI(SpiceyPyError):
    pass


class SpiceNOTTWOOFFSETS(SpiceyPyError):
    pass


class SpiceNOTTYPE1SCLK(SpiceyPyError):
    pass


class SpiceNOUNITSPEC(SpiceyPyError):
    pass


class SpiceNUMBEREXPECTED(SpiceyPyError):
    pass


class SpiceNUMCONSTANTSNEG(SpiceyPyError):
    pass


class SpiceNUMPACKETSNOTPOS(SpiceyPyError):
    pass


class SpiceOBJECTLISTFULL(SpiceyPyError):
    pass


class SpiceOBJECTSTOOCLOSE(SpiceyPyError):
    pass


class SpiceOBSIDCODENOTFOUND(SpiceyPyError):
    pass


class SpiceORBITDECAY(SpiceyPyError):
    pass


class SpiceOUTOFPLACEDELIMITER(SpiceyPyError):
    pass


class SpiceOUTOFRANGE(SpiceyPyError):
    pass


class SpiceOUTPUTERROR(SpiceyPyError):
    pass


class SpiceOUTPUTFILEEXISTS(SpiceyPyError):
    pass


class SpiceOUTPUTISNOTSPK(SpiceyPyError):
    pass


class SpiceOUTPUTTOOLONG(SpiceyPyError):
    pass


class SpiceOUTPUTTOOSHORT(SpiceyPyError):
    pass


class SpicePARSERNOTREADY(SpiceyPyError):
    pass


class SpicePARTIALFRAMESPEC(SpiceyPyError):
    pass


class SpicePASTENDSTR(SpiceyPyError):
    pass


class SpicePATHMISMATCH(SpiceyPyError):
    pass


class SpicePATHTOOLONG(SpiceyPyError):
    pass


class SpicePCKDOESNTEXIST(SpiceyPyError):
    pass


class SpicePCKFILE(SpiceyPyError):
    pass


class SpicePCKKRECTOOLARGE(SpiceyPyError):
    pass


class SpicePCKRECTOOLARGE(SpiceyPyError):
    pass


class SpicePOINTEROUTOFRANGE(SpiceyPyError):
    pass


class SpicePOINTERSETTOOBIG(SpiceyPyError):
    pass


class SpicePOINTERTABLEFULL(SpiceyPyError):
    pass


class SpicePOINTNOTFOUND(SpiceyPyError):
    pass


class SpicePOINTNOTINSEGMENT(SpiceyPyError):
    pass


class SpicePOINTOFFSURFACE(SpiceyPyError):
    pass


class SpicePOINTTOOSMALL(SpiceyPyError):
    pass


class SpicePUTCMLCALLEDTWICE(SpiceyPyError):
    pass


class SpicePUTCMLNOTCALLED(SpiceyPyError):
    pass


class SpiceQPARAMOUTOFRANGE(SpiceyPyError):
    pass


class SpiceQUERYFAILURE(SpiceyPyError):
    pass


class SpiceQUERYNOTPARSED(SpiceyPyError):
    pass


class SpiceRADIIOUTOFORDER(SpiceyPyError):
    pass


class SpiceRAYISZEROVECTOR(SpiceyPyError):
    pass


class SpiceREADFAILED(SpiceyPyError):
    pass


class SpiceREADFAILURE(SpiceyPyError):
    pass


class SpiceRECORDNOTFOUND(SpiceyPyError):
    pass


class SpiceRECURSIONTOODEEP(SpiceyPyError):
    pass


class SpiceREFNOTREC(SpiceyPyError):
    pass


class SpiceREFVALNOTINTEGER(SpiceyPyError):
    pass


class SpiceREPORTTOOWIDE(SpiceyPyError):
    pass


class SpiceREQUESTOUTOFBOUNDS(SpiceyPyError):
    pass


class SpiceREQUESTOUTOFORDER(SpiceyPyError):
    pass


class SpiceRWCONFLICT(SpiceyPyError):
    pass


class SpiceSAMEBODY1CENTER1(SpiceyPyError):
    pass


class SpiceSAMEBODY1CENTER2(SpiceyPyError):
    pass


class SpiceSAMEBODY2CENTER1(SpiceyPyError):
    pass


class SpiceSAMEBODY2CENTER2(SpiceyPyError):
    pass


class SpiceSAMEBODYANDCENTER3(SpiceyPyError):
    pass


class SpiceSAMEBODYANDCENTER4(SpiceyPyError):
    pass


class SpiceSBINSUFPTRSIZE(SpiceyPyError):
    pass


class SpiceSBTOOMANYSTRS(SpiceyPyError):
    pass


class SpiceSCLKDOESNTEXIST(SpiceyPyError):
    pass


class SpiceSEGMENTNOTFOUND(SpiceyPyError):
    pass


class SpiceSEGMENTTABLEFULL(SpiceyPyError):
    pass


class SpiceSEGTABLETOOSMALL(SpiceyPyError):
    pass


class SpiceSEGTYPECONFLICT(SpiceyPyError):
    pass


class SpiceSETTOOSMALL(SpiceyPyError):
    pass


class SpiceSETUPDOESNOTEXIST(SpiceyPyError):
    pass


class SpiceSIZEMISMATCH(SpiceyPyError):
    pass


class SpiceSIZEOUTOFRANGE(SpiceyPyError):
    pass


class SpiceSPACETOONARROW(SpiceyPyError):
    pass


class SpiceSPCRFLNOTCALLED(SpiceyPyError):
    pass


class SpiceSPICEISTIRED(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG1(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG10(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG11(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG12(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG2(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG3(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG5(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG6(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG7(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG8(SpiceyPyError):
    pass


class SpiceSPKDIFFBUG9(SpiceyPyError):
    pass


class SpiceSPKDOESNTEXIST(SpiceyPyError):
    pass


class SpiceSPKFILE(SpiceyPyError):
    pass


class SpiceSPKRECTOOLARGE(SpiceyPyError):
    pass


class SpiceSPKREFNOTSUPP(SpiceyPyError):
    pass


class SpiceSPKSTRUCTUREERROR(SpiceyPyError):
    pass


class SpiceSPKTYPENOTSUPPORTD(SpiceyPyError):
    pass


class SpiceSPURIOUSFLAG(SpiceyPyError):
    pass


class SpiceSPURIOUSKEYWORD(SpiceyPyError):
    pass


class SpiceSTEPTOOSMALL1(SpiceyPyError):
    pass


class SpiceSTEPTOOSMALL2(SpiceyPyError):
    pass


class SpiceSTFULL(SpiceyPyError):
    pass


class SpiceSTRINGCONVERROR(SpiceyPyError):
    pass


class SpiceSTRINGCOPYFAIL(SpiceyPyError):
    pass


class SpiceSTRINGCREATEFAIL(SpiceyPyError):
    pass


class SpiceSTRINGTOOSMALL(SpiceyPyError):
    pass


class SpiceSTRINGTRUNCATED(SpiceyPyError):
    pass


class SpiceSUBORBITAL(SpiceyPyError):
    pass


class SpiceSYNTAXERROR(SpiceyPyError):
    pass


class SpiceSYSTEMCALLFAILED(SpiceyPyError):
    pass


class SpiceTARGIDCODENOTFOUND(SpiceyPyError):
    pass


class SpiceTIMEOUTOFBOUNDS(SpiceyPyError):
    pass


class SpiceTIMESYSTEMPROBLEM(SpiceyPyError):
    pass


class SpiceTIMEZONEERROR(SpiceyPyError):
    pass


class SpiceTOOFEWINPUTLINES(SpiceyPyError):
    pass


class SpiceTOOFEWWINDOWS(SpiceyPyError):
    pass


class SpiceTOOMANYBASEFRAMES(SpiceyPyError):
    pass


class SpiceTOOMANYCOLUMNS(SpiceyPyError):
    pass


class SpiceTOOMANYFIELDS(SpiceyPyError):
    pass


class SpiceTOOMANYHITS(SpiceyPyError):
    pass


class SpiceTOOMANYITERATIONS(SpiceyPyError):
    pass


class SpiceTOOMANYKEYWORDS(SpiceyPyError):
    pass


class SpiceTOOMANYPAIRS(SpiceyPyError):
    pass


class SpiceTOOMANYPEAS(SpiceyPyError):
    pass


class SpiceTOOMANYPLATES(SpiceyPyError):
    pass


class SpiceTOOMANYSURFACES(SpiceyPyError):
    pass


class SpiceTOOMANYVERTICES(SpiceyPyError):
    pass


class SpiceTOOMANYWATCHES(SpiceyPyError):
    pass


class SpiceTRANSFERFILE(SpiceyPyError):
    pass


class SpiceTRANSFERFORMAT(SpiceyPyError):
    pass


class SpiceTWOSCLKFILENAMES(SpiceyPyError):
    pass


class SpiceTYPE1TEXTEK(SpiceyPyError):
    pass


class SpiceTYPENOTSUPPORTED(SpiceyPyError):
    pass


class SpiceTYPESMISMATCH(SpiceyPyError):
    pass


class SpiceUNALLOCATEDNODE(SpiceyPyError):
    pass


class SpiceUNBALACEDPAIR(SpiceyPyError):
    pass


class SpiceUNBALANCEDGROUP(SpiceyPyError):
    pass


class SpiceUNBALANCEDPAIR(SpiceyPyError):
    pass


class SpiceUNEQUALTIMESTEP(SpiceyPyError):
    pass


class SpiceUNINITIALIZED(SpiceyPyError):
    pass


class SpiceUNINITIALIZEDHASH(SpiceyPyError):
    pass


class SpiceUNINITIALIZEDVALUE(SpiceyPyError):
    pass


class SpiceUNKNOWNFRAME2(SpiceyPyError):
    pass


class SpiceUNKNONWNTIMESYSTEM(SpiceyPyError):
    pass


class SpiceUNKNOWNBFF(SpiceyPyError):
    pass


class SpiceUNKNOWNCKMETA(SpiceyPyError):
    pass


class SpiceUNKNOWNDATATYPE(SpiceyPyError):
    pass


class SpiceUNKNOWNFILARC(SpiceyPyError):
    pass


class SpiceUNKNOWNFRAMESPEC(SpiceyPyError):
    pass


class SpiceUNKNOWNFRAMETYPE(SpiceyPyError):
    pass


class SpiceUNKNOWNID(SpiceyPyError):
    pass


class SpiceUNKNOWNINCLUSION(SpiceyPyError):
    pass


class SpiceUNKNOWNINDEXTYPE(SpiceyPyError):
    pass


class SpiceUNKNOWNKERNELTYPE(SpiceyPyError):
    pass


class SpiceUNKNOWNKEY(SpiceyPyError):
    pass


class SpiceUNKNOWNMETAITEM(SpiceyPyError):
    pass


class SpiceUNKNOWNMODE(SpiceyPyError):
    pass


class SpiceUNKNOWNOP(SpiceyPyError):
    pass


class SpiceUNKNOWNPACKETDIR(SpiceyPyError):
    pass


class SpiceUNKNOWNPCKTYPE(SpiceyPyError):
    pass


class SpiceUNKNOWNREFDIR(SpiceyPyError):
    pass


class SpiceUNKNOWNTYPE(SpiceyPyError):
    pass


class SpiceUNKNOWNUNITS(SpiceyPyError):
    pass


class SpiceUNNATURALACT(SpiceyPyError):
    pass


class SpiceUNNATURALRELATION(SpiceyPyError):
    pass


class SpiceUNORDEREDREFS(SpiceyPyError):
    pass


class SpiceUNPARSEDQUERY(SpiceyPyError):
    pass


class SpiceUNRECOGNAPPFLAG(SpiceyPyError):
    pass


class SpiceUNRECOGNDATATYPE(SpiceyPyError):
    pass


class SpiceUNRECOGNDELIMITER(SpiceyPyError):
    pass


class SpiceUNRECOGNIZABLEFILE(SpiceyPyError):
    pass


class SpiceUNRECOGNIZEDACTION(SpiceyPyError):
    pass


class SpiceUNRECOGNIZEDFORMAT(SpiceyPyError):
    pass


class SpiceUNRECOGNIZEDFRAME(SpiceyPyError):
    pass


class SpiceUNRECOGNIZEDTYPE(SpiceyPyError):
    pass


class SpiceUNRECOGNPRECTYPE(SpiceyPyError):
    pass


class SpiceUNRESOLVEDNAMES(SpiceyPyError):
    pass


class SpiceUNRESOLVEDTIMES(SpiceyPyError):
    pass


class SpiceUNSUPPBINARYARCH(SpiceyPyError):
    pass


class SpiceUNSUPPORTEDARCH(SpiceyPyError):
    pass


class SpiceUNSUPPORTEDMETHOD(SpiceyPyError):
    pass


class SpiceUNSUPPTEXTFORMAT(SpiceyPyError):
    pass


class SpiceUNTITLEDHELP(SpiceyPyError):
    pass


class SpiceUPDATEPENDING(SpiceyPyError):
    pass


class SpiceUSAGEERROR(SpiceyPyError):
    pass


class SpiceUTFULL(SpiceyPyError):
    pass


class SpiceVALUETABLEFULL(SpiceyPyError):
    pass


class SpiceVARNAMETOOLONG(SpiceyPyError):
    pass


class SpiceVERSIONMISMATCH(SpiceyPyError):
    pass


class SpiceVERSIONMISMATCH1(SpiceyPyError):
    pass


class SpiceVERSIONMISMATCH2(SpiceyPyError):
    pass


class SpiceVERTEXNOTINGRID(SpiceyPyError):
    pass


class SpiceVOXELGRIDTOOBIG(SpiceyPyError):
    pass


class SpiceWIDTHTOOSMALL(SpiceyPyError):
    pass


class SpiceWINDOWSTOOSMALL(SpiceyPyError):
    pass


class SpiceWRITEERROR(SpiceyPyError):
    pass


class SpiceWRITEFAILED(SpiceyPyError):
    pass


class SpiceWRONGARCHITECTURE(SpiceyPyError):
    pass


class SpiceWRONGCKTYPE(SpiceyPyError):
    pass


class SpiceWRONGCONIC(SpiceyPyError):
    pass


class SpiceWRONGSEGMENT(SpiceyPyError):
    pass


class SpiceWRONGSPKTYPE(SpiceyPyError):
    pass


class SpiceYEAROUTOFBOUNDS(SpiceyPyError):
    pass


class SpiceZEROAXISLENGTH(SpiceyPyError):
    pass


class SpiceZEROBORESIGHT(SpiceyPyError):
    pass


class SpiceZEROFRAMEID(SpiceyPyError):
    pass


class SpiceZERORADIUS(SpiceyPyError):
    pass


class SpiceZEROSTEP(SpiceyPyError):
    pass


class SpiceZZHOLDDGETFAILED(SpiceyPyError):
    pass


class SpiceZZHOLDNOPUT(SpiceyPyError):
    pass


exceptions = {
    "SPICE(BADARCHTYPE)": SpiceBADARCHTYPE,
    "SPICE(BADATTRIBUTES)": SpiceBADATTRIBUTES,
    "SPICE(BADCOMMENTAREA)": SpiceBADCOMMENTAREA,
    "SPICE(BADCOORDSYSTEM)": SpiceBADCOORDSYSTEM,
    "SPICE(BADDASCOMMENTAREA)": SpiceBADDASCOMMENTAREA,
    "SPICE(BADFILETYPE)": SpiceBADFILETYPE,
    "SPICE(BADVARNAME)": SpiceBADVARNAME,
    "SPICE(BLANKFILENAME)": SpiceBLANKFILENAME,
    "SPICE(CKINSUFFDATA)": SpiceCKINSUFFDATA,
    "SPICE(COVERAGEGAP)": SpiceCOVERAGEGAP,
    "SPICE(DAFBEGGTEND)": SpiceDAFBEGGTEND,
    "SPICE(DAFFRNOTFOUND)": SpiceDAFFRNOTFOUND,
    "SPICE(DAFIMPROPOPEN)": SpiceDAFIMPROPOPEN,
    "SPICE(DAFNEGADDR)": SpiceDAFNEGADDR,
    "SPICE(DAFNOSEARCH)": SpiceDAFNOSEARCH,
    "SPICE(DAFOPENFAIL)": SpiceDAFOPENFAIL,
    "SPICE(DAFRWCONFLICT)": SpiceDAFRWCONFLICT,
    "SPICE(DASFILEREADFAILED)": SpiceDASFILEREADFAILED,
    "SPICE(DASIMPROPOPEN)": SpiceDASIMPROPOPEN,
    "SPICE(DASNOSUCHHANDLE)": SpiceDASNOSUCHHANDLE,
    "SPICE(DASOPENCONFLICT)": SpiceDASOPENCONFLICT,
    "SPICE(DASOPENFAIL)": SpiceDASOPENFAIL,
    "SPICE(DASRWCONFLICT)": SpiceDASRWCONFLICT,
    "SPICE(EKNOSEGMENTS)": SpiceEKNOSEGMENTS,
    "SPICE(FILECURRENTLYOPEN)": SpiceFILECURRENTLYOPEN,
    "SPICE(FILEDOESNOTEXIST)": SpiceFILEDOESNOTEXIST,
    "SPICE(FILEISNOTSPK)": SpiceFILEISNOTSPK,
    "SPICE(FILENOTFOUND)": SpiceFILENOTFOUND,
    "SPICE(FILEOPENFAILED)": SpiceFILEOPENFAILED,
    "SPICE(FILEREADFAILED)": SpiceFILEREADFAILED,
    "SPICE(INQUIREERROR)": SpiceINQUIREERROR,
    "SPICE(INQUIREFAILED)": SpiceINQUIREFAILED,
    "SPICE(INVALIDARCHTYPE)": SpiceINVALIDARCHTYPE,
    "SPICE(NOCURRENTARRAY)": SpiceNOCURRENTARRAY,
    "SPICE(NOLOADEDFILES)": SpiceNOLOADEDFILES,
    "SPICE(NOSEGMENTSFOUND)": SpiceNOSEGMENTSFOUND,
    "SPICE(NOSUCHFILE)": SpiceNOSUCHFILE,
    "SPICE(NOTADAFFILE)": SpiceNOTADAFFILE,
    "SPICE(NOTADASFILE)": SpiceNOTADASFILE,
    "SPICE(RECURSIVELOADING)": SpiceRECURSIVELOADING,
    "SPICE(SPKINSUFFDATA)": SpiceSPKINSUFFDATA,
    "SPICE(SPKINVALIDOPTION)": SpiceSPKINVALIDOPTION,
    "SPICE(SPKNOTASUBSET)": SpiceSPKNOTASUBSET,
    "SPICE(SPKTYPENOTSUPP)": SpiceSPKTYPENOTSUPP,
    "SPICE(TABLENOTLOADED)": SpiceTABLENOTLOADED,
    "SPICE(TOOMANYFILESOPEN)": SpiceTOOMANYFILESOPEN,
    "SPICE(UNKNOWNSPKTYPE)": SpiceUNKNOWNSPKTYPE,
    "SPICE(UNSUPPORTEDBFF)": SpiceUNSUPPORTEDBFF,
    "SPICE(UNSUPPORTEDSPEC)": SpiceUNSUPPORTEDSPEC,
    "SPICE(ARRAYTOOSMALL)": SpiceARRAYTOOSMALL,
    "SPICE(BADARRAYSIZE)": SpiceBADARRAYSIZE,
    "SPICE(BOUNDARYTOOBIG)": SpiceBOUNDARYTOOBIG,
    "SPICE(BUFFEROVERFLOW)": SpiceBUFFEROVERFLOW,
    "SPICE(CELLTOOSMALL)": SpiceCELLTOOSMALL,
    "SPICE(CKTOOMANYFILES)": SpiceCKTOOMANYFILES,
    "SPICE(COLUMNTOOSMALL)": SpiceCOLUMNTOOSMALL,
    "SPICE(COMMENTTOOLONG)": SpiceCOMMENTTOOLONG,
    "SPICE(DAFFTFULL)": SpiceDAFFTFULL,
    "SPICE(DASFTFULL)": SpiceDASFTFULL,
    "SPICE(DEVICENAMETOOLONG)": SpiceDEVICENAMETOOLONG,
    "SPICE(EKCOLATTRTABLEFULL)": SpiceEKCOLATTRTABLEFULL,
    "SPICE(EKCOLDESCTABLEFULL)": SpiceEKCOLDESCTABLEFULL,
    "SPICE(EKFILETABLEFULL)": SpiceEKFILETABLEFULL,
    "SPICE(EKIDTABLEFULL)": SpiceEKIDTABLEFULL,
    "SPICE(EKSEGMENTTABLEFULL)": SpiceEKSEGMENTTABLEFULL,
    "SPICE(GRIDTOOLARGE)": SpiceGRIDTOOLARGE,
    "SPICE(INSUFFLEN)": SpiceINSUFFLEN,
    "SPICE(KERNELPOOLFULL)": SpiceKERNELPOOLFULL,
    "SPICE(MALLOCFAILED)": SpiceMALLOCFAILED,
    "SPICE(MALLOCFAILURE)": SpiceMALLOCFAILURE,
    "SPICE(MEMALLOCFAILED)": SpiceMEMALLOCFAILED,
    "SPICE(MESSAGETOOLONG)": SpiceMESSAGETOOLONG,
    "SPICE(NOMOREROOM)": SpiceNOMOREROOM,
    "SPICE(OUTOFROOM)": SpiceOUTOFROOM,
    "SPICE(PCKFILETABLEFULL)": SpicePCKFILETABLEFULL,
    "SPICE(SETEXCESS)": SpiceSETEXCESS,
    "SPICE(SPKFILETABLEFULL)": SpiceSPKFILETABLEFULL,
    "SPICE(TRACEBACKOVERFLOW)": SpiceTRACEBACKOVERFLOW,
    "SPICE(WINDOWEXCESS)": SpiceWINDOWEXCESS,
    "SPICE(WORKSPACETOOSMALL)": SpiceWORKSPACETOOSMALL,
    "SPICE(BADVARIABLETYPE)": SpiceBADVARIABLETYPE,
    "SPICE(INVALIDTYPE)": SpiceINVALIDTYPE,
    "SPICE(INVALIDARRAYTYPE)": SpiceINVALIDARRAYTYPE,
    "SPICE(NOTASET)": SpiceNOTASET,
    "SPICE(TYPEMISMATCH)": SpiceTYPEMISMATCH,
    "SPICE(WRONGDATATYPE)": SpiceWRONGDATATYPE,
    "SPICE(BODYIDNOTFOUND)": SpiceBODYIDNOTFOUND,
    "SPICE(BODYNAMENOTFOUND)": SpiceBODYNAMENOTFOUND,
    "SPICE(CANTFINDFRAME)": SpiceCANTFINDFRAME,
    "SPICE(FRAMEIDNOTFOUND)": SpiceFRAMEIDNOTFOUND,
    "SPICE(FRAMENAMENOTFOUND)": SpiceFRAMENAMENOTFOUND,
    "SPICE(IDCODENOTFOUND)": SpiceIDCODENOTFOUND,
    "SPICE(KERNELVARNOTFOUND)": SpiceKERNELVARNOTFOUND,
    "SPICE(NOTRANSLATION)": SpiceNOTRANSLATION,
    "SPICE(UNKNOWNFRAME)": SpiceUNKNOWNFRAME,
    "SPICE(VARIABLENOTFOUND)": SpiceVARIABLENOTFOUND,
    "SPICE(BADVERTEXINDEX)": SpiceBADVERTEXINDEX,
    "SPICE(INDEXOUTOFRANGE)": SpiceINDEXOUTOFRANGE,
    "SPICE(INVALDINDEX)": SpiceINVALDINDEX,
    "SPICE(INVALIDINDEX)": SpiceINVALIDINDEX,
    "SPICE(DIVIDEBYZERO)": SpiceDIVIDEBYZERO,
    "SPICE(BADINITSTATE)": SpiceBADINITSTATE,
    "SPICE(BUG)": SpiceBUG,
    "SPICE(IMMUTABLEVALUE)": SpiceIMMUTABLEVALUE,
    "SPICE(INVALIDSIGNAL)": SpiceINVALIDSIGNAL,
    "SPICE(NOTINITIALIZED)": SpiceNOTINITIALIZED,
    "SPICE(SIGNALFAILED)": SpiceSIGNALFAILED,
    "SPICE(SIGNALFAILURE)": SpiceSIGNALFAILURE,
    "SPICE(TRACESTACKEMPTY)": SpiceTRACESTACKEMPTY,
    "SPICE(ARRAYSHAPEMISMATCH)": SpiceARRAYSHAPEMISMATCH,
    "SPICE(BADACTION)": SpiceBADACTION,
    "SPICE(BADAXISLENGTH)": SpiceBADAXISLENGTH,
    "SPICE(BADAXISNUMBERS)": SpiceBADAXISNUMBERS,
    "SPICE(BADBORESIGHTSPEC)": SpiceBADBORESIGHTSPEC,
    "SPICE(BADBOUNDARY)": SpiceBADBOUNDARY,
    "SPICE(BADCOARSEVOXSCALE)": SpiceBADCOARSEVOXSCALE,
    "SPICE(BADDEFAULTVALUE)": SpiceBADDEFAULTVALUE,
    "SPICE(BADDESCRTIMES)": SpiceBADDESCRTIMES,
    "SPICE(BADDIRECTION)": SpiceBADDIRECTION,
    "SPICE(BADECCENTRICITY)": SpiceBADECCENTRICITY,
    "SPICE(BADENDPOINTS)": SpiceBADENDPOINTS,
    "SPICE(BADFINEVOXELSCALE)": SpiceBADFINEVOXELSCALE,
    "SPICE(BADFRAME)": SpiceBADFRAME,
    "SPICE(BADFRAMECLASS)": SpiceBADFRAMECLASS,
    "SPICE(BADGM)": SpiceBADGM,
    "SPICE(BADINDEX)": SpiceBADINDEX,
    "SPICE(BADLATUSRECTUM)": SpiceBADLATUSRECTUM,
    "SPICE(BADLIMBLOCUSMIX)": SpiceBADLIMBLOCUSMIX,
    "SPICE(BADPARTNUMBER)": SpiceBADPARTNUMBER,
    "SPICE(BADPERIAPSEVALUE)": SpiceBADPERIAPSEVALUE,
    "SPICE(BADPLATECOUNT)": SpiceBADPLATECOUNT,
    "SPICE(BADRADIUS)": SpiceBADRADIUS,
    "SPICE(BADRADIUSCOUNT)": SpiceBADRADIUSCOUNT,
    "SPICE(BADREFVECTORSPEC)": SpiceBADREFVECTORSPEC,
    "SPICE(BADSEMIAXIS)": SpiceBADSEMIAXIS,
    "SPICE(BADSTOPTIME)": SpiceBADSTOPTIME,
    "SPICE(BADTIMEITEM)": SpiceBADTIMEITEM,
    "SPICE(BADTIMESTRING)": SpiceBADTIMESTRING,
    "SPICE(BADTIMETYPE)": SpiceBADTIMETYPE,
    "SPICE(BADVARIABLESIZE)": SpiceBADVARIABLESIZE,
    "SPICE(BADVECTOR)": SpiceBADVECTOR,
    "SPICE(BADVERTEXCOUNT)": SpiceBADVERTEXCOUNT,
    "SPICE(BARYCENTEREPHEM)": SpiceBARYCENTEREPHEM,
    "SPICE(BLANKMODULENAME)": SpiceBLANKMODULENAME,
    "SPICE(BODIESNOTDISTINCT)": SpiceBODIESNOTDISTINCT,
    "SPICE(BODYANDCENTERSAME)": SpiceBODYANDCENTERSAME,
    "SPICE(BORESIGHTMISSING)": SpiceBORESIGHTMISSING,
    "SPICE(BOUNDARYMISSING)": SpiceBOUNDARYMISSING,
    "SPICE(BOUNDSOUTOFORDER)": SpiceBOUNDSOUTOFORDER,
    "SPICE(COORDSYSNOTREC)": SpiceCOORDSYSNOTREC,
    "SPICE(CROSSANGLEMISSING)": SpiceCROSSANGLEMISSING,
    "SPICE(DEGENERATECASE)": SpiceDEGENERATECASE,
    "SPICE(DEGENERATEINTERVAL)": SpiceDEGENERATEINTERVAL,
    "SPICE(DEGENERATESURFACE)": SpiceDEGENERATESURFACE,
    "SPICE(DEGREEOUTOFRANGE)": SpiceDEGREEOUTOFRANGE,
    "SPICE(DEPENDENTVECTORS)": SpiceDEPENDENTVECTORS,
    "SPICE(NONCONTIGUOUSARRAY)": SpiceNONCONTIGUOUSARRAY,
    "SPICE(DSKTARGETMISMATCH)": SpiceDSKTARGETMISMATCH,
    "SPICE(DTOUTOFRANGE)": SpiceDTOUTOFRANGE,
    "SPICE(DUBIOUSMETHOD)": SpiceDUBIOUSMETHOD,
    "SPICE(ECCOUTOFRANGE)": SpiceECCOUTOFRANGE,
    "SPICE(ELEMENTSTOOSHORT)": SpiceELEMENTSTOOSHORT,
    "SPICE(EMPTYSEGMENT)": SpiceEMPTYSEGMENT,
    "SPICE(EMPTYSTRING)": SpiceEMPTYSTRING,
    "SPICE(FRAMEMISSING)": SpiceFRAMEMISSING,
    "SPICE(ILLEGALCHARACTER)": SpiceILLEGALCHARACTER,
    "SPICE(INCOMPATIBLESCALE)": SpiceINCOMPATIBLESCALE,
    "SPICE(INCOMPATIBLEUNITS)": SpiceINCOMPATIBLEUNITS,
    "SPICE(INPUTOUTOFRANGE)": SpiceINPUTOUTOFRANGE,
    "SPICE(INPUTSTOOLARGE)": SpiceINPUTSTOOLARGE,
    "SPICE(INSUFFICIENTANGLES)": SpiceINSUFFICIENTANGLES,
    "SPICE(INTINDEXTOOSMALL)": SpiceINTINDEXTOOSMALL,
    "SPICE(INTLENNOTPOS)": SpiceINTLENNOTPOS,
    "SPICE(INTOUTOFRANGE)": SpiceINTOUTOFRANGE,
    "SPICE(INVALIDACTION)": SpiceINVALIDACTION,
    "SPICE(INVALIDARGUMENT)": SpiceINVALIDARGUMENT,
    "SPICE(INVALIDARRAYRANK)": SpiceINVALIDARRAYRANK,
    "SPICE(INVALIDARRAYSHAPE)": SpiceINVALIDARRAYSHAPE,
    "SPICE(INVALIDAXISLENGTH)": SpiceINVALIDAXISLENGTH,
    "SPICE(INVALIDCARDINALITY)": SpiceINVALIDCARDINALITY,
    "SPICE(INVALIDCOUNT)": SpiceINVALIDCOUNT,
    "SPICE(INVALIDDEGREE)": SpiceINVALIDDEGREE,
    "SPICE(INVALIDDESCRTIME)": SpiceINVALIDDESCRTIME,
    "SPICE(INVALIDDIMENSION)": SpiceINVALIDDIMENSION,
    "SPICE(INVALIDELLIPSE)": SpiceINVALIDELLIPSE,
    "SPICE(INVALIDENDPNTSPEC)": SpiceINVALIDENDPNTSPEC,
    "SPICE(INVALIDEPOCH)": SpiceINVALIDEPOCH,
    "SPICE(INVALIDFORMAT)": SpiceINVALIDFORMAT,
    "SPICE(INVALIDFRAME)": SpiceINVALIDFRAME,
    "SPICE(INVALIDFRAMEDEF)": SpiceINVALIDFRAMEDEF,
    "SPICE(INVALIDLIMBTYPE)": SpiceINVALIDLIMBTYPE,
    "SPICE(INVALIDLISTITEM)": SpiceINVALIDLISTITEM,
    "SPICE(INVALIDLOCUS)": SpiceINVALIDLOCUS,
    "SPICE(INVALIDLONEXTENT)": SpiceINVALIDLONEXTENT,
    "SPICE(INVALIDMETHOD)": SpiceINVALIDMETHOD,
    "SPICE(INVALIDMSGTYPE)": SpiceINVALIDMSGTYPE,
    "SPICE(INVALIDNUMINTS)": SpiceINVALIDNUMINTS,
    "SPICE(INVALIDNUMRECS)": SpiceINVALIDNUMRECS,
    "SPICE(INVALIDOCCTYPE)": SpiceINVALIDOCCTYPE,
    "SPICE(INVALIDOPERATION)": SpiceINVALIDOPERATION,
    "SPICE(INVALIDOPTION)": SpiceINVALIDOPTION,
    "SPICE(INVALIDPLANE)": SpiceINVALIDPLANE,
    "SPICE(INVALIDPOINT)": SpiceINVALIDPOINT,
    "SPICE(INVALIDRADIUS)": SpiceINVALIDRADIUS,
    "SPICE(INVALIDREFFRAME)": SpiceINVALIDREFFRAME,
    "SPICE(INVALIDROLLSTEP)": SpiceINVALIDROLLSTEP,
    "SPICE(INVALIDSCLKSTRING)": SpiceINVALIDSCLKSTRING,
    "SPICE(INVALIDSCLKTIME)": SpiceINVALIDSCLKTIME,
    "SPICE(INVALIDSEARCHSTEP)": SpiceINVALIDSEARCHSTEP,
    "SPICE(INVALIDSIZE)": SpiceINVALIDSIZE,
    "SPICE(INVALIDSTARTTIME)": SpiceINVALIDSTARTTIME,
    "SPICE(INVALIDSTATE)": SpiceINVALIDSTATE,
    "SPICE(INVALIDSTEP)": SpiceINVALIDSTEP,
    "SPICE(INVALIDSTEPSIZE)": SpiceINVALIDSTEPSIZE,
    "SPICE(INVALIDSUBTYPE)": SpiceINVALIDSUBTYPE,
    "SPICE(INVALIDTARGET)": SpiceINVALIDTARGET,
    "SPICE(INVALIDTERMTYPE)": SpiceINVALIDTERMTYPE,
    "SPICE(INVALIDTIMEFORMAT)": SpiceINVALIDTIMEFORMAT,
    "SPICE(INVALIDTIMESTRING)": SpiceINVALIDTIMESTRING,
    "SPICE(INVALIDTOL)": SpiceINVALIDTOL,
    "SPICE(INVALIDTOLERANCE)": SpiceINVALIDTOLERANCE,
    "SPICE(INVALIDVALUE)": SpiceINVALIDVALUE,
    "SPICE(INVALIDVERTEX)": SpiceINVALIDVERTEX,
    "SPICE(MISSINGDATA)": SpiceMISSINGDATA,
    "SPICE(MISSINGTIMEINFO)": SpiceMISSINGTIMEINFO,
    "SPICE(MISSINGVALUE)": SpiceMISSINGVALUE,
    "SPICE(NAMESDONOTMATCH)": SpiceNAMESDONOTMATCH,
    "SPICE(NOCLASS)": SpiceNOCLASS,
    "SPICE(NOCOLUMN)": SpiceNOCOLUMN,
    "SPICE(NOFRAME)": SpiceNOFRAME,
    "SPICE(NOFRAMEINFO)": SpiceNOFRAMEINFO,
    "SPICE(NOINTERCEPT)": SpiceNOINTERCEPT,
    "SPICE(NOINTERVAL)": SpiceNOINTERVAL,
    "SPICE(NONCONICMOTION)": SpiceNONCONICMOTION,
    "SPICE(NONPOSITIVEMASS)": SpiceNONPOSITIVEMASS,
    "SPICE(NONPOSITIVESCALE)": SpiceNONPOSITIVESCALE,
    "SPICE(NONPRINTABLECHARS)": SpiceNONPRINTABLECHARS,
    "SPICE(NOPARTITION)": SpiceNOPARTITION,
    "SPICE(NOPATHVALUE)": SpiceNOPATHVALUE,
    "SPICE(NOPRIORITIZATION)": SpiceNOPRIORITIZATION,
    "SPICE(NOSEPARATION)": SpiceNOSEPARATION,
    "SPICE(NOTADPNUMBER)": SpiceNOTADPNUMBER,
    "SPICE(NOTANINTEGER)": SpiceNOTANINTEGER,
    "SPICE(NOTAROTATION)": SpiceNOTAROTATION,
    "SPICE(NOTINPART)": SpiceNOTINPART,
    "SPICE(NOTPRINTABLECHARS)": SpiceNOTPRINTABLECHARS,
    "SPICE(NOTRECOGNIZED)": SpiceNOTRECOGNIZED,
    "SPICE(NOTSUPPORTED)": SpiceNOTSUPPORTED,
    "SPICE(NULLPOINTER)": SpiceNULLPOINTER,
    "SPICE(NUMCOEFFSNOTPOS)": SpiceNUMCOEFFSNOTPOS,
    "SPICE(NUMERICOVERFLOW)": SpiceNUMERICOVERFLOW,
    "SPICE(NUMPARTSUNEQUAL)": SpiceNUMPARTSUNEQUAL,
    "SPICE(NUMSTATESNOTPOS)": SpiceNUMSTATESNOTPOS,
    "SPICE(PLATELISTTOOSMALL)": SpicePLATELISTTOOSMALL,
    "SPICE(POINTNOTONSURFACE)": SpicePOINTNOTONSURFACE,
    "SPICE(POINTONZAXIS)": SpicePOINTONZAXIS,
    "SPICE(PTRARRAYTOOSMALL)": SpicePTRARRAYTOOSMALL,
    "SPICE(REFANGLEMISSING)": SpiceREFANGLEMISSING,
    "SPICE(REFVECTORMISSING)": SpiceREFVECTORMISSING,
    "SPICE(SCLKTRUNCATED)": SpiceSCLKTRUNCATED,
    "SPICE(SEGIDTOOLONG)": SpiceSEGIDTOOLONG,
    "SPICE(SHAPEMISSING)": SpiceSHAPEMISSING,
    "SPICE(SHAPENOTSUPPORTED)": SpiceSHAPENOTSUPPORTED,
    "SPICE(SINGULARMATRIX)": SpiceSINGULARMATRIX,
    "SPICE(STRINGTOOLSHORT)": SpiceSTRINGTOOLSHORT,
    "SPICE(STRINGTOOSHORT)": SpiceSTRINGTOOSHORT,
    "SPICE(SUBPOINTNOTFOUND)": SpiceSUBPOINTNOTFOUND,
    "SPICE(TARGETMISMATCH)": SpiceTARGETMISMATCH,
    "SPICE(TIMECONFLICT)": SpiceTIMECONFLICT,
    "SPICE(TIMESDONTMATCH)": SpiceTIMESDONTMATCH,
    "SPICE(TIMESOUTOFORDER)": SpiceTIMESOUTOFORDER,
    "SPICE(TOOFEWPACKETS)": SpiceTOOFEWPACKETS,
    "SPICE(TOOFEWPLATES)": SpiceTOOFEWPLATES,
    "SPICE(TOOFEWSTATES)": SpiceTOOFEWSTATES,
    "SPICE(TOOFEWVERTICES)": SpiceTOOFEWVERTICES,
    "SPICE(TOOMANYPARTS)": SpiceTOOMANYPARTS,
    "SPICE(UNDEFINEDFRAME)": SpiceUNDEFINEDFRAME,
    "SPICE(UNITSMISSING)": SpiceUNITSMISSING,
    "SPICE(UNITSNOTREC)": SpiceUNITSNOTREC,
    "SPICE(UNKNOWNCOMPARE)": SpiceUNKNOWNCOMPARE,
    "SPICE(UNKNOWNSYSTEM)": SpiceUNKNOWNSYSTEM,
    "SPICE(UNMATCHENDPTS)": SpiceUNMATCHENDPTS,
    "SPICE(UNORDEREDTIMES)": SpiceUNORDEREDTIMES,
    "SPICE(UNPARSEDTIME)": SpiceUNPARSEDTIME,
    "SPICE(VALUEOUTOFRANGE)": SpiceVALUEOUTOFRANGE,
    "SPICE(VECTORTOOBIG)": SpiceVECTORTOOBIG,
    "SPICE(WINDOWTOOSMALL)": SpiceWINDOWTOOSMALL,
    "SPICE(YEAROUTOFRANGE)": SpiceYEAROUTOFRANGE,
    "SPICE(ZEROBOUNDSEXTENT)": SpiceZEROBOUNDSEXTENT,
    "SPICE(ZEROLENGTHCOLUMN)": SpiceZEROLENGTHCOLUMN,
    "SPICE(ZEROPOSITION)": SpiceZEROPOSITION,
    "SPICE(ZEROQUATERNION)": SpiceZEROQUATERNION,
    "SPICE(ZEROVECTOR)": SpiceZEROVECTOR,
    "SPICE(ZEROVELOCITY)": SpiceZEROVELOCITY,
    "SPICE(1NODATAFORBODY)":Spice1NODATAFORBODY,
    "SPICE(ADDRESSOUTOFBOUNDS)": SpiceADDRESSOUTOFBOUNDS,
    "SPICE(AGENTLISTOVERFLOW)": SpiceAGENTLISTOVERFLOW,
    "SPICE(ALLGONE)": SpiceALLGONE,
    "SPICE(AMBIGTEMPL)": SpiceAMBIGTEMPL,
    "SPICE(ARRAYSIZEMISMATCH)": SpiceARRAYSIZEMISMATCH,
    "SPICE(AVALOUTOFRANGE)": SpiceAVALOUTOFRANGE,
    "SPICE(AXISUNDERFLOW)": SpiceAXISUNDERFLOW,
    "SPICE(BADADDRESS)": SpiceBADADDRESS,
    "SPICE(BADANGLE)": SpiceBADANGLE,
    "SPICE(BADANGLEUNITS)": SpiceBADANGLEUNITS,
    "SPICE(BADANGRATEERROR)": SpiceBADANGRATEERROR,
    "SPICE(BADANGULARRATE)": SpiceBADANGULARRATE,
    "SPICE(BADANGULARRATEFLAG)": SpiceBADANGULARRATEFLAG,
    "SPICE(BADARCHITECTURE)": SpiceBADARCHITECTURE,
    "SPICE(BADATTIME)": SpiceBADATTIME,
    "SPICE(BADATTRIBUTE)": SpiceBADATTRIBUTE,
    "SPICE(BADAUVALUE)": SpiceBADAUVALUE,
    "SPICE(BADAVFLAG)": SpiceBADAVFLAG,
    "SPICE(BADAVFRAMEFLAG)": SpiceBADAVFRAMEFLAG,
    "SPICE(BADAXIS)": SpiceBADAXIS,
    "SPICE(BADBLOCKSIZE)": SpiceBADBLOCKSIZE,
    "SPICE(BADBODY1SPEC)":SpiceBADBODY1SPEC,
    "SPICE(BADBODY2SPEC)":SpiceBADBODY2SPEC,
    "SPICE(BADBODYID)": SpiceBADBODYID,
    "SPICE(BADBODYID1)":SpiceBADBODYID1,
    "SPICE(BADBODYID2)":SpiceBADBODYID2,
    "SPICE(BADCATALOGFILE)": SpiceBADCATALOGFILE,
    "SPICE(BADCENTER1SPEC)":SpiceBADCENTER1SPEC,
    "SPICE(BADCENTER2SPEC)":SpiceBADCENTER2SPEC,
    "SPICE(BADCENTERNAME)": SpiceBADCENTERNAME,
    "SPICE(BADCHECKFLAG)": SpiceBADCHECKFLAG,
    "SPICE(BADCK1SEGMENT)":SpiceBADCK1SEGMENT,
    "SPICE(BADCK3SEGMENT)":SpiceBADCK3SEGMENT,
    "SPICE(BADCKTYPESPEC)": SpiceBADCKTYPESPEC,
    "SPICE(BADCOLUMDECL)": SpiceBADCOLUMDECL,
    "SPICE(BADCOLUMNCOUNT)": SpiceBADCOLUMNCOUNT,
    "SPICE(BADCOLUMNDECL)": SpiceBADCOLUMNDECL,
    "SPICE(BADCOMPNUMBER)": SpiceBADCOMPNUMBER,
    "SPICE(BADCOORDBOUNDS)": SpiceBADCOORDBOUNDS,
    "SPICE(BADCOORDSYS)": SpiceBADCOORDSYS,
    "SPICE(BADCOVFRAME1SPEC1)":SpiceBADCOVFRAME1SPEC1,
    "SPICE(BADCOVFRAME1SPEC2)":SpiceBADCOVFRAME1SPEC2,
    "SPICE(BADCOVFRAME1SPEC4)":SpiceBADCOVFRAME1SPEC4,
    "SPICE(BADCOVFRAME1SPEC5)":SpiceBADCOVFRAME1SPEC5,
    "SPICE(BADCOVFRAME1SPEC6)":SpiceBADCOVFRAME1SPEC6,
    "SPICE(BADCOVFRAME2SPEC1)":SpiceBADCOVFRAME2SPEC1,
    "SPICE(BADCOVFRAME2SPEC2)":SpiceBADCOVFRAME2SPEC2,
    "SPICE(BADCOVFRAME2SPEC4)":SpiceBADCOVFRAME2SPEC4,
    "SPICE(BADCOVFRAME2SPEC5)":SpiceBADCOVFRAME2SPEC5,
    "SPICE(BADCOVFRAME2SPEC6)":SpiceBADCOVFRAME2SPEC6,
    "SPICE(BADCURVETYPE)": SpiceBADCURVETYPE,
    "SPICE(BADDAFTRANSFERFILE)": SpiceBADDAFTRANSFERFILE,
    "SPICE(BADDASDIRECTORY)": SpiceBADDASDIRECTORY,
    "SPICE(BADDASFILE)": SpiceBADDASFILE,
    "SPICE(BADDASTRANSFERFILE)": SpiceBADDASTRANSFERFILE,
    "SPICE(BADDATALINE)": SpiceBADDATALINE,
    "SPICE(BADDATAORDERTOKEN)": SpiceBADDATAORDERTOKEN,
    "SPICE(BADDATATYPE)": SpiceBADDATATYPE,
    "SPICE(BADDATATYPEFLAG)": SpiceBADDATATYPEFLAG,
    "SPICE(BADDECIMALSCLK1)":SpiceBADDECIMALSCLK1,
    "SPICE(BADDECIMALSCLK2)":SpiceBADDECIMALSCLK2,
    "SPICE(BADDIMENSION)": SpiceBADDIMENSION,
    "SPICE(BADDIMENSIONS)": SpiceBADDIMENSIONS,
    "SPICE(BADDOUBLEPRECISION)": SpiceBADDOUBLEPRECISION,
    "SPICE(BADDOWNSAMPLINGTOL)": SpiceBADDOWNSAMPLINGTOL,
    "SPICE(BADDPSCLK1)":SpiceBADDPSCLK1,
    "SPICE(BADDPSCLK2)":SpiceBADDPSCLK2,
    "SPICE(BADET1)":SpiceBADET1,
    "SPICE(BADET2)":SpiceBADET2,
    "SPICE(BADEULERANGLEUNITS)": SpiceBADEULERANGLEUNITS,
    "SPICE(BADFILEFORMAT)": SpiceBADFILEFORMAT,
    "SPICE(BADFILENAME)": SpiceBADFILENAME,
    "SPICE(BADFORMATSPECIFIER)": SpiceBADFORMATSPECIFIER,
    "SPICE(BADFORMATSTRING)": SpiceBADFORMATSTRING,
    "SPICE(BADFRAME1NAME)":SpiceBADFRAME1NAME,
    "SPICE(BADFRAME2NAME)":SpiceBADFRAME2NAME,
    "SPICE(BADFRAMECOUNT)": SpiceBADFRAMECOUNT,
    "SPICE(BADFRAMESPEC)": SpiceBADFRAMESPEC,
    "SPICE(BADFRAMESPEC2)":SpiceBADFRAMESPEC2,
    "SPICE(BADFROMFRAME1SP1)":SpiceBADFROMFRAME1SP1,
    "SPICE(BADFROMFRAME1SP2)":SpiceBADFROMFRAME1SP2,
    "SPICE(BADFROMFRAME2SP1)":SpiceBADFROMFRAME2SP1,
    "SPICE(BADFROMFRAME2SP2)":SpiceBADFROMFRAME2SP2,
    "SPICE(BADFROMTIME)": SpiceBADFROMTIME,
    "SPICE(BADFROMTIMESYSTEM)": SpiceBADFROMTIMESYSTEM,
    "SPICE(BADFROMTIMETYPE)": SpiceBADFROMTIMETYPE,
    "SPICE(BADGEFVERSION)": SpiceBADGEFVERSION,
    "SPICE(BADGEOMETRY)": SpiceBADGEOMETRY,
    "SPICE(BADHARDSPACE)": SpiceBADHARDSPACE,
    "SPICE(BADHERMITDEGREE)": SpiceBADHERMITDEGREE,
    "SPICE(BADINPUTDATALINE)": SpiceBADINPUTDATALINE,
    "SPICE(BADINPUTETTIME)": SpiceBADINPUTETTIME,
    "SPICE(BADINPUTTYPE)": SpiceBADINPUTTYPE,
    "SPICE(BADINPUTUTCTIME)": SpiceBADINPUTUTCTIME,
    "SPICE(BADINSTRUMENTID)": SpiceBADINSTRUMENTID,
    "SPICE(BADINTEGER)": SpiceBADINTEGER,
    "SPICE(BADKERNELTYPE)": SpiceBADKERNELTYPE,
    "SPICE(BADKERNELVARTYPE)": SpiceBADKERNELVARTYPE,
    "SPICE(BADLAGRANGEDEGREE)": SpiceBADLAGRANGEDEGREE,
    "SPICE(BADLATITUDEBOUNDS)": SpiceBADLATITUDEBOUNDS,
    "SPICE(BADLATITUDERANGE)": SpiceBADLATITUDERANGE,
    "SPICE(BADLEAPSECONDS)": SpiceBADLEAPSECONDS,
    "SPICE(BADLINEPERRECCOUNT)": SpiceBADLINEPERRECCOUNT,
    "SPICE(BADLISTFILENAME)": SpiceBADLISTFILENAME,
    "SPICE(BADLONGITUDERANGE)": SpiceBADLONGITUDERANGE,
    "SPICE(BADMATRIX)": SpiceBADMATRIX,
    "SPICE(BADMEANMOTION)": SpiceBADMEANMOTION,
    "SPICE(BADMECCENTRICITY)": SpiceBADMECCENTRICITY,
    "SPICE(BADMETHODSYNTAX)": SpiceBADMETHODSYNTAX,
    "SPICE(BADMIDNIGHTTYPE)": SpiceBADMIDNIGHTTYPE,
    "SPICE(BADMSEMIMAJOR)": SpiceBADMSEMIMAJOR,
    "SPICE(BADMSOPQUATERNION)": SpiceBADMSOPQUATERNION,
    "SPICE(BADNOFDIGITS)": SpiceBADNOFDIGITS,
    "SPICE(BADNOFSTATES)": SpiceBADNOFSTATES,
    "SPICE(BADNUMBEROFPOINTS)": SpiceBADNUMBEROFPOINTS,
    "SPICE(BADOBJECTID)": SpiceBADOBJECTID,
    "SPICE(BADOBJECTNAME)": SpiceBADOBJECTNAME,
    "SPICE(BADOFFSETANGLES)": SpiceBADOFFSETANGLES,
    "SPICE(BADOFFSETANGUNITS)": SpiceBADOFFSETANGUNITS,
    "SPICE(BADOFFSETAXESFORMAT)": SpiceBADOFFSETAXESFORMAT,
    "SPICE(BADOFFSETAXIS123)":SpiceBADOFFSETAXIS123,
    "SPICE(BADOFFSETAXISXYZ)": SpiceBADOFFSETAXISXYZ,
    "SPICE(BADOPTIONNAME)": SpiceBADOPTIONNAME,
    "SPICE(BADORBITALPERIOD)": SpiceBADORBITALPERIOD,
    "SPICE(BADOUTPUTSPKTYPE)": SpiceBADOUTPUTSPKTYPE,
    "SPICE(BADOUTPUTTYPE)": SpiceBADOUTPUTTYPE,
    "SPICE(BADPCKVALUE)": SpiceBADPCKVALUE,
    "SPICE(BADPECCENTRICITY)": SpiceBADPECCENTRICITY,
    "SPICE(BADPICTURE)": SpiceBADPICTURE,
    "SPICE(BADPODLOCATION)": SpiceBADPODLOCATION,
    "SPICE(BADPRECVALUE)": SpiceBADPRECVALUE,
    "SPICE(BADPRIORITYSPEC)": SpiceBADPRIORITYSPEC,
    "SPICE(BADQUATSIGN)": SpiceBADQUATSIGN,
    "SPICE(BADQUATTHRESHOLD)": SpiceBADQUATTHRESHOLD,
    "SPICE(BADRATEFRAMEFLAG)": SpiceBADRATEFRAMEFLAG,
    "SPICE(BADRATETHRESHOLD)": SpiceBADRATETHRESHOLD,
    "SPICE(BADRECORDCOUNT)": SpiceBADRECORDCOUNT,
    "SPICE(BADROTATIONAXIS123)":SpiceBADROTATIONAXIS123,
    "SPICE(BADROTATIONAXISXYZ)": SpiceBADROTATIONAXISXYZ,
    "SPICE(BADROTATIONORDER1)":SpiceBADROTATIONORDER1,
    "SPICE(BADROTATIONORDER2)":SpiceBADROTATIONORDER2,
    "SPICE(BADROTATIONORDER3)":SpiceBADROTATIONORDER3,
    "SPICE(BADROTATIONSORDER)": SpiceBADROTATIONSORDER,
    "SPICE(BADROTATIONTYPE)": SpiceBADROTATIONTYPE,
    "SPICE(BADROTAXESFORMAT)": SpiceBADROTAXESFORMAT,
    "SPICE(BADROWCOUNT)": SpiceBADROWCOUNT,
    "SPICE(BADSCID)": SpiceBADSCID,
    "SPICE(BADSCLKDATA1)":SpiceBADSCLKDATA1,
    "SPICE(BADSCLKDATA2)":SpiceBADSCLKDATA2,
    "SPICE(BADSCLKDATA3)":SpiceBADSCLKDATA3,
    "SPICE(BADSEMILATUS)": SpiceBADSEMILATUS,
    "SPICE(BADSHAPE)": SpiceBADSHAPE,
    "SPICE(BADSOLDAY)": SpiceBADSOLDAY,
    "SPICE(BADSOLINDEX)": SpiceBADSOLINDEX,
    "SPICE(BADSOLTIME)": SpiceBADSOLTIME,
    "SPICE(BADSOURCERADIUS)": SpiceBADSOURCERADIUS,
    "SPICE(BADSPICEQUATERNION)": SpiceBADSPICEQUATERNION,
    "SPICE(BADSTARINDEX)": SpiceBADSTARINDEX,
    "SPICE(BADSTARTTIME)": SpiceBADSTARTTIME,
    "SPICE(BADSTDIONAME)": SpiceBADSTDIONAME,
    "SPICE(BADSUBSCRIPT)": SpiceBADSUBSCRIPT,
    "SPICE(BADSUBSTR)": SpiceBADSUBSTR,
    "SPICE(BADSUBSTRINGBOUNDS)": SpiceBADSUBSTRINGBOUNDS,
    "SPICE(BADSURFACEMAP)": SpiceBADSURFACEMAP,
    "SPICE(BADTABLEFLAG)": SpiceBADTABLEFLAG,
    "SPICE(BADTERMLOCUSMIX)": SpiceBADTERMLOCUSMIX,
    "SPICE(BADTIMEBOUNDS)": SpiceBADTIMEBOUNDS,
    "SPICE(BADTIMECASE)": SpiceBADTIMECASE,
    "SPICE(BADTIMECOUNT)": SpiceBADTIMECOUNT,
    "SPICE(BADTIMEFORMAT)": SpiceBADTIMEFORMAT,
    "SPICE(BADTIMEOFFSET)": SpiceBADTIMEOFFSET,
    "SPICE(BADTIMESPEC)": SpiceBADTIMESPEC,
    "SPICE(BADTIMETYPEFLAG)": SpiceBADTIMETYPEFLAG,
    "SPICE(BADTLE)": SpiceBADTLE,
    "SPICE(BADTLECOVERAGEPAD)": SpiceBADTLECOVERAGEPAD,
    "SPICE(BADTLECOVERAGEPAD2)":SpiceBADTLECOVERAGEPAD2,
    "SPICE(BADTLECOVERAGEPAD3)":SpiceBADTLECOVERAGEPAD3,
    "SPICE(BADTLEPADS)": SpiceBADTLEPADS,
    "SPICE(BADTOFRAME1SPEC1)":SpiceBADTOFRAME1SPEC1,
    "SPICE(BADTOFRAME1SPEC2)":SpiceBADTOFRAME1SPEC2,
    "SPICE(BADTOFRAME2SPEC1)":SpiceBADTOFRAME2SPEC1,
    "SPICE(BADTOFRAME2SPEC2)":SpiceBADTOFRAME2SPEC2,
    "SPICE(BADTOTIME)": SpiceBADTOTIME,
    "SPICE(BADTOTIMESYSTEM)": SpiceBADTOTIMESYSTEM,
    "SPICE(BADTOTIMETYPE)": SpiceBADTOTIMETYPE,
    "SPICE(BADTYPESHAPECOMBO)": SpiceBADTYPESHAPECOMBO,
    "SPICE(BADUNITS)": SpiceBADUNITS,
    "SPICE(BADVARASSIGN)": SpiceBADVARASSIGN,
    "SPICE(BADWINDOWSIZE)": SpiceBADWINDOWSIZE,
    "SPICE(BARRAYTOOSMALL)": SpiceBARRAYTOOSMALL,
    "SPICE(BARYCENTERIDCODE)": SpiceBARYCENTERIDCODE,
    "SPICE(BEFOREBEGSTR)": SpiceBEFOREBEGSTR,
    "SPICE(BLANKCOMMANDLINE)": SpiceBLANKCOMMANDLINE,
    "SPICE(BLANKFILETYPE)": SpiceBLANKFILETYPE,
    "SPICE(BLANKINPUTFILENAME)": SpiceBLANKINPUTFILENAME,
    "SPICE(BLANKINPUTTIME)": SpiceBLANKINPUTTIME,
    "SPICE(BLANKNAMEASSIGNED)": SpiceBLANKNAMEASSIGNED,
    "SPICE(BLANKOUTPTFILENAME)": SpiceBLANKOUTPTFILENAME,
    "SPICE(BLANKSCLKSTRING)": SpiceBLANKSCLKSTRING,
    "SPICE(BLANKTIMEFORMAT)": SpiceBLANKTIMEFORMAT,
    "SPICE(BLOCKSNOTEVEN)": SpiceBLOCKSNOTEVEN,
    "SPICE(BOGUSENTRY)": SpiceBOGUSENTRY,
    "SPICE(BOUNDSDISAGREE)": SpiceBOUNDSDISAGREE,
    "SPICE(BUFFERSIZESMISMATCH)": SpiceBUFFERSIZESMISMATCH,
    "SPICE(BUFFEROVERRUN1)":SpiceBUFFEROVERRUN1,
    "SPICE(BUFFEROVERRUN2)":SpiceBUFFEROVERRUN2,
    "SPICE(BUFFEROVERRUN3)":SpiceBUFFEROVERRUN3,
    "SPICE(BUFFEROVERRUN4)":SpiceBUFFEROVERRUN4,
    "SPICE(BUFFERTOOSMALL)": SpiceBUFFERTOOSMALL,
    "SPICE(BUG0)":SpiceBUG0,
    "SPICE(BUG1)":SpiceBUG1,
    "SPICE(BUG2)":SpiceBUG2,
    "SPICE(BUG3)":SpiceBUG3,
    "SPICE(BUG4)":SpiceBUG4,
    "SPICE(BUG5)":SpiceBUG5,
    "SPICE(BUGWRITEFAILED)": SpiceBUGWRITEFAILED,
    "SPICE(CALLCKBSSFIRST)": SpiceCALLCKBSSFIRST,
    "SPICE(CALLEDOUTOFORDER)": SpiceCALLEDOUTOFORDER,
    "SPICE(CALLZZDSKBSSFIRST)": SpiceCALLZZDSKBSSFIRST,
    "SPICE(CANNOTFINDGRP)": SpiceCANNOTFINDGRP,
    "SPICE(CANNOTGETDEFAULTS1)":SpiceCANNOTGETDEFAULTS1,
    "SPICE(CANNOTGETDEFAULTS2)":SpiceCANNOTGETDEFAULTS2,
    "SPICE(CANNOTGETPACKET)": SpiceCANNOTGETPACKET,
    "SPICE(CANNOTMAKEFILE)": SpiceCANNOTMAKEFILE,
    "SPICE(CANNOTPICKFRAME)": SpiceCANNOTPICKFRAME,
    "SPICE(CANTGETROTATIONTYPE)": SpiceCANTGETROTATIONTYPE,
    "SPICE(CANTPICKDEFAULTS1)":SpiceCANTPICKDEFAULTS1,
    "SPICE(CANTPICKDEFAULTS2)":SpiceCANTPICKDEFAULTS2,
    "SPICE(CANTPICKDEFAULTS3)":SpiceCANTPICKDEFAULTS3,
    "SPICE(CANTPICKDEFAULTS4)":SpiceCANTPICKDEFAULTS4,
    "SPICE(CANTUSEPERIAPEPOCH)": SpiceCANTUSEPERIAPEPOCH,
    "SPICE(CBNOSUCHSTR)": SpiceCBNOSUCHSTR,
    "SPICE(CELLARRAYTOOSMALL)": SpiceCELLARRAYTOOSMALL,
    "SPICE(CHRONOSBUG1)":SpiceCHRONOSBUG1,
    "SPICE(CHRONOSBUG10)":SpiceCHRONOSBUG10,
    "SPICE(CHRONOSBUG2)":SpiceCHRONOSBUG2,
    "SPICE(CHRONOSBUG3)":SpiceCHRONOSBUG3,
    "SPICE(CHRONOSBUG4)":SpiceCHRONOSBUG4,
    "SPICE(CHRONOSBUG5)":SpiceCHRONOSBUG5,
    "SPICE(CHRONOSBUG6)":SpiceCHRONOSBUG6,
    "SPICE(CHRONOSBUG7)":SpiceCHRONOSBUG7,
    "SPICE(CHRONOSBUG8)":SpiceCHRONOSBUG8,
    "SPICE(CHRONOSBUG9)":SpiceCHRONOSBUG9,
    "SPICE(CK3SDNBUG)":SpiceCK3SDNBUG,
    "SPICE(CKBOGUSENTRY)": SpiceCKBOGUSENTRY,
    "SPICE(CKDOESNTEXIST)": SpiceCKDOESNTEXIST,
    "SPICE(CKFILE)": SpiceCKFILE,
    "SPICE(CKNONEXISTREC)": SpiceCKNONEXISTREC,
    "SPICE(CKUNKNOWNDATATYPE)": SpiceCKUNKNOWNDATATYPE,
    "SPICE(CKWRONGDATATYPE)": SpiceCKWRONGDATATYPE,
    "SPICE(CLIBCALLFAILED)": SpiceCLIBCALLFAILED,
    "SPICE(CLUSTERWRITEERROR)": SpiceCLUSTERWRITEERROR,
    "SPICE(CMDERROR)": SpiceCMDERROR,
    "SPICE(CMDPARSEERROR)": SpiceCMDPARSEERROR,
    "SPICE(COARSEGRIDOVERFLOW)": SpiceCOARSEGRIDOVERFLOW,
    "SPICE(COLDESCTABLEFULL)": SpiceCOLDESCTABLEFULL,
    "SPICE(COMMANDTOOLONG)": SpiceCOMMANDTOOLONG,
    "SPICE(COMMFILENOTEXIST)": SpiceCOMMFILENOTEXIST,
    "SPICE(COMPETINGEPOCHSPEC)": SpiceCOMPETINGEPOCHSPEC,
    "SPICE(COMPETINGFRAMESPEC)": SpiceCOMPETINGFRAMESPEC,
    "SPICE(COUNTMISMATCH)": SpiceCOUNTMISMATCH,
    "SPICE(COUNTTOOLARGE)": SpiceCOUNTTOOLARGE,
    "SPICE(COVFRAME1MISMATCH)":SpiceCOVFRAME1MISMATCH,
    "SPICE(COVFRAME1NODATA1)":SpiceCOVFRAME1NODATA1,
    "SPICE(COVFRAME1NODATA2)":SpiceCOVFRAME1NODATA2,
    "SPICE(COVFRAME2MISMATCH)":SpiceCOVFRAME2MISMATCH,
    "SPICE(COVFRAME2NODATA1)":SpiceCOVFRAME2NODATA1,
    "SPICE(COVFRAME2NODATA2)":SpiceCOVFRAME2NODATA2,
    "SPICE(DAFBADCRECLEN)": SpiceDAFBADCRECLEN,
    "SPICE(DAFBADRECLEN)": SpiceDAFBADRECLEN,
    "SPICE(DAFCRNOTFOUND)": SpiceDAFCRNOTFOUND,
    "SPICE(DAFDPWRITEFAIL)": SpiceDAFDPWRITEFAIL,
    "SPICE(DAFILLEGWRITE)": SpiceDAFILLEGWRITE,
    "SPICE(DAFINVALIDACCESS)": SpiceDAFINVALIDACCESS,
    "SPICE(DAFINVALIDPARAMS)": SpiceDAFINVALIDPARAMS,
    "SPICE(DAFNEWCONFLICT)": SpiceDAFNEWCONFLICT,
    "SPICE(DAFNOIDWORD)": SpiceDAFNOIDWORD,
    "SPICE(DAFNOIFNMATCH)": SpiceDAFNOIFNMATCH,
    "SPICE(DAFNONAMEMATCH)": SpiceDAFNONAMEMATCH,
    "SPICE(DAFNORESV)": SpiceDAFNORESV,
    "SPICE(DAFNOSUCHADDR)": SpiceDAFNOSUCHADDR,
    "SPICE(DAFNOSUCHFILE)": SpiceDAFNOSUCHFILE,
    "SPICE(DAFNOSUCHHANDLE)": SpiceDAFNOSUCHHANDLE,
    "SPICE(DAFNOSUCHUNIT)": SpiceDAFNOSUCHUNIT,
    "SPICE(DAFNOWRITE)": SpiceDAFNOWRITE,
    "SPICE(DAFOVERFLOW)": SpiceDAFOVERFLOW,
    "SPICE(DAFREADFAIL)": SpiceDAFREADFAIL,
    "SPICE(DAFWRITEFAIL)": SpiceDAFWRITEFAIL,
    "SPICE(DASFILEWRITEFAILED)": SpiceDASFILEWRITEFAILED,
    "SPICE(DASIDWORDNOTKNOWN)": SpiceDASIDWORDNOTKNOWN,
    "SPICE(DASINVALIDACCESS)": SpiceDASINVALIDACCESS,
    "SPICE(DASINVALIDCOUNT)": SpiceDASINVALIDCOUNT,
    "SPICE(DASINVALIDTYPE)": SpiceDASINVALIDTYPE,
    "SPICE(DASNOIDWORD)": SpiceDASNOIDWORD,
    "SPICE(DASNOSUCHADDRESS)": SpiceDASNOSUCHADDRESS,
    "SPICE(DASNOSUCHFILE)": SpiceDASNOSUCHFILE,
    "SPICE(DASNOSUCHUNIT)": SpiceDASNOSUCHUNIT,
    "SPICE(DASNOTEMPTY)": SpiceDASNOTEMPTY,
    "SPICE(DASREADFAIL)": SpiceDASREADFAIL,
    "SPICE(DASWRITEFAIL)": SpiceDASWRITEFAIL,
    "SPICE(DATAITEMLIMITEXCEEDED)": SpiceDATAITEMLIMITEXCEEDED,
    "SPICE(DATAREADFAILED)": SpiceDATAREADFAILED,
    "SPICE(DATATYPENOTRECOG)": SpiceDATATYPENOTRECOG,
    "SPICE(DATAWIDTHERROR)": SpiceDATAWIDTHERROR,
    "SPICE(DATEEXPECTED)": SpiceDATEEXPECTED,
    "SPICE(DECODINGERROR)": SpiceDECODINGERROR,
    "SPICE(DIFFLINETOOLARGE)": SpiceDIFFLINETOOLARGE,
    "SPICE(DIFFLINETOOSMALL)": SpiceDIFFLINETOOSMALL,
    "SPICE(DIMENSIONTOOSMALL)": SpiceDIMENSIONTOOSMALL,
    "SPICE(DISARRAY)": SpiceDISARRAY,
    "SPICE(DISORDER)": SpiceDISORDER,
    "SPICE(DSKBOGUSENTRY)": SpiceDSKBOGUSENTRY,
    "SPICE(DSKDATANOTFOUND)": SpiceDSKDATANOTFOUND,
    "SPICE(DSKTOOMANYFILES)": SpiceDSKTOOMANYFILES,
    "SPICE(DUPLICATETIMES)": SpiceDUPLICATETIMES,
    "SPICE(ECCOUTOFBOUNDS)": SpiceECCOUTOFBOUNDS,
    "SPICE(EKCOLNUMMISMATCH)": SpiceEKCOLNUMMISMATCH,
    "SPICE(EKFILE)": SpiceEKFILE,
    "SPICE(EKMISSINGCOLUMN)": SpiceEKMISSINGCOLUMN,
    "SPICE(EKSEGTABLEFULL)": SpiceEKSEGTABLEFULL,
    "SPICE(EKTABLELISTFULL)": SpiceEKTABLELISTFULL,
    "SPICE(EMBEDDEDBLANK)": SpiceEMBEDDEDBLANK,
    "SPICE(EMPTYINPUTFILE)": SpiceEMPTYINPUTFILE,
    "SPICE(ENDOFFILE)": SpiceENDOFFILE,
    "SPICE(ENDPOINTSMATCH)": SpiceENDPOINTSMATCH,
    "SPICE(ERROREXIT)": SpiceERROREXIT,
    "SPICE(EVECOUTOFRANGE)": SpiceEVECOUTOFRANGE,
    "SPICE(EVENHERMITDEGREE)": SpiceEVENHERMITDEGREE,
    "SPICE(EVILBOGUSENTRY)": SpiceEVILBOGUSENTRY,
    "SPICE(EXTERNALOPEN)": SpiceEXTERNALOPEN,
    "SPICE(FACENOTFOUND)": SpiceFACENOTFOUND,
    "SPICE(FAKESCLKEXISTS)": SpiceFAKESCLKEXISTS,
    "SPICE(FILARCHMISMATCH)": SpiceFILARCHMISMATCH,
    "SPICE(FILARCMISMATCH)": SpiceFILARCMISMATCH,
    "SPICE(FILEALREADYEXISTS)": SpiceFILEALREADYEXISTS,
    "SPICE(FILEALREADYOPEN)": SpiceFILEALREADYOPEN,
    "SPICE(FILEDELETEFAILED)": SpiceFILEDELETEFAILED,
    "SPICE(FILEDOESNTEXIST1)":SpiceFILEDOESNTEXIST1,
    "SPICE(FILEDOESNTEXIST2)":SpiceFILEDOESNTEXIST2,
    "SPICE(FILEDOESNTEXIST3)":SpiceFILEDOESNTEXIST3,
    "SPICE(FILEEXISTS)": SpiceFILEEXISTS,
    "SPICE(FILENAMETOOLONG)": SpiceFILENAMETOOLONG,
    "SPICE(FILENOTCONNECTED)": SpiceFILENOTCONNECTED,
    "SPICE(FILENOTOPEN)": SpiceFILENOTOPEN,
    "SPICE(FILEOPENCONFLICT)": SpiceFILEOPENCONFLICT,
    "SPICE(FILEOPENERROR)": SpiceFILEOPENERROR,
    "SPICE(FILEOPENFAIL)": SpiceFILEOPENFAIL,
    "SPICE(FILEREADERROR)": SpiceFILEREADERROR,
    "SPICE(FILETABLEFULL)": SpiceFILETABLEFULL,
    "SPICE(FILETRUNCATED)": SpiceFILETRUNCATED,
    "SPICE(FILEWRITEFAILED)": SpiceFILEWRITEFAILED,
    "SPICE(FIRSTRECORDMISMATCH)": SpiceFIRSTRECORDMISMATCH,
    "SPICE(FKDOESNTEXIST)": SpiceFKDOESNTEXIST,
    "SPICE(FMTITEMLIMITEXCEEDED)": SpiceFMTITEMLIMITEXCEEDED,
    "SPICE(FORMATDATAMISMATCH)": SpiceFORMATDATAMISMATCH,
    "SPICE(FORMATDOESNTAPPLY)": SpiceFORMATDOESNTAPPLY,
    "SPICE(FORMATERROR)": SpiceFORMATERROR,
    "SPICE(FORMATITEMLIMITEXCEEDED)": SpiceFORMATITEMLIMITEXCEEDED,
    "SPICE(FORMATNOTAPPLICABLE)": SpiceFORMATNOTAPPLICABLE,
    "SPICE(FORMATSTRINGTOOLONG)": SpiceFORMATSTRINGTOOLONG,
    "SPICE(FOVTOOWIDE)": SpiceFOVTOOWIDE,
    "SPICE(FRAMEAIDCODENOTFOUND)": SpiceFRAMEAIDCODENOTFOUND,
    "SPICE(FRAMEBIDCODENOTFOUND)": SpiceFRAMEBIDCODENOTFOUND,
    "SPICE(FRAMEDATANOTFOUND)": SpiceFRAMEDATANOTFOUND,
    "SPICE(FRAMEDEFERROR)": SpiceFRAMEDEFERROR,
    "SPICE(FRAMEINFONOTFOUND)": SpiceFRAMEINFONOTFOUND,
    "SPICE(FRAMENOTFOUND)": SpiceFRAMENOTFOUND,
    "SPICE(FRAMENOTRECOGNIZED)": SpiceFRAMENOTRECOGNIZED,
    "SPICE(FRMDIFFBUG1)":SpiceFRMDIFFBUG1,
    "SPICE(FRMDIFFBUG2)":SpiceFRMDIFFBUG2,
    "SPICE(FRMDIFFBUG3)":SpiceFRMDIFFBUG3,
    "SPICE(FRMDIFFBUG4)":SpiceFRMDIFFBUG4,
    "SPICE(FRMDIFFBUG5)":SpiceFRMDIFFBUG5,
    "SPICE(FRMDIFFBUG6)":SpiceFRMDIFFBUG6,
    "SPICE(FRMDIFFBUG7)":SpiceFRMDIFFBUG7,
    "SPICE(FRMDIFFBUG8)":SpiceFRMDIFFBUG8,
    "SPICE(FRMDIFFBUG9)":SpiceFRMDIFFBUG9,
    "SPICE(FTFULL)": SpiceFTFULL,
    "SPICE(FTPXFERERROR)": SpiceFTPXFERERROR,
    "SPICE(HANDLENOTFOUND)": SpiceHANDLENOTFOUND,
    "SPICE(HASHISFULL)": SpiceHASHISFULL,
    "SPICE(HLULOCKFAILED)": SpiceHLULOCKFAILED,
    "SPICE(IDENTICALTIMES1)":SpiceIDENTICALTIMES1,
    "SPICE(IDENTICALTIMES2)":SpiceIDENTICALTIMES2,
    "SPICE(IDSTRINGTOOLONG)": SpiceIDSTRINGTOOLONG,
    "SPICE(IDWORDNOTKNOWN)": SpiceIDWORDNOTKNOWN,
    "SPICE(ILLEGALOPTIONNAME)": SpiceILLEGALOPTIONNAME,
    "SPICE(ILLEGSHIFTDIR)": SpiceILLEGSHIFTDIR,
    "SPICE(ILLEGTEMPL)": SpiceILLEGTEMPL,
    "SPICE(IMPROPERFILE)": SpiceIMPROPERFILE,
    "SPICE(IMPROPEROPEN)": SpiceIMPROPEROPEN,
    "SPICE(INACTIVEOBJECT)": SpiceINACTIVEOBJECT,
    "SPICE(INCOMPATIBLEEOL)": SpiceINCOMPATIBLEEOL,
    "SPICE(INCOMPATIBLENUMREF)": SpiceINCOMPATIBLENUMREF,
    "SPICE(INCOMPLETEELEMENTS)": SpiceINCOMPLETEELEMENTS,
    "SPICE(INCOMPLETEFRAME)": SpiceINCOMPLETEFRAME,
    "SPICE(INCOMPLETFRAME)": SpiceINCOMPLETFRAME,
    "SPICE(INCONSISTCENTERID)": SpiceINCONSISTCENTERID,
    "SPICE(INCONSISTELEMENTS)": SpiceINCONSISTELEMENTS,
    "SPICE(INCONSISTENTTIMES)": SpiceINCONSISTENTTIMES,
    "SPICE(INCONSISTENTTIMES1)":SpiceINCONSISTENTTIMES1,
    "SPICE(INCONSISTENTTIMES2)":SpiceINCONSISTENTTIMES2,
    "SPICE(INCONSISTFRAME)": SpiceINCONSISTFRAME,
    "SPICE(INCONSISTSTARTTIME)": SpiceINCONSISTSTARTTIME,
    "SPICE(INCONSISTSTOPTIME)": SpiceINCONSISTSTOPTIME,
    "SPICE(INCORRECTUSAGE)": SpiceINCORRECTUSAGE,
    "SPICE(INDEFINITELOCALSECOND)": SpiceINDEFINITELOCALSECOND,
    "SPICE(INDEXTOOLARGE)": SpiceINDEXTOOLARGE,
    "SPICE(INDICESOUTOFORDER)": SpiceINDICESOUTOFORDER,
    "SPICE(INPUTDOESNOTEXIST)": SpiceINPUTDOESNOTEXIST,
    "SPICE(INPUTFILENOTEXIST)": SpiceINPUTFILENOTEXIST,
    "SPICE(INPUTOUTOFBOUNDS)": SpiceINPUTOUTOFBOUNDS,
    "SPICE(INSIDEBODY)": SpiceINSIDEBODY,
    "SPICE(INSUFFICIENTDATA)": SpiceINSUFFICIENTDATA,
    "SPICE(INSUFFICIENTDATA2)":SpiceINSUFFICIENTDATA2,
    "SPICE(INSUFPTRSIZE)": SpiceINSUFPTRSIZE,
    "SPICE(INTERVALSTARTNOTFOUND)": SpiceINTERVALSTARTNOTFOUND,
    "SPICE(INVALDDEGREE)": SpiceINVALDDEGREE,
    "SPICE(INVALIDACCESS)": SpiceINVALIDACCESS,
    "SPICE(INVALIDADD)": SpiceINVALIDADD,
    "SPICE(INVALIDADDRESS)": SpiceINVALIDADDRESS,
    "SPICE(INVALIDANGLE)": SpiceINVALIDANGLE,
    "SPICE(INVALIDAXES)": SpiceINVALIDAXES,
    "SPICE(INVALIDAXIS)": SpiceINVALIDAXIS,
    "SPICE(INVALIDBOUNDS)": SpiceINVALIDBOUNDS,
    "SPICE(INVALIDCASE)": SpiceINVALIDCASE,
    "SPICE(INVALIDCHECKOUT)": SpiceINVALIDCHECKOUT,
    "SPICE(INVALIDCLUSTERNUM)": SpiceINVALIDCLUSTERNUM,
    "SPICE(INVALIDCOLUMN)": SpiceINVALIDCOLUMN,
    "SPICE(INVALIDCONSTSTEP)": SpiceINVALIDCONSTSTEP,
    "SPICE(INVALIDDATA)": SpiceINVALIDDATA,
    "SPICE(INVALIDDATACOUNT)": SpiceINVALIDDATACOUNT,
    "SPICE(INVALIDDATATYPE)": SpiceINVALIDDATATYPE,
    "SPICE(INVALIDDIRECTION)": SpiceINVALIDDIRECTION,
    "SPICE(INVALIDDIVISOR)": SpiceINVALIDDIVISOR,
    "SPICE(INVALIDENDPTS)": SpiceINVALIDENDPTS,
    "SPICE(INVALIDFILETYPE)": SpiceINVALIDFILETYPE,
    "SPICE(INVALIDFIXREF)": SpiceINVALIDFIXREF,
    "SPICE(INVALIDFLAG)": SpiceINVALIDFLAG,
    "SPICE(INVALIDFOV)": SpiceINVALIDFOV,
    "SPICE(INVALIDGEOMETRY)": SpiceINVALIDGEOMETRY,
    "SPICE(INVALIDHANDLE)": SpiceINVALIDHANDLE,
    "SPICE(INVALIDINPUT1)":SpiceINVALIDINPUT1,
    "SPICE(INVALIDINPUT2)":SpiceINVALIDINPUT2,
    "SPICE(INVALIDINTEGER)": SpiceINVALIDINTEGER,
    "SPICE(INVALIDMETADATA)": SpiceINVALIDMETADATA,
    "SPICE(INVALIDNAME)": SpiceINVALIDNAME,
    "SPICE(INVALIDNODE)": SpiceINVALIDNODE,
    "SPICE(INVALIDNUMBEROFINTERVALS)": SpiceINVALIDNUMBEROFINTERVALS,
    "SPICE(INVALIDNUMBEROFRECORDS)": SpiceINVALIDNUMBEROFRECORDS,
    "SPICE(INVALIDNUMINT)": SpiceINVALIDNUMINT,
    "SPICE(INVALIDNUMREC)": SpiceINVALIDNUMREC,
    "SPICE(INVALIDRADII)": SpiceINVALIDRADII,
    "SPICE(INVALIDREFVAL)": SpiceINVALIDREFVAL,
    "SPICE(INVALIDSCALE)": SpiceINVALIDSCALE,
    "SPICE(INVALIDSCLKRATE)": SpiceINVALIDSCLKRATE,
    "SPICE(INVALIDSCLKSTRING1)":SpiceINVALIDSCLKSTRING1,
    "SPICE(INVALIDSCLKSTRING2)":SpiceINVALIDSCLKSTRING2,
    "SPICE(INVALIDSELECTION)": SpiceINVALIDSELECTION,
    "SPICE(INVALIDSHADOW)": SpiceINVALIDSHADOW,
    "SPICE(INVALIDSHAPE)": SpiceINVALIDSHAPE,
    "SPICE(INVALIDSHAPECOMBO)": SpiceINVALIDSHAPECOMBO,
    "SPICE(INVALIDSUBLIST)": SpiceINVALIDSUBLIST,
    "SPICE(INVALIDTABLENAME)": SpiceINVALIDTABLENAME,
    "SPICE(INVALIDTABLESIZE)": SpiceINVALIDTABLESIZE,
    "SPICE(INVALIDTEXT)": SpiceINVALIDTEXT,
    "SPICE(INVALIDTLEORDER)": SpiceINVALIDTLEORDER,
    "SPICE(INVALIDUNITS)": SpiceINVALIDUNITS,
    "SPICE(INVALIDVALUE1)":SpiceINVALIDVALUE1,
    "SPICE(INVALIDVALUE2)":SpiceINVALIDVALUE2,
    "SPICE(INVERSTARTSTOPTIME)": SpiceINVERSTARTSTOPTIME,
    "SPICE(INVERSTIMES2)":SpiceINVERSTIMES2,
    "SPICE(IRFNOTREC)": SpiceIRFNOTREC,
    "SPICE(ITEMNOTFOUND)": SpiceITEMNOTFOUND,
    "SPICE(ITEMNOTRECOGNIZED)": SpiceITEMNOTRECOGNIZED,
    "SPICE(ITERATIONEXCEEDED)": SpiceITERATIONEXCEEDED,
    "SPICE(JEOPARDIZEDRUN0)":SpiceJEOPARDIZEDRUN0,
    "SPICE(JEOPARDIZEDRUN1)":SpiceJEOPARDIZEDRUN1,
    "SPICE(JEOPARDIZEDRUN2)":SpiceJEOPARDIZEDRUN2,
    "SPICE(JEOPARDIZEDRUN3)":SpiceJEOPARDIZEDRUN3,
    "SPICE(JEOPARDIZEDRUN4)":SpiceJEOPARDIZEDRUN4,
    "SPICE(JEOPARDIZEDRUN5)":SpiceJEOPARDIZEDRUN5,
    "SPICE(KERNELNOTLOADED)": SpiceKERNELNOTLOADED,
    "SPICE(KERVARSETOVERFLOW)": SpiceKERVARSETOVERFLOW,
    "SPICE(KERVARTOOBIG)": SpiceKERVARTOOBIG,
    "SPICE(KEYWORDNOTFOUND)": SpiceKEYWORDNOTFOUND,
    "SPICE(KEYWORDSMISMATCH1)":SpiceKEYWORDSMISMATCH1,
    "SPICE(KEYWORDSMISMATCH2)":SpiceKEYWORDSMISMATCH2,
    "SPICE(KEYWORDSMISMATCH3)":SpiceKEYWORDSMISMATCH3,
    "SPICE(LBCORRUPTED)": SpiceLBCORRUPTED,
    "SPICE(LBINSUFPTRSIZE)": SpiceLBINSUFPTRSIZE,
    "SPICE(LBLINETOOLONG)": SpiceLBLINETOOLONG,
    "SPICE(LBNOSUCHLINE)": SpiceLBNOSUCHLINE,
    "SPICE(LBTOOMANYLINES)": SpiceLBTOOMANYLINES,
    "SPICE(LOWERBOUNDTOOLOW)": SpiceLOWERBOUNDTOOLOW,
    "SPICE(LSKDOESNTEXIST)": SpiceLSKDOESNTEXIST,
    "SPICE(MALFORMEDSEGMENT)": SpiceMALFORMEDSEGMENT,
    "SPICE(MALLOCCOUNT)": SpiceMALLOCCOUNT,
    "SPICE(MARKERNOTFOUND)": SpiceMARKERNOTFOUND,
    "SPICE(META2DEFERR)":SpiceMETA2DEFERR,
    "SPICE(META2TOOMANYKEYS)":SpiceMETA2TOOMANYKEYS,
    "SPICE(MISMATCHFROMTIMETYPE)": SpiceMISMATCHFROMTIMETYPE,
    "SPICE(MISMATCHOUTPUTFORMAT)": SpiceMISMATCHOUTPUTFORMAT,
    "SPICE(MISMATCHTOTIMETYPE)": SpiceMISMATCHTOTIMETYPE,
    "SPICE(MISSINGARGUMENTS)": SpiceMISSINGARGUMENTS,
    "SPICE(MISSINGCENTER)": SpiceMISSINGCENTER,
    "SPICE(MISSINGCOLSTEP)": SpiceMISSINGCOLSTEP,
    "SPICE(MISSINGCOORDBOUND)": SpiceMISSINGCOORDBOUND,
    "SPICE(MISSINGCOORDSYS)": SpiceMISSINGCOORDSYS,
    "SPICE(MISSINGDATACLASS)": SpiceMISSINGDATACLASS,
    "SPICE(MISSINGDATAORDERTK)": SpiceMISSINGDATAORDERTK,
    "SPICE(MISSINGDATATYPE)": SpiceMISSINGDATATYPE,
    "SPICE(MISSINGEOT)": SpiceMISSINGEOT,
    "SPICE(MISSINGEPOCHTOKEN)": SpiceMISSINGEPOCHTOKEN,
    "SPICE(MISSINGFILENAMES1)":SpiceMISSINGFILENAMES1,
    "SPICE(MISSINGFILENAMES2)":SpiceMISSINGFILENAMES2,
    "SPICE(MISSINGFILENAMES3)":SpiceMISSINGFILENAMES3,
    "SPICE(MISSINGFRAME)": SpiceMISSINGFRAME,
    "SPICE(MISSINGFRAMEVAR)": SpiceMISSINGFRAMEVAR,
    "SPICE(MISSINGGEOCONSTS)": SpiceMISSINGGEOCONSTS,
    "SPICE(MISSINGHEIGHTREF)": SpiceMISSINGHEIGHTREF,
    "SPICE(MISSINGHSCALE)": SpiceMISSINGHSCALE,
    "SPICE(MISSINGKPV)": SpiceMISSINGKPV,
    "SPICE(MISSINGLEFTCOR)": SpiceMISSINGLEFTCOR,
    "SPICE(MISSINGLEFTRTFLAG)": SpiceMISSINGLEFTRTFLAG,
    "SPICE(MISSINGNCAPFLAG)": SpiceMISSINGNCAPFLAG,
    "SPICE(MISSINGNCOLS)": SpiceMISSINGNCOLS,
    "SPICE(MISSINGNROWS)": SpiceMISSINGNROWS,
    "SPICE(MISSINGPLATETYPE)": SpiceMISSINGPLATETYPE,
    "SPICE(MISSINGROWMAJFLAG)": SpiceMISSINGROWMAJFLAG,
    "SPICE(MISSINGROWSTEP)": SpiceMISSINGROWSTEP,
    "SPICE(MISSINGSCAPFLAG)": SpiceMISSINGSCAPFLAG,
    "SPICE(MISSINGSURFACE)": SpiceMISSINGSURFACE,
    "SPICE(MISSINGTLEIDKEYWORD)": SpiceMISSINGTLEIDKEYWORD,
    "SPICE(MISSINGTLEKEYWORD)": SpiceMISSINGTLEKEYWORD,
    "SPICE(MISSINGTOPCOR)": SpiceMISSINGTOPCOR,
    "SPICE(MISSINGTOPDOWNFLAG)": SpiceMISSINGTOPDOWNFLAG,
    "SPICE(MISSINGVOXELSCALE)": SpiceMISSINGVOXELSCALE,
    "SPICE(MISSINGWRAPFLAG)": SpiceMISSINGWRAPFLAG,
    "SPICE(MKSPKBUG3)":SpiceMKSPKBUG3,
    "SPICE(MKSPKBUGSETUP1)":SpiceMKSPKBUGSETUP1,
    "SPICE(MKSPKBUGSETUP2)":SpiceMKSPKBUGSETUP2,
    "SPICE(MKSPKBUGSETUP3)":SpiceMKSPKBUGSETUP3,
    "SPICE(MKSPKBUGSETUP4)":SpiceMKSPKBUGSETUP4,
    "SPICE(MKSPKBUGSETUP5)":SpiceMKSPKBUGSETUP5,
    "SPICE(MKSPKTLE2SPKBUG0)":SpiceMKSPKTLE2SPKBUG0,
    "SPICE(MKSPKTLE2SPKBUG1)":SpiceMKSPKTLE2SPKBUG1,
    "SPICE(MKSPKTLE2SPKBUG2)":SpiceMKSPKTLE2SPKBUG2,
    "SPICE(MKSPKTLE2SPKBUG3)":SpiceMKSPKTLE2SPKBUG3,
    "SPICE(MKSPKTLE2SPKBUG4)":SpiceMKSPKTLE2SPKBUG4,
    "SPICE(MSGNAME)": SpiceMSGNAME,
    "SPICE(NAMENOTFOUND)": SpiceNAMENOTFOUND,
    "SPICE(NAMENOTRECOGNIZED)": SpiceNAMENOTRECOGNIZED,
    "SPICE(NAMENOTUNIQUE)": SpiceNAMENOTUNIQUE,
    "SPICE(NAMESNOTRESOLVED)": SpiceNAMESNOTRESOLVED,
    "SPICE(NAMETABLEFULL)": SpiceNAMETABLEFULL,
    "SPICE(NARATESFLAG)": SpiceNARATESFLAG,
    "SPICE(NEGATIVEHASHVALUE1)":SpiceNEGATIVEHASHVALUE1,
    "SPICE(NEGATIVEHASHVALUE2)":SpiceNEGATIVEHASHVALUE2,
    "SPICE(NEGATIVETOL)": SpiceNEGATIVETOL,
    "SPICE(NOACCEPTABLEDATA)": SpiceNOACCEPTABLEDATA,
    "SPICE(NOANGULARRATEFLAG)": SpiceNOANGULARRATEFLAG,
    "SPICE(NOARRAYSTARTED)": SpiceNOARRAYSTARTED,
    "SPICE(NOATTIME)": SpiceNOATTIME,
    "SPICE(NOAVDATA)": SpiceNOAVDATA,
    "SPICE(NOBODYID)": SpiceNOBODYID,
    "SPICE(NOCANDOSPKSPCKS)": SpiceNOCANDOSPKSPCKS,
    "SPICE(NOCENTERIDORNAME)": SpiceNOCENTERIDORNAME,
    "SPICE(NOCKSEGMENTTYPE)": SpiceNOCKSEGMENTTYPE,
    "SPICE(NOCOMMENTSFILE)": SpiceNOCOMMENTSFILE,
    "SPICE(NOCONVERG)": SpiceNOCONVERG,
    "SPICE(NOCONVERGENCE)": SpiceNOCONVERGENCE,
    "SPICE(NODATA)": SpiceNODATA,
    "SPICE(NODATAORDER)": SpiceNODATAORDER,
    "SPICE(NODATATYPEFLAG)": SpiceNODATATYPEFLAG,
    "SPICE(NODELIMCHARACTER)": SpiceNODELIMCHARACTER,
    "SPICE(NODETOOFULL)": SpiceNODETOOFULL,
    "SPICE(NODSKSEGMENT)": SpiceNODSKSEGMENT,
    "SPICE(NODSKSEGMENTS)": SpiceNODSKSEGMENTS,
    "SPICE(NOENVVARIABLE)": SpiceNOENVVARIABLE,
    "SPICE(NOEULERANGLEUNITS)": SpiceNOEULERANGLEUNITS,
    "SPICE(NOFILENAMES)": SpiceNOFILENAMES,
    "SPICE(NOFILES)": SpiceNOFILES,
    "SPICE(NOFILESPEC)": SpiceNOFILESPEC,
    "SPICE(NOFRAMECONNECT)": SpiceNOFRAMECONNECT,
    "SPICE(NOFRAMEDATA)": SpiceNOFRAMEDATA,
    "SPICE(NOFRAMENAME)": SpiceNOFRAMENAME,
    "SPICE(NOFRAMESKERNELNAME)": SpiceNOFRAMESKERNELNAME,
    "SPICE(NOFREELOGICALUNIT)": SpiceNOFREELOGICALUNIT,
    "SPICE(NOFREENODES)": SpiceNOFREENODES,
    "SPICE(NOFROMTIME)": SpiceNOFROMTIME,
    "SPICE(NOFROMTIMESYSTEM)": SpiceNOFROMTIMESYSTEM,
    "SPICE(NOHEADNODE)": SpiceNOHEADNODE,
    "SPICE(NOINFO)": SpiceNOINFO,
    "SPICE(NOINPUTDATATYPE)": SpiceNOINPUTDATATYPE,
    "SPICE(NOINPUTFILENAME)": SpiceNOINPUTFILENAME,
    "SPICE(NOINSTRUMENTID)": SpiceNOINSTRUMENTID,
    "SPICE(NOKERNELLOADED)": SpiceNOKERNELLOADED,
    "SPICE(NOLANDINGTIME)": SpiceNOLANDINGTIME,
    "SPICE(NOLEAPSECONDS)": SpiceNOLEAPSECONDS,
    "SPICE(NOLINESPERRECCOUNT)": SpiceNOLINESPERRECCOUNT,
    "SPICE(NOLISTFILENAME)": SpiceNOLISTFILENAME,
    "SPICE(NOLOADEDDSKFILES)": SpiceNOLOADEDDSKFILES,
    "SPICE(NOLSKFILENAME)": SpiceNOLSKFILENAME,
    "SPICE(NONAPPLICABLETYPE1)":SpiceNONAPPLICABLETYPE1,
    "SPICE(NONAPPLICABLETYPE2)":SpiceNONAPPLICABLETYPE2,
    "SPICE(NONDISTINCTPAIR)": SpiceNONDISTINCTPAIR,
    "SPICE(NONEMPTYENTRY)": SpiceNONEMPTYENTRY,
    "SPICE(NONEMPTYTREE)": SpiceNONEMPTYTREE,
    "SPICE(NONEXISTELEMENTS)": SpiceNONEXISTELEMENTS,
    "SPICE(NONINTEGERFIELD)": SpiceNONINTEGERFIELD,
    "SPICE(NONNUMERICSTRING)": SpiceNONNUMERICSTRING,
    "SPICE(NONPOSBUFLENGTH)": SpiceNONPOSBUFLENGTH,
    "SPICE(NONPOSITIVEAXIS)": SpiceNONPOSITIVEAXIS,
    "SPICE(NONPOSITIVERADIUS)": SpiceNONPOSITIVERADIUS,
    "SPICE(NONPOSITIVEVALUE)": SpiceNONPOSITIVEVALUE,
    "SPICE(NONPOSPACKETSIZE)": SpiceNONPOSPACKETSIZE,
    "SPICE(NONPRINTINGCHAR)": SpiceNONPRINTINGCHAR,
    "SPICE(NONPRINTINGCHARS)": SpiceNONPRINTINGCHARS,
    "SPICE(NONUNITNORMAL)": SpiceNONUNITNORMAL,
    "SPICE(NONUNITQUATERNION)": SpiceNONUNITQUATERNION,
    "SPICE(NOOBJECTIDORNAME)": SpiceNOOBJECTIDORNAME,
    "SPICE(NOOFFSETANGLEAXES)": SpiceNOOFFSETANGLEAXES,
    "SPICE(NOOFFSETANGLEUNITS)": SpiceNOOFFSETANGLEUNITS,
    "SPICE(NOOUTPUTFILENAME)": SpiceNOOUTPUTFILENAME,
    "SPICE(NOOUTPUTSPKTYPE)": SpiceNOOUTPUTSPKTYPE,
    "SPICE(NOPICTURE)": SpiceNOPICTURE,
    "SPICE(NOPLATES)": SpiceNOPLATES,
    "SPICE(NOPOLYNOMIALDEGREE)": SpiceNOPOLYNOMIALDEGREE,
    "SPICE(NOPRECESSIONTYPE)": SpiceNOPRECESSIONTYPE,
    "SPICE(NOPRODUCERID)": SpiceNOPRODUCERID,
    "SPICE(NORATESFORTYPE2CK)":SpiceNORATESFORTYPE2CK,
    "SPICE(NOROTATIONORDER)": SpiceNOROTATIONORDER,
    "SPICE(NOSCID)": SpiceNOSCID,
    "SPICE(NOSCLKFILENAMES)": SpiceNOSCLKFILENAMES,
    "SPICE(NOSECONDLINE)": SpiceNOSECONDLINE,
    "SPICE(NOSECONDLINE2)":SpiceNOSECONDLINE2,
    "SPICE(NOSEGMENT)": SpiceNOSEGMENT,
    "SPICE(NOSLKFILENAME)": SpiceNOSLKFILENAME,
    "SPICE(NOSOLMARKER)": SpiceNOSOLMARKER,
    "SPICE(NOSPACECRAFTID)": SpiceNOSPACECRAFTID,
    "SPICE(NOSTARTTIME)": SpiceNOSTARTTIME,
    "SPICE(NOSTARTTIME4SPK15)":SpiceNOSTARTTIME4SPK15,
    "SPICE(NOSTARTTIME4SPK17)":SpiceNOSTARTTIME4SPK17,
    "SPICE(NOSTOPTIME)": SpiceNOSTOPTIME,
    "SPICE(NOSTOPTIME4SPK15)":SpiceNOSTOPTIME4SPK15,
    "SPICE(NOSTOPTIME4SPK17)":SpiceNOSTOPTIME4SPK17,
    "SPICE(NOSUCHHANDLE)": SpiceNOSUCHHANDLE,
    "SPICE(NOSUCHSYMBOL)": SpiceNOSUCHSYMBOL,
    "SPICE(NOSUNGM)": SpiceNOSUNGM,
    "SPICE(NOSURFACENAME)": SpiceNOSURFACENAME,
    "SPICE(NOTABINARYKERNEL)": SpiceNOTABINARYKERNEL,
    "SPICE(NOTACKFILE)": SpiceNOTACKFILE,
    "SPICE(NOTAKERNELFILE1)":SpiceNOTAKERNELFILE1,
    "SPICE(NOTAKERNELFILE2)":SpiceNOTAKERNELFILE2,
    "SPICE(NOTANDPNUMBER)": SpiceNOTANDPNUMBER,
    "SPICE(NOTANINTEGERNUMBER)": SpiceNOTANINTEGERNUMBER,
    "SPICE(NOTANINTNUMBER)": SpiceNOTANINTNUMBER,
    "SPICE(NOTANINTNUMBER2)":SpiceNOTANINTNUMBER2,
    "SPICE(NOTAPCKFILE)": SpiceNOTAPCKFILE,
    "SPICE(NOTATEXTFILE)": SpiceNOTATEXTFILE,
    "SPICE(NOTATRANSFERFILE)": SpiceNOTATRANSFERFILE,
    "SPICE(NOTCOMPUTABLE)": SpiceNOTCOMPUTABLE,
    "SPICE(NOTDIMENSIONALLYEQUIV)": SpiceNOTDIMENSIONALLYEQUIV,
    "SPICE(NOTDISJOINT)": SpiceNOTDISJOINT,
    "SPICE(NOTDISTINCT)": SpiceNOTDISTINCT,
    "SPICE(NOTENOUGHDATA0)":SpiceNOTENOUGHDATA0,
    "SPICE(NOTENOUGHDATA1)":SpiceNOTENOUGHDATA1,
    "SPICE(NOTENOUGHDATA2)": SpiceNOTENOUGHDATA2,
    "SPICE(NOTENOUGHDATA3)":SpiceNOTENOUGHDATA3,
    "SPICE(NOTENOUGHDATA4)":SpiceNOTENOUGHDATA4,
    "SPICE(NOTENOUGHDATA5)":SpiceNOTENOUGHDATA5,
    "SPICE(NOTENOUGHDATA6)":SpiceNOTENOUGHDATA6,
    "SPICE(NOTENOUGHDATA7)":SpiceNOTENOUGHDATA7,
    "SPICE(NOTENOUGHDATA8)":SpiceNOTENOUGHDATA8,
    "SPICE(NOTENOUGHPEAS)": SpiceNOTENOUGHPEAS,
    "SPICE(NOTFOUND)": SpiceNOTFOUND,
    "SPICE(NOTIMEBOUNDS1)":SpiceNOTIMEBOUNDS1,
    "SPICE(NOTIMEBOUNDS10)":SpiceNOTIMEBOUNDS10,
    "SPICE(NOTIMEBOUNDS11)":SpiceNOTIMEBOUNDS11,
    "SPICE(NOTIMEBOUNDS12)":SpiceNOTIMEBOUNDS12,
    "SPICE(NOTIMEBOUNDS4)":SpiceNOTIMEBOUNDS4,
    "SPICE(NOTIMEBOUNDS5)":SpiceNOTIMEBOUNDS5,
    "SPICE(NOTIMEBOUNDS6)":SpiceNOTIMEBOUNDS6,
    "SPICE(NOTIMEBOUNDS7)":SpiceNOTIMEBOUNDS7,
    "SPICE(NOTIMEBOUNDS8)":SpiceNOTIMEBOUNDS8,
    "SPICE(NOTIMEBOUNDS9)":SpiceNOTIMEBOUNDS9,
    "SPICE(NOTIMETYPEFLAG)": SpiceNOTIMETYPEFLAG,
    "SPICE(NOTINDEXED)": SpiceNOTINDEXED,
    "SPICE(NOTINTEGERNUMBER2)":SpiceNOTINTEGERNUMBER2,
    "SPICE(NOTISOFORMAT)": SpiceNOTISOFORMAT,
    "SPICE(NOTLEDATAFOROBJECT)": SpiceNOTLEDATAFOROBJECT,
    "SPICE(NOTLEGALCB)": SpiceNOTLEGALCB,
    "SPICE(NOTOTIME)": SpiceNOTOTIME,
    "SPICE(NOTOTIMESYSTEM)": SpiceNOTOTIMESYSTEM,
    "SPICE(NOTPOSITIVE)": SpiceNOTPOSITIVE,
    "SPICE(NOTSEMCHECKED)": SpiceNOTSEMCHECKED,
    "SPICE(NOTTWOFIELDSCLK)": SpiceNOTTWOFIELDSCLK,
    "SPICE(NOTTWOMODULI)": SpiceNOTTWOMODULI,
    "SPICE(NOTTWOOFFSETS)": SpiceNOTTWOOFFSETS,
    "SPICE(NOTTYPE1SCLK)":SpiceNOTTYPE1SCLK,
    "SPICE(NOUNITSPEC)": SpiceNOUNITSPEC,
    "SPICE(NUMBEREXPECTED)": SpiceNUMBEREXPECTED,
    "SPICE(NUMCONSTANTSNEG)": SpiceNUMCONSTANTSNEG,
    "SPICE(NUMPACKETSNOTPOS)": SpiceNUMPACKETSNOTPOS,
    "SPICE(OBJECTLISTFULL)": SpiceOBJECTLISTFULL,
    "SPICE(OBJECTSTOOCLOSE)": SpiceOBJECTSTOOCLOSE,
    "SPICE(OBSIDCODENOTFOUND)": SpiceOBSIDCODENOTFOUND,
    "SPICE(ORBITDECAY)": SpiceORBITDECAY,
    "SPICE(OUTOFPLACEDELIMITER)": SpiceOUTOFPLACEDELIMITER,
    "SPICE(OUTOFRANGE)": SpiceOUTOFRANGE,
    "SPICE(OUTPUTERROR)": SpiceOUTPUTERROR,
    "SPICE(OUTPUTFILEEXISTS)": SpiceOUTPUTFILEEXISTS,
    "SPICE(OUTPUTISNOTSPK)": SpiceOUTPUTISNOTSPK,
    "SPICE(OUTPUTTOOLONG)": SpiceOUTPUTTOOLONG,
    "SPICE(OUTPUTTOOSHORT)": SpiceOUTPUTTOOSHORT,
    "SPICE(PARSERNOTREADY)": SpicePARSERNOTREADY,
    "SPICE(PARTIALFRAMESPEC)": SpicePARTIALFRAMESPEC,
    "SPICE(PASTENDSTR)": SpicePASTENDSTR,
    "SPICE(PATHMISMATCH)": SpicePATHMISMATCH,
    "SPICE(PATHTOOLONG)": SpicePATHTOOLONG,
    "SPICE(PCKDOESNTEXIST)": SpicePCKDOESNTEXIST,
    "SPICE(PCKFILE)": SpicePCKFILE,
    "SPICE(PCKKRECTOOLARGE)": SpicePCKKRECTOOLARGE,
    "SPICE(PCKRECTOOLARGE)": SpicePCKRECTOOLARGE,
    "SPICE(POINTEROUTOFRANGE)": SpicePOINTEROUTOFRANGE,
    "SPICE(POINTERSETTOOBIG)": SpicePOINTERSETTOOBIG,
    "SPICE(POINTERTABLEFULL)": SpicePOINTERTABLEFULL,
    "SPICE(POINTNOTFOUND)": SpicePOINTNOTFOUND,
    "SPICE(POINTNOTINSEGMENT)": SpicePOINTNOTINSEGMENT,
    "SPICE(POINTOFFSURFACE)": SpicePOINTOFFSURFACE,
    "SPICE(POINTTOOSMALL)": SpicePOINTTOOSMALL,
    "SPICE(PUTCMLCALLEDTWICE)": SpicePUTCMLCALLEDTWICE,
    "SPICE(PUTCMLNOTCALLED)": SpicePUTCMLNOTCALLED,
    "SPICE(QPARAMOUTOFRANGE)": SpiceQPARAMOUTOFRANGE,
    "SPICE(QUERYFAILURE)": SpiceQUERYFAILURE,
    "SPICE(QUERYNOTPARSED)": SpiceQUERYNOTPARSED,
    "SPICE(RADIIOUTOFORDER)": SpiceRADIIOUTOFORDER,
    "SPICE(RAYISZEROVECTOR)": SpiceRAYISZEROVECTOR,
    "SPICE(READFAILED)": SpiceREADFAILED,
    "SPICE(READFAILURE)": SpiceREADFAILURE,
    "SPICE(RECORDNOTFOUND)": SpiceRECORDNOTFOUND,
    "SPICE(RECURSIONTOODEEP)": SpiceRECURSIONTOODEEP,
    "SPICE(REFNOTREC)": SpiceREFNOTREC,
    "SPICE(REFVALNOTINTEGER)": SpiceREFVALNOTINTEGER,
    "SPICE(REPORTTOOWIDE)": SpiceREPORTTOOWIDE,
    "SPICE(REQUESTOUTOFBOUNDS)": SpiceREQUESTOUTOFBOUNDS,
    "SPICE(REQUESTOUTOFORDER)": SpiceREQUESTOUTOFORDER,
    "SPICE(RWCONFLICT)": SpiceRWCONFLICT,
    "SPICE(SAMEBODY1CENTER1)":SpiceSAMEBODY1CENTER1,
    "SPICE(SAMEBODY1CENTER2)":SpiceSAMEBODY1CENTER2,
    "SPICE(SAMEBODY2CENTER1)":SpiceSAMEBODY2CENTER1,
    "SPICE(SAMEBODY2CENTER2)":SpiceSAMEBODY2CENTER2,
    "SPICE(SAMEBODYANDCENTER3)":SpiceSAMEBODYANDCENTER3,
    "SPICE(SAMEBODYANDCENTER4)":SpiceSAMEBODYANDCENTER4,
    "SPICE(SBINSUFPTRSIZE)": SpiceSBINSUFPTRSIZE,
    "SPICE(SBTOOMANYSTRS)": SpiceSBTOOMANYSTRS,
    "SPICE(SCLKDOESNTEXIST)": SpiceSCLKDOESNTEXIST,
    "SPICE(SEGMENTNOTFOUND)": SpiceSEGMENTNOTFOUND,
    "SPICE(SEGMENTTABLEFULL)": SpiceSEGMENTTABLEFULL,
    "SPICE(SEGTABLETOOSMALL)": SpiceSEGTABLETOOSMALL,
    "SPICE(SEGTYPECONFLICT)": SpiceSEGTYPECONFLICT,
    "SPICE(SETTOOSMALL)": SpiceSETTOOSMALL,
    "SPICE(SETUPDOESNOTEXIST)": SpiceSETUPDOESNOTEXIST,
    "SPICE(SIZEMISMATCH)": SpiceSIZEMISMATCH,
    "SPICE(SIZEOUTOFRANGE)": SpiceSIZEOUTOFRANGE,
    "SPICE(SPACETOONARROW)": SpiceSPACETOONARROW,
    "SPICE(SPCRFLNOTCALLED)": SpiceSPCRFLNOTCALLED,
    "SPICE(SPICEISTIRED)": SpiceSPICEISTIRED,
    "SPICE(SPKDIFFBUG1)":SpiceSPKDIFFBUG1,
    "SPICE(SPKDIFFBUG10)":SpiceSPKDIFFBUG10,
    "SPICE(SPKDIFFBUG11)":SpiceSPKDIFFBUG11,
    "SPICE(SPKDIFFBUG12)":SpiceSPKDIFFBUG12,
    "SPICE(SPKDIFFBUG2)":SpiceSPKDIFFBUG2,
    "SPICE(SPKDIFFBUG3)":SpiceSPKDIFFBUG3,
    "SPICE(SPKDIFFBUG5)":SpiceSPKDIFFBUG5,
    "SPICE(SPKDIFFBUG6)":SpiceSPKDIFFBUG6,
    "SPICE(SPKDIFFBUG7)":SpiceSPKDIFFBUG7,
    "SPICE(SPKDIFFBUG8)":SpiceSPKDIFFBUG8,
    "SPICE(SPKDIFFBUG9)":SpiceSPKDIFFBUG9,
    "SPICE(SPKDOESNTEXIST)": SpiceSPKDOESNTEXIST,
    "SPICE(SPKFILE)": SpiceSPKFILE,
    "SPICE(SPKRECTOOLARGE)": SpiceSPKRECTOOLARGE,
    "SPICE(SPKREFNOTSUPP)": SpiceSPKREFNOTSUPP,
    "SPICE(SPKSTRUCTUREERROR)": SpiceSPKSTRUCTUREERROR,
    "SPICE(SPKTYPENOTSUPPORTD)": SpiceSPKTYPENOTSUPPORTD,
    "SPICE(SPURIOUSFLAG)": SpiceSPURIOUSFLAG,
    "SPICE(SPURIOUSKEYWORD)": SpiceSPURIOUSKEYWORD,
    "SPICE(STEPTOOSMALL1)":SpiceSTEPTOOSMALL1,
    "SPICE(STEPTOOSMALL2)":SpiceSTEPTOOSMALL2,
    "SPICE(STFULL)": SpiceSTFULL,
    "SPICE(STRINGCONVERROR)": SpiceSTRINGCONVERROR,
    "SPICE(STRINGCOPYFAIL)": SpiceSTRINGCOPYFAIL,
    "SPICE(STRINGCREATEFAIL)": SpiceSTRINGCREATEFAIL,
    "SPICE(STRINGTOOSMALL)": SpiceSTRINGTOOSMALL,
    "SPICE(STRINGTRUNCATED)": SpiceSTRINGTRUNCATED,
    "SPICE(SUBORBITAL)": SpiceSUBORBITAL,
    "SPICE(SYNTAXERROR)": SpiceSYNTAXERROR,
    "SPICE(SYSTEMCALLFAILED)": SpiceSYSTEMCALLFAILED,
    "SPICE(TARGIDCODENOTFOUND)": SpiceTARGIDCODENOTFOUND,
    "SPICE(TIMEOUTOFBOUNDS)": SpiceTIMEOUTOFBOUNDS,
    "SPICE(TIMESYSTEMPROBLEM)": SpiceTIMESYSTEMPROBLEM,
    "SPICE(TIMEZONEERROR)": SpiceTIMEZONEERROR,
    "SPICE(TOOFEWINPUTLINES)": SpiceTOOFEWINPUTLINES,
    "SPICE(TOOFEWWINDOWS)": SpiceTOOFEWWINDOWS,
    "SPICE(TOOMANYBASEFRAMES)": SpiceTOOMANYBASEFRAMES,
    "SPICE(TOOMANYCOLUMNS)": SpiceTOOMANYCOLUMNS,
    "SPICE(TOOMANYFIELDS)": SpiceTOOMANYFIELDS,
    "SPICE(TOOMANYHITS)": SpiceTOOMANYHITS,
    "SPICE(TOOMANYITERATIONS)": SpiceTOOMANYITERATIONS,
    "SPICE(TOOMANYKEYWORDS)": SpiceTOOMANYKEYWORDS,
    "SPICE(TOOMANYPAIRS)": SpiceTOOMANYPAIRS,
    "SPICE(TOOMANYPEAS)": SpiceTOOMANYPEAS,
    "SPICE(TOOMANYPLATES)": SpiceTOOMANYPLATES,
    "SPICE(TOOMANYSURFACES)": SpiceTOOMANYSURFACES,
    "SPICE(TOOMANYVERTICES)": SpiceTOOMANYVERTICES,
    "SPICE(TOOMANYWATCHES)": SpiceTOOMANYWATCHES,
    "SPICE(TRANSFERFILE)": SpiceTRANSFERFILE,
    "SPICE(TRANSFERFORMAT)": SpiceTRANSFERFORMAT,
    "SPICE(TWOSCLKFILENAMES)": SpiceTWOSCLKFILENAMES,
    "SPICE(TYPE1TEXTEK)":SpiceTYPE1TEXTEK,
    "SPICE(TYPENOTSUPPORTED)": SpiceTYPENOTSUPPORTED,
    "SPICE(TYPESMISMATCH)": SpiceTYPESMISMATCH,
    "SPICE(UNALLOCATEDNODE)": SpiceUNALLOCATEDNODE,
    "SPICE(UNBALACEDPAIR)": SpiceUNBALACEDPAIR,
    "SPICE(UNBALANCEDGROUP)": SpiceUNBALANCEDGROUP,
    "SPICE(UNBALANCEDPAIR)": SpiceUNBALANCEDPAIR,
    "SPICE(UNEQUALTIMESTEP)": SpiceUNEQUALTIMESTEP,
    "SPICE(UNINITIALIZED)": SpiceUNINITIALIZED,
    "SPICE(UNINITIALIZEDHASH)": SpiceUNINITIALIZEDHASH,
    "SPICE(UNINITIALIZEDVALUE)": SpiceUNINITIALIZEDVALUE,
    "SPICE(UNKNONWNTIMESYSTEM)": SpiceUNKNONWNTIMESYSTEM,
    "SPICE(UNKNOWNBFF)": SpiceUNKNOWNBFF,
    "SPICE(UNKNOWNCKMETA)": SpiceUNKNOWNCKMETA,
    "SPICE(UNKNOWNDATATYPE)": SpiceUNKNOWNDATATYPE,
    "SPICE(UNKNOWNFILARC)": SpiceUNKNOWNFILARC,
    "SPICE(UNKNOWNFRAME2)":SpiceUNKNOWNFRAME2,
    "SPICE(UNKNOWNFRAMESPEC)": SpiceUNKNOWNFRAMESPEC,
    "SPICE(UNKNOWNFRAMETYPE)": SpiceUNKNOWNFRAMETYPE,
    "SPICE(UNKNOWNID)": SpiceUNKNOWNID,
    "SPICE(UNKNOWNINCLUSION)": SpiceUNKNOWNINCLUSION,
    "SPICE(UNKNOWNINDEXTYPE)": SpiceUNKNOWNINDEXTYPE,
    "SPICE(UNKNOWNKERNELTYPE)": SpiceUNKNOWNKERNELTYPE,
    "SPICE(UNKNOWNKEY)": SpiceUNKNOWNKEY,
    "SPICE(UNKNOWNMETAITEM)": SpiceUNKNOWNMETAITEM,
    "SPICE(UNKNOWNMODE)": SpiceUNKNOWNMODE,
    "SPICE(UNKNOWNOP)": SpiceUNKNOWNOP,
    "SPICE(UNKNOWNPACKETDIR)": SpiceUNKNOWNPACKETDIR,
    "SPICE(UNKNOWNPCKTYPE)": SpiceUNKNOWNPCKTYPE,
    "SPICE(UNKNOWNREFDIR)": SpiceUNKNOWNREFDIR,
    "SPICE(UNKNOWNTYPE)": SpiceUNKNOWNTYPE,
    "SPICE(UNKNOWNUNITS)": SpiceUNKNOWNUNITS,
    "SPICE(UNNATURALACT)": SpiceUNNATURALACT,
    "SPICE(UNNATURALRELATION)": SpiceUNNATURALRELATION,
    "SPICE(UNORDEREDREFS)": SpiceUNORDEREDREFS,
    "SPICE(UNPARSEDQUERY)": SpiceUNPARSEDQUERY,
    "SPICE(UNRECOGNAPPFLAG)": SpiceUNRECOGNAPPFLAG,
    "SPICE(UNRECOGNDATATYPE)": SpiceUNRECOGNDATATYPE,
    "SPICE(UNRECOGNDELIMITER)": SpiceUNRECOGNDELIMITER,
    "SPICE(UNRECOGNIZABLEFILE)": SpiceUNRECOGNIZABLEFILE,
    "SPICE(UNRECOGNIZEDACTION)": SpiceUNRECOGNIZEDACTION,
    "SPICE(UNRECOGNIZEDFORMAT)": SpiceUNRECOGNIZEDFORMAT,
    "SPICE(UNRECOGNIZEDFRAME)": SpiceUNRECOGNIZEDFRAME,
    "SPICE(UNRECOGNIZEDTYPE)": SpiceUNRECOGNIZEDTYPE,
    "SPICE(UNRECOGNPRECTYPE)": SpiceUNRECOGNPRECTYPE,
    "SPICE(UNRESOLVEDNAMES)": SpiceUNRESOLVEDNAMES,
    "SPICE(UNRESOLVEDTIMES)": SpiceUNRESOLVEDTIMES,
    "SPICE(UNSUPPBINARYARCH)": SpiceUNSUPPBINARYARCH,
    "SPICE(UNSUPPORTEDARCH)": SpiceUNSUPPORTEDARCH,
    "SPICE(UNSUPPORTEDMETHOD)": SpiceUNSUPPORTEDMETHOD,
    "SPICE(UNSUPPTEXTFORMAT)": SpiceUNSUPPTEXTFORMAT,
    "SPICE(UNTITLEDHELP)": SpiceUNTITLEDHELP,
    "SPICE(UPDATEPENDING)": SpiceUPDATEPENDING,
    "SPICE(USAGEERROR)": SpiceUSAGEERROR,
    "SPICE(UTFULL)": SpiceUTFULL,
    "SPICE(VALUETABLEFULL)": SpiceVALUETABLEFULL,
    "SPICE(VARNAMETOOLONG)": SpiceVARNAMETOOLONG,
    "SPICE(VERSIONMISMATCH)": SpiceVERSIONMISMATCH,
    "SPICE(VERSIONMISMATCH1)":SpiceVERSIONMISMATCH1,
    "SPICE(VERSIONMISMATCH2)":SpiceVERSIONMISMATCH2,
    "SPICE(VERTEXNOTINGRID)": SpiceVERTEXNOTINGRID,
    "SPICE(VOXELGRIDTOOBIG)": SpiceVOXELGRIDTOOBIG,
    "SPICE(WIDTHTOOSMALL)": SpiceWIDTHTOOSMALL,
    "SPICE(WINDOWSTOOSMALL)": SpiceWINDOWSTOOSMALL,
    "SPICE(WRITEERROR)": SpiceWRITEERROR,
    "SPICE(WRITEFAILED)": SpiceWRITEFAILED,
    "SPICE(WRONGARCHITECTURE)": SpiceWRONGARCHITECTURE,
    "SPICE(WRONGCKTYPE)": SpiceWRONGCKTYPE,
    "SPICE(WRONGCONIC)": SpiceWRONGCONIC,
    "SPICE(WRONGSEGMENT)": SpiceWRONGSEGMENT,
    "SPICE(WRONGSPKTYPE)": SpiceWRONGSPKTYPE,
    "SPICE(YEAROUTOFBOUNDS)": SpiceYEAROUTOFBOUNDS,
    "SPICE(ZEROAXISLENGTH)": SpiceZEROAXISLENGTH,
    "SPICE(ZEROBORESIGHT)": SpiceZEROBORESIGHT,
    "SPICE(ZEROFRAMEID)": SpiceZEROFRAMEID,
    "SPICE(ZERORADIUS)": SpiceZERORADIUS,
    "SPICE(ZEROSTEP)": SpiceZEROSTEP,
    "SPICE(ZZHOLDDGETFAILED)": SpiceZZHOLDDGETFAILED,
    "SPICE(ZZHOLDNOPUT)": SpiceZZHOLDNOPUT,
}


def short_to_spiceypy_exception_class(short: str) -> Type[SpiceyError]:
    """
    Lookup the correct Spice Exception class

    :param short: Spice error system short description key
    :return: SpiceyError
    """
    return exceptions.get(short, SpiceyError)


def dynamically_instantiate_spiceyerror(
    short: str = "",
    explain: str = "",
    long: str = "",
    traceback: str = "",
    found: str = "",
):
    """
    Dynamically creates a SpiceyPyException which is a subclass of SpiceyError and
    may also be subclassed to other exceptions such as IOError and such depending on the Short description

    :param short:
    :param explain:
    :param long:
    :param traceback:
    :param found:
    :return:
    """
    base_exception = short_to_spiceypy_exception_class(short)
    return base_exception(
        short=short, explain=explain, long=long, traceback=traceback, found=found
    )
