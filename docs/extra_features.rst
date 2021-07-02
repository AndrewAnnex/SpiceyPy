Extra Features
==============

July 2, 2021

SpiceyPy was always intended to be a thin wrapper around the CSPICE routines, however
as it is implemented in Python there are a small number of extra features to help
make end-users' code more Pythonic.

Overview
--------

These tasks teach basic substitutions and code idioms that can be included in code to
make it easier to read in Python, and less error-prone.

Lesson 1: Loading Kernels as Contexts
-------------------------------------

Task Statement
^^^^^^^^^^^^^^
Write a program which loads kernels using a context manager. Then, load kernels using a
function decorator.

Learning Goals
^^^^^^^^^^^^^^
SpiceyPy includes a context manager which can load kernels and guarantees that they will
be unloaded when they're finished with, which can also be used as a decorator.

Code Solution
^^^^^^^^^^^^^

::

    import spiceypy
    from spiceypy.context import SpiceKernel


    # This is an example of a function which uses the context manager SpiceKernel. It only
    # loads the kernel within the "with" statement, then unloads it, and if an error happens
    # in it all the kernels are unloaded properly. It's good practice to only keep the
    # kernels loaded for as long as necessary.
    def get_time_using_context_manager():
        """Gets the user to input a time and converts it to an Ephemeris Time (ET)."""

        # This could be calculated by some other routine.
        utc = input("Enter a time in UTC: ")

        # Load the kernel, and only keep it loaded for as long as needed.
        with SpiceKernel("win.tm"):
            et = spiceypy.str2et(utc)

        # Now print the ET, although this could be any other operation.
        print("UTC {0} corresponds to ET {1}".format(utc, et))


    # Alternatively, the SpiceKernel can be used as a decorator for cases where the entire
    # function needs to be executed with the kernel.
    @SpiceKernel("win.tm")
    def get_time_using_decorator(utc):
        """Converts a given UTC string to Ephemeris Time (ET)."""

        # Do the conversion. Because of the @SpiceKernel decorator, no kernels need to be
        # loaded or unloaded.
        et = spiceypy.str2et(utc)

        # Print the ET, could be any other operation. If the function ends with a return,
        # the kernels are unloaded AFTER the return value is calculated (so you could
        # have, for example, "return spiceypy.str2et(utc)".
        print("UTC {0} corresponds to ET {1}".format(utc, et))
