SpiceyPy
========

SpiceyPy is a Python wrapper for the NAIF C SPICE Toolkit (N66), written using ctypes.

+------------------------+-------------------+--------+------------+--------------+
| Continuous Integration | Code Coverage     | Docs   |  Citation  |  Code Style  |
+========================+===================+========+============+==============+
| |Github Build Status|  | |Coverage Status| | |Docs| | |JOSS|     |  |Black|     |
+------------------------+-------------------+--------+------------+--------------+

.. |Github Build Status| image:: https://img.shields.io/github/actions/workflow/status/AndrewAnnex/SpiceyPy/ci-build.yml?branch=main
   :alt: Github - Build Status
   :target: https://github.com/AndrewAnnex/SpiceyPy/actions
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/AndrewAnnex/SpiceyPy/main?logo=codecov
   :alt: Codecov - Test Coverage
   :target: https://codecov.io/gh/AndrewAnnex/SpiceyPy
.. |Docs| image:: https://img.shields.io/readthedocs/spiceypy/main
   :alt: Readthedocs - Documentation
   :target: http://spiceypy.readthedocs.org/en/main/
.. |JOSS| image:: https://joss.theoj.org/papers/98136d30bea9982ad160d251e2039fee/status.svg
   :alt: Citation Information: Journal of Open Source Software
   :target: https://joss.theoj.org/papers/98136d30bea9982ad160d251e2039fee
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg 
   :alt: Code Style - Black
   :target: https://github.com/psf/black


Introduction
------------

SpiceyPy is a python wrapper for the `SPICE Toolkit <https://naif.jpl.nasa.gov/naif/>`__.
SPICE is an essential tool for scientists and engineers alike in the planetary
science field for Solar System Geometry. Please visit the NAIF website for more details about SPICE.

*IMPORTANT*: The code is provided "as is", use at your own risk. However, the NAIF now distributes python "lessons" that use SpiceyPy as the python to spice interface.

Citing SpiceyPy
---------------

If you are publishing work that uses SpiceyPy, please cite SpiceyPy and the SPICE toolkit.

SpiceyPy can be cited using the JOSS DOI (`https://doi.org/10.21105/joss.02050`) or with the following:
    Annex et al., (2020). SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit. Journal of Open Source Software, 5(46), 2050, https://doi.org/10.21105/joss.02050

Instructions for how to cite the SPICE Toolkit are available on the NAIF website: 
    https://naif.jpl.nasa.gov/naif/credit.html. 

To cite information about SpiceyPy usage statistics, please cite my 2017 and or 2019 abstracts as appropriate below:
    1. 2017 abstract: `<https://ui.adsabs.harvard.edu/abs/2017LPICo1986.7081A/abstract>`__.
    2. 2019 abstract: `<https://ui.adsabs.harvard.edu/abs/2019LPICo2151.7043A/abstract>`__.

Installation
------------

+----------------+-------------------+
| PyPI           | Conda Forge       |
+================+===================+
| |PyPI|         | |Conda Version|   |
+----------------+-------------------+

.. |PyPI| image:: https://img.shields.io/pypi/v/spiceypy.svg
   :alt: PyPI - python package index
   :target: https://pypi.org/project/spiceypy/
.. |Conda Version| image:: https://img.shields.io/conda/vn/conda-forge/spiceypy.svg
   :alt: Conda - conda-forge feedstock for SpiceyPy
   :target: https://anaconda.org/conda-forge/spiceypy

SpiceyPy can be installed using pip by running:
``pip install spiceypy``

Anaconda users should use the conda-forge distribution of SpiceyPy by running:

``conda config --add channels conda-forge``

``conda install spiceypy``

If you wish to install spiceypy from source first download or clone the project. Then run ``python setup.py install``.
To uninstall run ``pip uninstall spiceypy``.

Documentation
-------------

The SpiceyPy docs are available at:
`spiceypy.readthedocs.org <http://spiceypy.readthedocs.org>`__.
The documentation for SpiceyPy is intentionally abridged so as to utilize the excellent `documentation provided by the
NAIF. <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/index.html>`__
Please refer to C and IDL documentation available on the NAIF website
for in-depth explanations. Each function docstring has a link to the
corresponding C function in the NAIF docs at a minimum.
SpiceyPy documentation contains the NAIF authored `Lessons <https://spiceypy.readthedocs.io/en/main/lessonindex.html>`__ for step-by-step tutorials with code examples. 

How to Help
-----------

Feedback is always welcomed, if you discover that a function is not working as expected,
submit an issue detailing how to reproduce the problem. If you utilize SpiceyPy frequently 
please consider contributing to the project by citing me using the zenodo DOI above.

Known Working Environments:
---------------------------

SpiceyPy is compatible with modern Linux, Mac, and Windows
environments. Since the package is a wrapper, any environment not
supported by the NAIF is similarly not supported by SpiceyPy.
If you run into issues with your system please submit an issue with details. 
Please note that support for Python minor versions are generally phased out 
as newer versions are released. 

- OS: OS X, Linux, Windows, FreeBSD
- CPU: 64bit only!
- Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
- ARM support for Linux-aarch64 & osx-arm64

* Support for Python 2.7 ended with version 2.3.2 January 2020 *

Acknowledgements
----------------

`DaRasch <https://github.com/DaRasch>`__ wrote spiceminer, which I
looked at to get SpiceCells working, thanks!

