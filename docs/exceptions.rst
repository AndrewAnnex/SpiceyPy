Exceptions in SpiceyPy
======================

SpiceyPy by default checks the spice error system for errors after all function
calls and will raise an exception containing the error information when the spice indicates an error has occurred.

Exception Hierarchy Basics
--------------------------

SpiceyPy exceptions are all based on the :py:exc:`spiceypy.utils.exceptions.SpiceyError` exception.
SpiceyError is subclassed by :py:exc:`spiceypy.utils.exceptions.SpiceyPyError` to present a more consistent exception class for the user.
SpiceyPyError is subclassed by a number of exceptions that also inherit from some of the common builtin Python exceptions:

.. inheritance-diagram:: spiceypy.utils.exceptions.NotFoundError spiceypy.utils.exceptions.SpiceyPyIOError spiceypy.utils.exceptions.SpiceyPyMemoryError spiceypy.utils.exceptions.SpiceyPyTypeError spiceypy.utils.exceptions.SpiceyPyKeyError spiceypy.utils.exceptions.SpiceyPyIndexError spiceypy.utils.exceptions.SpiceyPyRuntimeError spiceypy.utils.exceptions.SpiceyPyValueError spiceypy.utils.exceptions.SpiceyPyZeroDivisionError
   :top-classes: spiceypy.utils.exceptions.SpiceyError spiceypy.utils.exceptions.SpiceyPyError

Spice defines hundreds of errors in the format "SPICE(ERROR_NAME)" which are also included in SpiceyPy by a slightly different naming convention,
where a Spice error "SPICE(QUERYFAILURE)" will correspond to the SpiceyPy exception :py:exc:`spiceypy.utils.exceptions.SpiceQUERYFAILURE`.

These errors will inherit the appropriate parent SpiceyPyError with builtin exception mix-in if the correct corresponding exception type is known.
For example, :py:exc:`spiceypy.utils.exceptions.SpiceDIVIDEBYZERO` is a subclass of the :py:exc:`spiceypy.utils.exceptions.SpiceyPyZeroDivisionError`.

:py:exc:`spiceypy.utils.exceptions.SpiceyPyZeroDivisionError` in turn, is a subclass of :py:exc:`spiceypy.utils.exceptions.SpiceyPyError` and the built in :py:exc:`ZeroDivisionError`.

By subclassing the errors in this way, users can tune how granular their exception handling code will respond.
For most users the top level SpiceyError and SpiceyPyError will be sufficient for their needs.

Exception Contents
------------------

The exception message is a string that follows the format used elsewhere in spice and
includes the toolkit version, the short description, explanation, long format description,
and traceback (of spice calls). `Read the NAIF tutorial on exceptions here. <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Tutorials/pdf/individual_docs/32_exceptions.pdf>`_
These values are stored in parameters of the exception object.

Here is an example of the exception message text:

.. code:: python

    spice.furnsh("/tmp/_null_kernel.txt")

will result in the following exception message which is also a parameter of the exception object.

.. code-block:: text

    ================================================================================

    Toolkit version: CSPICE66

    SPICE(NOSUCHFILE) --

    The attempt to load "/tmp/_null_kernel.txt" by the routine FURNSH failed. It could not be located.

    furnsh_c --> FURNSH --> ZZLDKER

    ================================================================================

SpiceyErrors, SpiceyPyErrors, and all subclasses of SpiceyPyErrors contain the following parameters that the user can access:

1. tkvsn, the toolkit version of cspice used for example: "CSPICE66".

2. short, the short error description which is the same as the granular exception object type when possible, for example: "SPICE(NOSUCHFILE)".

3. explain, if present is the explanation from spice for the error.

4. long, the long error message description from spice, for example: "The attempt to load "/tmp/_null_kernel.txt" by the routine FURNSH failed. It could not be located."

5. traceback, sequence of calls within spice leading to the error, for example: "furnsh_c --> FURNSH --> ZZLDKER".

6. message, the full exception message following the spice template from the example above.


Not Found Errors
----------------

Also, by default SpiceyPy captures the 'found' flags some functions return as it is not
idiomatic to python as a :py:exc:`spiceypy.utils.exceptions.NotFoundError` . This can be temporarily disabled using
the :py:meth:`spiceypy.spiceypy.no_found_check` context manager that allows the found
flag to be returned to the user for action. Outside of that context SpiceyPy functions will revert to default behavior. For vectorized
functions, the found parameter of the exception will contain an iterable of the found flags to help track down failed calls.

.. code:: python

    import spiceypy as spice

    spice.bodc2n(-9991) # will raise an exception

    with spice.no_found_check():
        name, found = spice.bodc2n(-9991) # found is now available, no exception raised!
        assert not found # found is going to be False in this case.

    spice.bodc2n(-9991) # will raise an exception again

There is also an accompanying context manager for enabling the default SpiceyPy behavior within a code block like so:

.. code:: python

    import spiceypy as spice

    spice.bodc2n(-9991) # will raise an exception

    with spice.found_check():
        name = spice.bodc2n(-9991) # will also raise an exception


In addition, for advanced users there are two function :py:meth:`spiceypy.spiceypy.found_check_off` and :py:meth:`spiceypy.spiceypy.found_check_on`
which will disable and enable the behavior without use of the context manager. Additionally, a method :py:meth:`spiceypy.spiceypy.get_found_catch_state` allows users
to query the current state of found flag catching setting.
