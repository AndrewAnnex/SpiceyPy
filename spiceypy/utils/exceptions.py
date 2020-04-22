"""
The MIT License (MIT)

Copyright (c) [2015-2020] [Andrew Annex]

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
    SpiceyError wraps CSPICE errors.
    """

    def __init__(
        self,
        short: str = "",
        explain: str = "",
        long: str = "",
        traceback: str = "",
        found: str = "",
    ):
        self.tkvsn = "CSPICE66"
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
    Thin exception for backwards compatibility with future exception types

    In SpiceyPy versions 3.0.2 and prior, the base exception was a SpiceyError
    SpiceyPyError is a slightly more verbose error name.
    """

    pass


class NotFoundError(SpiceyPyError):
    """
    A NotFound Error for Spice
    """

    def __init__(self, message=None, found: bool = False):
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
}
