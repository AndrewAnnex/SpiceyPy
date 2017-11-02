Basics of SpiceyPy
==================

Environment Set-up
------------------

Follow the installation instructions provided in :ref:`installation`.

Confirm SpiceyPy installation
-----------------------------

There are multiple ways to verify your SpiceyPy installation. The first test
is to simply run

::

    pip list

You should see SpiceyPy in the list of your installed packages. If SpiceyPy
is not present in the list then a configuration issue in your environment
caused SpiceyPy to be installed in a non-standard way. Note this is an error
prone to systems with multiple installed python versions.

If SpiceyPy is present in the pip list, then SpiceyPy is installed. Another
verification step is within the python REPL run:

.. code:: python

    import spiceypy as spice


The version of the installed cspice toolkit (note: not SpiceyPy's version)
should be printed out. Otherwise the Python interpreter should output an
explanitory error message.


A simple example program
------------------------

The following calls the SPICE function :py:meth:`spiceypy.spiceypy.tkvrsn` which outputs the version
of cspice that SpiceyPy is wrapping.

.. code:: python

    import spiceypy as spice

    spice.tkvrsn('TOOLKIT')

This should output the following string:

.. parsed-literal::

    'CSPICE_N0066'


Exceptions
----------

SpiceyPy by default checks the spice error system for errors after all function
calls and will raise SpiceyErrors (a python exception) when spice indicates an error.
The exception message is a string that follows the format used elsewhere in spice and
includes the toolkit version, the short description, explanation, long format description,
and traceback (of spice calls). `Read the NAIF tutorial on exceptions here. <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Tutorials/pdf/individual_docs/32_exceptions.pdf>`_

Also, by default SpiceyPy captures the 'found' flags some functions return as it is not
idiomatic to python and instead through a SpiceyError exception. This can be temporarily disabled using
the :py:meth:`spiceypy.spiceypy.disable_found_catch` context manager that allows the found
flag to be returned to the user for action. Outside the context SpiceyPy functions will revert to default behavior.

.. code:: python

    import spiceypy as spice

    spice.bodc2n(-9991) # will raise an exception

    with spice.disable_found_catch():
        name, found = spice.bodc2n(-9991) # found is now available, no exception raised!
        assert not found # found is going to be False.

    spice.bodc2n(-9991) # will raise an exception again
