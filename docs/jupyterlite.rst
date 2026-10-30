.. _jupyterlite:

======================
JupyterLite Scratchpad
======================

.. DANGER::
  The Pyodide distribution of SpiceyPy is highly experimental, see :doc:`pyodide`.

A JupyterLab for quick SpiceyPy one-offs, right in the browser. Like the
:doc:`gallery/plot_scratchpad`, it runs SpiceyPy on
`Pyodide <https://pyodide.org/en/stable/>`_, here in
`JupyterLite <https://jupyterlite.readthedocs.io/en/latest/>`__, a JupyterLab
that runs entirely in your browser.

The scratchpad notebook below has the same setup as the gallery scratchpad:
run its first two cells to install NumPy, SciPy, SymPy, Astropy, matplotlib
and SpiceyPy and load a few generic kernels (leap seconds, planetary
constants and a planetary ephemeris for 2000-2019), then write your own
cells. The kernels are in the ``scratchpad`` folder in the file browser, and
you can start more notebooks from the Launcher (*File > New Launcher*).

Notebooks are saved in your browser's storage, not on a server, so use
*File > Download* to keep a copy. For more room,
`open the scratchpad in a new tab <lite/lab/index.html?path=scratchpad.ipynb>`__.

..
   Pages with live editors (.. py-editor::) register the mini-coi service
   worker for the whole site, which makes this page cross-origin isolated, and
   JupyterLite's kernel then never starts. JupyterLite unregisters it, so it
   only bites the first visit after such a page: drop it and reload once.

.. raw:: html

   <script>
     (() => {
       const sw = navigator.serviceWorker;
       const isMiniCoi = (w) => w && w.scriptURL.endsWith("/mini-coi.js");
       // the flag stops a reload loop if unregistering fails
       if (!isMiniCoi(sw && sw.controller)) return sessionStorage.removeItem("mini-coi-dropped");
       if (sessionStorage.getItem("mini-coi-dropped")) return;
       sessionStorage.setItem("mini-coi-dropped", "1");
       sw.getRegistrations()
         .then((regs) => Promise.all(regs.filter((r) => isMiniCoi(r.active)).map((r) => r.unregister())))
         .finally(() => location.reload());
     })();
   </script>

.. jupyterlite:: scratchpad.ipynb
   :height: 800px
