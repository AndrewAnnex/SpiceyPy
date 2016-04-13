Basics of SpiceyPy
==================

Environment Set-up
------------------

Follow the installation instructions provided.


Confirm SpiceyPy installation
-----------------------------

There are multiple ways to verify your SpiceyPy installation. The first test
is to simply run

::

    pip list

You should see spiceypy in the list of your installed packages. If spiceypy
is not present in the list then a configuration issue in your environment
caused spiceypy to be installed in a non-standard way. Note this is an error
prone to systems with multiple installed python versions.

If spiceypy is present in the pip list, then spiceypy is installed. Another
verification step is within the python REPL run:

.. code:: python

    import spiceypy as spice


The version of the installed cspice toolkit (note: not SpiceyPy's version)
should be printed out. Otherwise the Python interpreter should output an
explanitory error message.


A simple example program
------------------------

The following calls the SPICE function ``tkvrsn`` which outputs the version
of cspice that SpiceyPy is wrapping.

.. code:: python

    import spiceypy as spice

    spice.tkvrsn('TOOLKIT')

This should output the following string:

.. parsed-literal::

    'CSPICE_N0065'
