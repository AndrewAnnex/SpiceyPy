=====================================
Pyodide (Browser-accessible) SpiceyPy
=====================================

.. DANGER::
  This distribution of SpiceyPy is highly experimental! 
  Do not trust it for anything critical. Use at your own risk.

A new Pyodide distribution of SpiceyPy is currently in development.

`Pyodide <https://pyodide.org/en/stable/>` is a port of CPython to WebAssembly, meaning a Python distribution that can run entirely natively within common web browsers.
Many popular scientific libraries are already availble for Pyodide, including numpy, scipy, matplotlib, pandas, and many more!

This version of SpiceyPy is essentially the same as the normal desktop Python distributions, as the CSPICE library is compiled to Wasm (web-assembly), allowing the pure python codebase for SpiceyPy to function essentially without modification.
The existing test suite for SpiceyPy is used to validate the distribution releases. 

It is however slightly limited:  

1. Currently, cyice is unsupported in this pyodide distribution and not included. That may eventually change.
2. Some functions may not function as expected or return null results, seemingly due to memory limitations and compilation differences.
3. Pyodide is currently limited to 32bit architecture.
4. Installation is not possible through PyPI yet, see section below.

Despite these limitations and the danger warning at the top of this page, the Pyodide distribution of SpiceyPy is an incredible new capability with the following potential applications:

1. Interactive web-based learning and teaching materials. No (to little) setup required.
2. Embeddable Spice code in websites and FFI with Javascript and other Web APIs.
3. Easier-to-use supporting information documents for scientific publications.
4. Wider system and device compatibility, run SpiceyPy on your Phone!

As per the warning above, production use is not recommended.

One of the best places to start using and learning about Pyodide is `Jupyter-lite <https://jupyter.org/try-jupyter/>`, a browser-native JupyterLab that includes many scientific python packages for use.

Installation
-------------

TODO



Usage Example
--------------

TODO 



Javascript Example
-------------------

TODO

