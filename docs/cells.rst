===============
Cells Explained
===============

Spice Cells are data structures included in SPICE and serve as the equivalents to lists and sets for CSPICE.
For more primary documentation on cells, please see the `Cells required reading <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/cells.html>`_.
For SpiceyPy, cells can be constructed in a variety of ways, shown below.

.. code:: python

    import spiceypy as spice

    # create a spice bool cell using a function
    bool_cell = spice.cell_bool(10)

    # create a spice time cell using a function
    time_cell = spice.cell_time(10)

    # create a spice int cell using a function
    int_cell = spice.cell_int(10)

    # create a spice double cell using a function
    double_cell = spice.cell_double(10)

    # create a spice char cell using a function
    char_cell = spice.cell_char(10, 10)



One can also use provided classes to provide easier type checking,
in future versions SpiceyPy this may become default.

.. code:: python

    import spiceypy as spice

    # create a spice bool cell using a function
    bool_cell = spice.Cell_Bool(10)

    # create a spice time cell using a function
    time_cell = spice.Cell_Time(10)

    # create a spice int cell using a function
    int_cell = spice.Cell_Int(10)

    # create a spice double cell using a function
    double_cell = spice.Cell_Double(10)

    # create a spice char cell using a function
    char_cell = spice.Cell_Char(10, 10)
