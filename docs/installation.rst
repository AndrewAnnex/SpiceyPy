============
Installation
============

SpiceyPy is currently supported on Mac and Linux.
To install, first simply clone the repository by
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