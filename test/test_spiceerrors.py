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


def test_getspiceyexception():
    with pytest.raises(spice.stypes.SpiceyError):
        spice.furnsh(os.path.join(cwd,"_null_kernel.txt"))