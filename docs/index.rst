Welcome to SpiceyPy's documentation!
====================================
Introduction
------------

SpiceyPy is a python wrapper for the `SPICE Toolkit <https://naif.jpl.nasa.gov/naif/>`__.
SPICE provides access and tools to interact with  planetary and spacecraft ephemeris and ancillary engineering information. 
Please visit the NAIF website for more details about SPICE.

*IMPORTANT*: The code is provided "as is", use at your own risk.

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

Documentation Overview
----------------------

This is the documentation for SpiceyPy. The documentation for each
function in the wrapper is in large part copied from the "Abstract"
and "Brief_I/O" sections of the corresponding CSPICE function documentation.
Each wrapper function has a link back to the corresponding original CSPICE
function documentation hosted at the NAIF website. For more in-depth information
about SPICE, please visit the NAIF website or
`click here <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/>`_
to view the entire CSPICE documentation.

The intent of the function doc-strings is to serve only as a quick reference to
what the parameter's expected types are for the purpose of getting started with
the wrapper. As each function has a link to the CSPICE documentation for that
function, more detailed explanations are deferred to the NAIF via those links.

Contents:

.. toctree::
   :maxdepth: 2

   citation
   installation
   changelog
   exampleone
   cells
   exceptions
   contextmanager
   requiredindex
   lessonindex
   documentation


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

