Multithreading in SpiceyPy
======================

SpiceyPy by default enable a semaphore to avoid a cuncurrent call to the SpiceyPy functions.

This semaphore system is intended to avoind a cuncurrent call to the kernel from different threads that could make fail
the called routine (e.g. 2 cuncurrent calls to 'spkezr' may fail into a DAF error due to spice internal errors)

The handling of multiprocesses is not the scope of this feature.

Occasionaly Enabling Multithreading
----------------

In order to activate the multithreading feature only when it is required, it is possible to disable the default behavior and use 
the provided SpiceyPy function that returns the context manager to be used only where the feature is 

.. code:: python

    import spiceypy as spice 

    spice.threading_lock_on() # the SpiceyPy multithread handler is disabled

    
    with spice.threading_lock(): # the SpiceyPy multithread handler is enabled 
        ...
        # do stuff with multithread

    # the SpiceyPy multithread handler is disabled again
