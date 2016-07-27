============
Installation
============

SpiceyPy is currently supported on Mac, Linux, and Windows systems.

.. _installation:

To install simply run::

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

How to install from source (for bleeding edge)
----------------------------------------------

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