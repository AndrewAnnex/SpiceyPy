import pytest

import spiceypy as spice


@pytest.fixture(scope="session", autouse=True)
def trcoff_after_all_tests():
    # trcoff permanently disables SPICE call tracing for the process, so it is
    # checked once after every test in the session has run; doing it in any
    # module teardown would break trace-dependent tests (qcktrc, trcdep, ...)
    # that a random test order schedules after that module
    yield
    spice.reset()
    # Initialize stack trace with two values, and test
    spice.chkin("A")
    spice.chkin("B")
    assert 2 == spice.trcdep()
    assert "B" == spice.trcnam(1)
    assert "A" == spice.trcnam(0)
    # Turn off tracing and test
    spice.trcoff()
    assert 0 == spice.trcdep()
    assert "" == spice.qcktrc(2)
    # Ensure subsequent checkins are also ignored
    spice.chkin("C")
    assert 0 == spice.trcdep()
    spice.reset()
