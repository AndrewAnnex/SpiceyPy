============
Installation
============

SpiceyPy is currently supported on Mac, Linux, and Windows systems.

.. _installation:

If you are new to python, it is a good idea to read a bit about it first `<docs.python-guide.org>`_.
For new installations of python, it is encouraged to install and or update: pip, setuptools, wheel, numpy, six, certifi::

    pip install -U pip setuptools wheel
    pip install -U numpy six certifi

Then to install SpiceyPy, simply run::

    pip install spiceypy

If you use anaconda/miniconda/conda run::

    conda install -c https://conda.anaconda.org/andrewannex spiceypy

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

=============
Common Issues
=============

SSL Alert Handshake Issue
-------------------------
In early 2017, JPL updated to a TLS1.2 certificate and enforced https connections causing installation
issues for users, in particular for macOS users, with OpenSSL versions older
than 1.0.1g. This is because older versions of OpenSSL still distributed in some
environments which are incompatible with TLS1.2. As of late 2017 SpiceyPy has been updated with
a strategy that can mitigate this issue on some systems, but it may not be totally reliable due to known deficiencies in setuptools and pip.

Another solution is to configure a new python installation that is linked against a newer version
of OpenSSL, the easiest way to do this is to install python using homebrew, once this is done spiceypy
can be installed to this new installation of python (IMHO this is the best option).

If your python 3.6 distribution was installed from the packages available at python.org an included command
``Install Certificates.command`` should be run before attempting to install SpiceyPy again.
That command installs the certifi package that can also be install using pip. 

Alternatively, installing an anaconda or miniconda
python distribution and installing SpiceyPy using the conda command above is another possible work around.

Users continuing to have issues should report an issue to the github repository.

Supporting links:

`<https://bugs.python.org/issue29065>`_
`<https://github.com/requests/requests/issues/2022>`_
`<https://pyfound.blogspot.com/2017/01/time-to-upgrade-your-python-tls-v12.html>`_
`<https://www.python.org/dev/peps/pep-0518>`_
`<https://github.com/AndrewAnnex/SpiceyPy/pull/202>`_

======================================================
How to install from source (for bleeding edge updates)
======================================================

.. attention::

    If you have used the pip or conda install commands above you do not
    need to do any of the following commands. Installing from source is intended
    for advanced users. Users on machines running Windows should take note
    that attempting to install from source will require software
    such as visual studio and additonal environment configuration. Given
    the complexity of this Windows users are highly encouraged to stick
    with the releases made available through PyPi/Anaconda Cloud.


If you wish to install from source, first simply clone the repository by
running the following in your favorite shell::

    git clone git@github.com:AndrewAnnex/SpiceyPy.git

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
