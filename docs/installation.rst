============
Installation
============

SpiceyPy is currently supported on Mac, Linux, FreeBSD, and Windows systems.

.. _installation:

If you are new to python, it is a good idea to read a bit about it first
`<https://docs.python-guide.org>`_.  For new installations of python, it is
encouraged to install and or update: pip, setuptools, wheel, and numpy first
before installing SpiceyPy ::

    pip install -U pip setuptools
    pip install -U numpy

Then to install SpiceyPy, simply run::

    pip install spiceypy

If you use anaconda/miniconda/conda/mamba/micromamba run:
---------------------------------------------------------
::

    conda config --add channels conda-forge
    conda install spiceypy
    

Using the appropriate "conda" or "mamba" or "micromamba" command.

If no error was returned you have successfully installed SpiceyPy.
To verify this you can list the installed packages via this pip command::

    pip list

You should see spiceypy in the output of this command.
Or you can start a python interpreter and try importing SpiceyPy like so:

.. code:: python

    import spiceypy

    # print out the toolkit version installed
    print(spiceypy.tkvrsn('TOOLKIT'))

This should print out the toolkit version without any errors. You have now
verified that SpiceyPy is installed.

Using a system or custom CSPICE (source builds)
-----------------------------------------------

Since version 7.0.0 SpiceyPy is built with CMake (scikit-build-core). When building
from source (``pip install .`` in a clone of the repository), CSPICE is located in
this order:

1. ``SPICEYPY_CSPICE_PREFIX`` (environment variable or CMake define): an install
   prefix containing a CSPICE built with
   `cspice-cmake-spiceypy <https://github.com/AndrewAnnex/cspice-cmake-spiceypy>`_.
   The shared library is bundled into the built package.
2. A system or conda CSPICE found via ``find_library``, with headers (``SpiceUsr.h``)
   findable on the default paths (e.g. ``include/cspice/``). Used as-is, not bundled.
3. Otherwise CSPICE is downloaded and compiled from source automatically via the
   cspice-cmake-spiceypy recipe, and the shared library is bundled into the package.

To build a reusable CSPICE prefix (option 1) from a SpiceyPy clone:

.. code-block:: bash

    cmake -S . -B build-cspice -DSPICEYPY_CSPICE_ONLY=ON -DCMAKE_BUILD_TYPE=Release
    cmake --build build-cspice
    cmake --install build-cspice --prefix /tmp/cspice-prefix
    SPICEYPY_CSPICE_PREFIX=/tmp/cspice-prefix pip install .

CMake options can be passed through pip in several equivalent ways:

.. code-block:: bash

    # scikit-build-core config-setting
    pip install . -C cmake.define.SPICEYPY_CSPICE_PREFIX=/tmp/cspice-prefix
    # environment variable form of the same (";"-separated NAME=VALUE list)
    SKBUILD_CMAKE_DEFINE="SPICEYPY_CSPICE_PREFIX=/tmp/cspice-prefix" pip install .
    # raw CMake arguments (space-separated), also reaches recipe options
    CMAKE_ARGS="-DCSPICE_PATCH_SOURCE=OFF" pip install .

``CMAKE_PREFIX_PATH`` is honored as well: a CSPICE installed under a
non-standard prefix (e.g. ``CMAKE_PREFIX_PATH=/tmp/mycspice``) is found by the
system search (option 2 above) — and, unlike ``SPICEYPY_CSPICE_PREFIX``, used
in place without being bundled into the package.

The cspice-cmake-spiceypy recipe (used by options 1 and 3) exposes a few options of
its own, which flow through a ``pip install .``:

* ``CSPICE_SRC`` (environment variable): path to a local extracted CSPICE toolkit
  source tree to use instead of downloading from NAIF. It is copied into the build
  tree before patching; your copy is never modified.
* ``CSPICE_PATCH_SOURCE`` (CMake option or environment variable, default ``ON``):
  apply SpiceyPy-specific patches to the working copy. Set to ``OFF`` if supplying
  an already-patched ``CSPICE_SRC``.
* ``BUILD_EXECUTABLES`` / ``BUILD_TESTING`` (default ``OFF``): additionally build the
  CSPICE utility executables / the recipe's C test.

Offline installation
--------------------

A from-source build normally downloads two things: the cspice-cmake-spiceypy recipe
(via git) and the CSPICE toolkit archive (from NAIF). To install without a network,
either use a system CSPICE or a prebuilt ``SPICEYPY_CSPICE_PREFIX`` prefix (see
above), so that neither download occurs, or point the build at local copies of both:

.. code-block:: bash

    export CSPICE_SRC="/tmp/cspice"  # extracted CSPICE toolkit source tree
    pip install . -C cmake.args=-DFETCHCONTENT_SOURCE_DIR_CSPICE=/path/to/cspice-cmake-spiceypy

.. note::
    The build-time ``CSPICE_SRC_DIR`` and ``CSPICE_SHARED_LIB`` environment variables
    from the pre-7.0.0 build system are no longer used.

Runtime library selection
-------------------------

At import time SpiceyPy loads the first CSPICE shared library found from:

1. The ``CSPICE_SHARED_LIB`` environment variable (full path to the library).
2. A system or conda library found by ``ctypes.util.find_library("cspice")`` —
   note this takes precedence over the library bundled in the wheel. On Linux,
   directories on ``LD_LIBRARY_PATH`` (set before launching Python) are searched
   here too, though ``CSPICE_SHARED_LIB`` is the more reliable override.
3. The bundled library next to the package (``spiceypy/utils/``).

Set ``SPICEYPY_LOGLEVEL=INFO`` before importing spiceypy to log which library was
loaded.

A simple example program
------------------------

This script calls the spiceypy function 'tkvrsn' and outputs the return
value.

.. code-block:: python

              File tkvrsn.py

                 import spiceypy

                 def print_ver():
                         """
                         Prints the TOOLKIT version
                         """
                         print(spiceypy.tkvrsn('TOOLKIT'))

                 if __name__ == '__main__':
                        print_ver()

From the command line, execute the function:

::

              $ python tkvrsn.py
              CSPICE_N0067

From Python, execute the function:

::

              $ python
              >>> import tkvrsn
              >>> tkvrsn.print_ver()
              CSPICE_N0067

SpiceyPy Documentation
----------------------

The current version of SpiceyPy does not provide extensive
documentation, but there are several ways to navigate your way through
the Python version of the toolkit. One simple way is to use the standard
Python mechanisms. All interfaces implemented in SpiceyPy can be listed
using the standard built-in function dir(), which returns an
alphabetized list of names comprising (among) other things, the API
names. If you need to get additional information about an API
parameters, the standard built-in function help() could be used:

::

      >>> import spiceypy
      >>> help(spiceypy.tkvrsn)

which produces

.. code-block:: text

      Help on function tkvrsn in module spiceypy.spiceypy:

      tkvrsn(item: str) -> str
          Given an item such as the Toolkit or an entry point name, return
          the latest version string.

          https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/tkvrsn_c.html

          :param item: Item for which a version string is desired.
          :return: the latest version string.

As indicated in the help on the function, the complete documentation is
available on the CSPICE toolkit version. Therefore it is recommended to
have the CSPICE toolkit version installed locally in order to access its
documentation offline.


=============
Common Issues
=============

SSL Alert Handshake Issue
-------------------------

.. attention::

    As of 2020, users are not likely to experience this issue with python
    version 3.7 and above, and for newer 3.6.X releases. Users running
    older operating systems are encouraged to update to newer versions
    of python if they are attempting to install version 3.0.0 or above.
    See other sections of this document for more information.


In early 2017, JPL updated to a TLS1.2 certificate and enforced https connections causing installation
issues for users, in particular for macOS users, with OpenSSL versions older
than 1.0.1g. This is because older versions of OpenSSL still distributed in some
environments which are incompatible with TLS1.2. As of late 2017 SpiceyPy has been updated with
a strategy that can mitigate this issue on some systems, but it may not be totally reliable due to known deficiencies in setuptools and pip.

Another solution is to configure a new python installation that is linked against a newer version
of OpenSSL, the easiest way to do this is to install python using homebrew, once this is done spiceypy
can be installed to this new installation of python (IMHO this is the best option).

If your python 3.6 distribution was installed from the packages available at python.org an included command
"Install Certificates.command" should be run before attempting to install SpiceyPy again.
That command installs the certifi package that can also be install using pip.

Alternatively, installing an anaconda or miniconda
python distribution and installing SpiceyPy using the conda command above is another possible work around.

Users continuing to have issues should report an issue to the github repository.

Supporting links:

* `<https://bugs.python.org/issue29065>`_
* `<https://github.com/psf/requests/issues/2022>`_
* `<https://pyfound.blogspot.com/2017/01/time-to-upgrade-your-python-tls-v12.html>`_
* `<https://www.python.org/dev/peps/pep-0518>`_
* `<https://github.com/AndrewAnnex/SpiceyPy/pull/202>`_

======================================================
How to install from source (for bleeding edge updates)
======================================================

.. attention::

    If you have used the pip or conda install commands above you do not
    need to do any of the following commands. Installing from source is intended
    for advanced users. Users on machines running Windows should take note
    that attempting to install from source will require software
    such as visual studio, CMake, and additional environment configuration. Given
    the complexity of this Windows users are highly encouraged to stick
    with the releases made available through PyPi/Conda-Forge.


If you wish to install from source, first simply clone the repository by
running the following in your favorite shell::

    git clone https://github.com/AndrewAnnex/SpiceyPy.git

If you do not have git, you can also directly download
the source code from the GitHub repo for SpiceyPy at
`https://github.com/AndrewAnnex/SpiceyPy <https://github.com/AndrewAnnex/SpiceyPy>`_

To install the library, simply change into the root
directory of the project and then run::

    pip install .

The build will locate or build CSPICE as described in
`Using a system or custom CSPICE (source builds)`_ above
(downloading and compiling it from source if none is found)
and install SpiceyPy into your site-packages directory.
Building from source requires CMake and a C compiler;
Cython and NumPy are handled automatically by build
isolation.
