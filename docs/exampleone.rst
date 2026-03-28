========================
Cassini Position Example
========================

Below is an example that uses spiceypy to plot the position of the
Cassini spacecraft relative to the barycenter of Saturn.

.. py-editor::
    :env: cass
    :config: pyscript_cassini_example.json
    :setup:

    from pyscript import display
    import numpy as np
    import matplotlib
    matplotlib.use("AGG")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import spiceypy as spice


First import spiceypy and test it out.

.. py-editor::
    :env: cass
    :config: pyscript_cassini_example.json

    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import spiceypy as spice
    # Print out the toolkit version
    print(f'SpiceyPy for {spice.tkvrsn("TOOLKIT")} ready!')


.. parsed-literal::

    'CSPICE_N0067'


We will need to load some kernels. You will need to download the following kernels
from the NAIF servers via the links provided. After the kernels have been downloaded
to a common directory write a metakernel containing the file names for each downloaded
kernel (provided after the links).
I named the metakernel 'cassMetaK.txt' for this example. For more on defining
meta kernels in spice, please consult the `Kernel Required Reading <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/kernel.html>`_.

- `naif0009.tls <https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/a_old_versions/naif0009.tls>`_
- `cas00084.tsc <https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/sclk/cas00084.tsc>`_
- `cpck05Mar2004.tpc <https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/pck/cpck05Mar2004.tpc>`_
- `cas_v37.tf <https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/fk/release.11/cas_v37.tf>`_
- `cas_iss_v09.ti <https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ik/release.11/cas_iss_v09.ti>`_
- `030201AP_SK_SM546_T45.bsp <https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/030201AP_SK_SM546_T45.bsp>`_
- `020514_SE_SAT105.bsp <https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/020514_SE_SAT105.bsp>`_
- `981005_PLTEPH-DE405S.bsp <https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/981005_PLTEPH-DE405S.bsp>`_


.. py-editor::
    :env: cass

    # The Following kernels can also be downloaded from the NAIF at these urls:
    # the kernels with "_s" postfixes are subset from the NAIF hosted versions
    #   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/lsk/naif0008.tls
    #   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/sclk/cas00084.tsc
    #   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/pck/cpck05Mar2004.tpc
    #   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/fk/release.11/cas_v37.tf
    #   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ik/release.11/cas_iss_v09.ti
    #   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/030201AP_SK_SM546_T45.bsp
    #   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/020514_SE_SAT105.bsp
    #   https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/981005_PLTEPH-DE405S.bsp

    spice.furnsh([
        'kernels/lsk/naif0008.tls',
        'kernels/sclk/cas00084.tsc',
        'kernels/pck/cpck05Mar2004.tpc',
        'kernels/fk/cas_v37.tf',
        'kernels/ik/cas_iss_v09.ti',
        'kernels/spk/020514_SE_SAT105_s.bsp',
        'kernels/spk/981005_PLTEPH-DE405S_s.bsp',
        'kernels/spk/030201AP_SK_SM546_T45_s.bsp'
    ])
    print(f'Loaded {spice.ktotal("ALL")} kernels')


.. py-editor::
    :env: cass

    step = 4000
    # we are going to get positions between these two dates
    utc = ["Jun 20, 2004", "Dec 1, 2005"]

    # get et values one and two, we could vectorize str2et
    etOne = spice.str2et(utc[0])
    etTwo = spice.str2et(utc[1])
    print(f"ET One: {etOne}, ET Two: {etTwo}")


.. parsed-literal::

    ET One: 140961664.18440723, ET Two: 186667264.18308285


.. py-editor::
    :env: cass

    # get times
    times = [x * (etTwo - etOne) / step + etOne for x in range(step)]

    # check first few times:
    print(times[0:3])


.. parsed-literal::

    [140961664.18440723, 140973090.5844069, 140984516.98440656]


.. py-editor::
    :env: cass

    # check the documentation on spkpos before continuing
    help(spice.spkpos)


.. parsed-literal::

    Help on function spkpos in module spiceypy.spiceypy:

    spkpos(targ: str, et: Union[float, numpy.ndarray], ref: str, abcorr: str, obs: str) -> Union[Tuple[numpy.ndarray, float], Tuple[numpy.ndarray, numpy.ndarray]]
        Return the position of a target body relative to an observing
        body, optionally corrected for light time (planetary aberration)
        and stellar aberration.

        https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkpos_c.html

        :param targ: Target body name.
        :param et: Observer epoch.
        :param ref: Reference frame of output position vector.
        :param abcorr: Aberration correction flag.
        :param obs: Observing body name.
        :return:
                Position of target,
                One way light time between observer and target.




.. py-editor::
    :env: cass

    # Run spkpos as a vectorized function
    positions, lightTimes = spice.spkpos(
        "Cassini", times, "J2000", "NONE", "SATURN BARYCENTER"
    )

    # Positions is a 3xN vector of XYZ positions
    print("Positions: ")
    print(positions[0])

    # Light times is a N vector of time
    print("Light Times: ")
    print(lightTimes[0])


.. parsed-literal::

    Positions:
    [-5461446.61080924 -4434793.40785864 -1200385.93315424]
    Light Times:
    23.8062238783


.. py-editor::
    :env: cass

    # Clean up the kernels
    spice.kclear()

We will use matplotlib's 3D plotting to visualize Cassini's coordinates. We first convert the
positions list to a 2D numpy array for easier indexing in the plot.

.. py-editor::
    :env: cass
    :placeholder: images/exampleoneplot_min.png
    :target: mpl

    positions = (
        positions.T
    )  # positions is shaped (4000, 3), let's transpose to (3, 4000) for easier indexing
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(positions[0], positions[1], positions[2])
    plt.title("SpiceyPy Cassini Position Example from Jun 20, 2004 to Dec 1, 2005")
    display(fig, target="mpl", append=False)
