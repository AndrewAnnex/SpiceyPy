__author__ = 'AndrewAnnex'
import pytest
import spiceypy as spice
import os
cwd = os.path.realpath(os.path.dirname(__file__))


def test_geterror():
    spice.setmsg("some error occured")
    spice.sigerr("error")
    assert spice.failed()
    assert spice.getmsg("SHORT", 40) == "error"
    assert spice.getmsg("LONG", 200) == "some error occured"


def test_getSpiceyException():
    with pytest.raises(spice.stypes.SpiceyError):
        spice.furnsh(os.path.join(cwd, "_null_kernel.txt"))


def test_emptyKernelPoolException():
    with pytest.raises(spice.stypes.SpiceyError):
        spice.ckgp(0, 0, 0, "blah")


def test_foundErrorChecker():
    with pytest.raises(spice.stypes.SpiceyError):
        spice.bodc2n(-9991)

