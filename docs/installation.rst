============
Installation
============

SpiceyPy is currently supported on Mac, Linux, FreeBSD, and Windows systems.

.. _installation:

If you are new to python, it is a good idea to read a bit about it first
`<https://docs.python-guide.org>`_.  For new installations of python, it is
encouraged to install and or update: pip, setuptools, wheel, and numpy first
before installing SpiceyPy ::

    pip install -U pip setuptools wheel
    pip install -U numpy

Then to install SpiceyPy, simply run::

    pip install spiceypy

If you use anaconda/miniconda/conda run: 
----------------------------------------
::

    conda config --add channels conda-forge
    conda install spiceypy

If no error was returned you have successfully installed SpiceyPy.
To verify this you can list the installed packages via this pip command::

    pip list

You should see spicepy in the output of this command.
Or you can start a python interpreter and try importing SpiceyPy like so:

.. code:: python

    import spiceypy

    # print out the toolkit version installed
    print(spiceypy.tkvrsn('TOOLKIT'))

This should print out the toolkit version without any errors. You have now
verified that SpiceyPy is installed.

Offline installation
--------------------

If you need to install SpiceyPy without a network or if you have a prebuilt shared library at hand,
you can override the default behaviour of SpiceyPy by using the CSPICE_SRC_DIR and CSPICE_SHARED_LIB environment variables respectively.

For example, if you have downloaded SpiceyPy and the CSPICE toolkit, and extracted CSPICE to /tmp/cspice you can run:

.. code-block:: bash

            export CSPICE_SRC_DIR="/tmp/cspice"
            python setup.py install

Or if you have a shared library of CSPICE located at /tmp/cspice.so, you can run:

.. code-block:: bash

            export CSPICE_SHARED_LIB="/tmp/cspice.so"
            python setup.py install

Both examples above assume you have cloned the SpiceyPy repository and are running those commands within the project directory.

A simple example program
------------------------

This script calls the spiceypy function 'tkvrsn' and outputs the return
value.

.. code-block:: python

              File tkvrsn.py

                 from __future__ import print_function
                 import spiceypy

                 def print_ver():
                         """Prints the TOOLKIT version
                         """
                         print(spiceypy.tkvrsn('TOOLKIT'))

                 if __name__ == '__main__':
                         print_ver()

From the command line, execute the function:

::

              $ python tkvrsn.py
              CSPICE_N0066

From Python, execute the function:

::

              $ python
              >>> import tkvrsn
              >>> tkvrsn.print_ver()
              CSPICE_N0066

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

      tkvrsn(item)
          Given an item such as the Toolkit or an entry point name, return
          the latest version string.

          https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tkvrsn_c.
      html

          :param item: Item for which a version string is desired.
          :type item: str
          :return: the latest version string.
          :rtype: str

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
    such as visual studio and additional environment configuration. Given
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

    python setup.py install

The installation script will download the appropriate
version of the SPICE toolkit for your system, and will
build a shared library from the included static library
files. Then the installation script will install SpiceyPy
along with the generated shared library into your
site-packages directory.
