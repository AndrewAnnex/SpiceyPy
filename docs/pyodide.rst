=====================================
Pyodide (Browser-accessible) SpiceyPy
=====================================

.. DANGER::
  This distribution of SpiceyPy is highly experimental!
  Do not trust it for anything critical. Use at your own risk.

A new Pyodide distribution of SpiceyPy is currently in development.

`Pyodide <https://pyodide.org/en/stable/>`_ is a port of CPython to WebAssembly, meaning a Python distribution that can run entirely natively within common web browsers.
Many popular scientific libraries are already availble for Pyodide, including numpy, scipy, matplotlib, pandas, and many more!

This version of SpiceyPy is essentially the same as the normal desktop Python distributions, as the CSPICE library is compiled to Wasm (web-assembly), allowing the pure python codebase for SpiceyPy to function essentially without modification.
The existing test suite for SpiceyPy is used to validate the distribution releases.

It is however slightly limited:

1. Currently, cyice is unsupported in this pyodide distribution and not included. That may eventually change.
2. Some functions may not function as expected or return null results, seemingly due to memory limitations and compilation differences.
3. Pyodide is currently limited to 32bit architecture.
4. Installation is not possible through PyPI yet, see section below on installation.

Despite these limitations and the danger warning at the top of this page, the Pyodide distribution of SpiceyPy is an incredible new capability with the following potential applications:

1. Interactive web-based learning and teaching materials. No (to little) setup required.
2. Embeddable Spice code in websites and FFI with Javascript and other Web APIs.
3. Easier-to-use supporting information documents for scientific publications.
4. Wider system and device compatibility, run SpiceyPy on your Phone!

As per the warning above, production use is not recommended.

One of the best places to start using and learning about Pyodide is `Jupyter-lite <https://jupyter.org/try-jupyter/>`_, a browser-native JupyterLab that includes many scientific python packages for use.

Installation
-------------

Currently, this distribution of SpiceyPy is not available through PyPI due to the CSPICE dependency.

It is made available through a public GitHub repository `https://github.com/AndrewAnnex/spiceypy-wheels-dist <https://github.com/AndrewAnnex/spiceypy-wheels-dist>`_.

To install the wheel in Jupyter-lite, access the wheel file using the jsDelivr url corresponding release that will look something like:

.. code-block:: bash

    https://cdn.jsdelivr.net/gh/AndrewAnnex/spiceypy-wheels-dist@<tag>/spiceypy-<version>-cp313-cp313-pyodide_2025_0_wasm32.whl


Then use piplite like so:

.. code-block:: python

    import piplite
    await piplite.install("https://cdn.jsdelivr.net/gh/AndrewAnnex/spiceypy-wheels-dist@v8.0.2-dev.2/spiceypy-8.0.2-cp313-cp313-pyodide_2025_0_wasm32.whl")

Usage Example
--------------

This page has Pyodide SpiceyPy pre-installed, so no need to run the piplite command above.

Run the cell below by clicking the arrow on the right side when you hover over it with your mouse cursor.
It may take a few moments to finish. This software is running on your web browser, no background services (besides CDNs) required.

In the example below we will plot the Venus Rose (Venus's apparent position as seen from Earth
over 8 years in the J2000 ecliptic plane.).
Try updating the plot below to plot the barycenter of Mars or Mercury!

Various imports and setup:
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <script src="mini-coi.js"></script>
    <link rel="stylesheet" href="https://pyscript.net/releases/2026.2.1/core.css" />
    <script type="module" src="https://pyscript.net/releases/2026.2.1/core.js"></script>
    <script type="py-editor" env="shared" config="pyscript.json">
        import numpy as np
        import matplotlib
        matplotlib.use("AGG")
        import matplotlib.pyplot as plt
        from pyscript import display
        import spiceypy as spice
        print(f'SpiceyPy for {spice.tkvrsn("TOOLKIT")} ready!')
    </script>


Load kernels
~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <script type="py-editor" env="shared">
        # Load kernels: leap seconds + planetary ephemeris
        spice.furnsh("naif0012.tls")
        spice.furnsh("de440s_2000_to_2020_simplified.bsp")
        print(f'Loaded {spice.ktotal("ALL")} kernels.')
    </script>

Specify the dates to sample:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <script type="py-editor" env="shared">
        # Grab 2000 dates over 8 years
        et0 = spice.str2et("2000-01-01")
        et1 = spice.str2et("2008-01-01")
        ets = np.linspace(et0, et1, 2000)
        print(f'ets array has len: {len(ets)}')
    </script>

Get the positions vector
~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <script type="py-editor" env="shared">
        # Venus position relative to Earth in ecliptic J2000 (km)
        positions, _ = spice.spkpos("VENUS BARYCENTER", ets, "ECLIPJ2000", "NONE", "EARTH")
        print(f'Got {len(positions)} positions of the Venus Barycenter')
    </script>


Plot it on the ecliptic plane.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <script type="py-editor" env="shared">
        fig, ax = plt.subplots()
        ax.plot(positions[:, 0], positions[:, 1], color="black", linewidth=0.5)
        ax.plot(0, 0, "o", color="blue", markersize=6, label="Earth")
        ax.set_title("Geocentric Orbit of Venus (2000–2008)", fontsize=14)
        ax.legend()
        ax.set_aspect("equal")
        display(fig, target="mpl", append=False)
        plt.close('all')
    </script>
    <div id="mpl"></div>



Javascript Example
-------------------

TODO
