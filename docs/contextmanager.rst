.. _KernelPool:

The KernelPool context manager 
========================================= 

The :py:exc:`KernelPool<spiceypy.spiceypy.KernelPool>` context manager provides a convenient way to load, and unload SPICE kernels, guaranteeing that the kernel database will still be cleared if an exception is raised.

.. warning::
    :py:exc:`KernelPool<spiceypy.spiceypy.KernelPool>` uses :py:exc:`spice.kclear()<spiceypy.spiceypy.kclear>` to temporarily unload previously loaded kernels. Thus, any user-defined variable will be permanently deleted from the kernel pool. Check the :ref:`Compatibility with kernel-pool assignment functions<kernel_pool_assignment_functions>` section for a detailed explanation.

Basic usage
-----------

A typical program using SpiceyPy starts with :py:exc:`spice.furnsh()<spiceypy.spiceypy.furnsh>`, and ends with :py:exc:`spice.kclear()<spiceypy.spiceypy.kclear>` or :py:exc:`spice.unload()<spiceypy.spiceypy.unload>`. If an exception is raised while loading kernels or executing user code, :py:exc:`spice.kclear()<spiceypy.spiceypy.kclear>` won't be executed, and the kernel database won't be cleared. To avoid this issue, a ``try...finally`` clause is often used:

.. code:: python

   try:
       spice.furnsh("path/to/kernels")
       # user code
   finally:
       spice.kclear()

The :py:exc:`KernelPool<spiceypy.spiceypy.KernelPool>` context manager provides the exact same result as the
previous example, but with a simpler syntax.

.. code:: python

   with spice.KernelPool("path/to/kernels"):
       
       # user code

Local and global kernels
------------------------

Each of the kernels used to initialize the context manager is known as a *local kernel*. Any kernel loaded before the ``with`` statement is known as
a *global kernel*. :py:exc:`KernelPool<spiceypy.spiceypy.KernelPool>` creates an isolated environment from which
only *local kernels* are accessible.

.. The set of kernels that the context manager takes as input is the set
.. *local kernels*. Any kernel that was loaded before the ``with``
.. statement is know as a *global kernel*. ``KernelPool`` creates an
.. isolated environment from which only *local kernels* are accessible.

.. code:: python

   spice.furnsh(["A", "B"])
   function_1()
   with spice.KernelPool(["A", "C", "D"]):
       function_2()
   function_3()

In the previous example, ``function_1()`` and ``function_3()`` have
access to kernels ``A``, and ``B`` (global kernels); while ``function_2()`` has
access to kernels ``A``, ``C``, and ``D`` (local kernels).

.. _kernel_pool_assignment_functions:

Compatibility with kernel-pool assignment functions
---------------------------------------------------

In order to create an isolated environment for local kernels,
:py:exc:`KernelPool<spiceypy.spiceypy.KernelPool>` performs a series of steps: 

#. Unload global kernels using :py:exc:`spice.kclear()<spiceypy.spiceypy.kclear>`. 
#. Load local kernels using :py:exc:`spice.furnsh()<spiceypy.spiceypy.furnsh>`. 
#. Execute user code. 
#. Unload local kernels using :py:exc:`spice.kclear()<spiceypy.spiceypy.kclear>`. 
#. Load global kernels using :py:exc:`spice.furnsh()<spiceypy.spiceypy.furnsh>`.

In addition to :py:exc:`spice.furnsh()<spiceypy.spiceypy.furnsh>`, SpiceyPy provides a series of functions (kernel-pool assignment functions) to add user-defined variables to the kernel pool, such as :py:exc:`spice.pcpool()<spiceypy.spiceypy.pcpool>`, :py:exc:`spice.pdpool()<spiceypy.spiceypy.pdpool>`, or :py:exc:`spice.pipool()<spiceypy.spiceypy.pipool>`. As
:py:exc:`KernelPool<spiceypy.spiceypy.KernelPool>` unloads, and then reloads global kernels, these user defined variables are not restored after the ``with`` statement.

.. code:: python

   spice.furnsh(["A", "B"])
   spice.pipool("VAR", [13])
   function_1()
   with spice.KernelPool(["A", "C", "D"]):
       function_2()
   function_3()

In this example, though ``function_1()`` has access to ``VAR``,
``function_2()`` and ``function_3()`` don’t.

.. note::
    For more information about SPICE kernels, refer to the `Kernel required reading <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/FORTRAN/req/kernel.html#top>`_ document of the NAIF. The Kernel Management section of this document provides detailed explanations regarding the kernel pool, the kernel database, kernel pool assignment functions, and the behavior of :py:exc:`spice.furnsh()<spiceypy.spiceypy.furnsh>`, :py:exc:`spice.kclear()<spiceypy.spiceypy.kclear>` and :py:exc:`spice.unload()<spiceypy.spiceypy.unload>`.
