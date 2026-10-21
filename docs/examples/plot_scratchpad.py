"""
SpiceyPy scratchpad
===================

A blank page for your own SpiceyPy experiments, right in the browser. The
environment has NumPy, SciPy, SymPy, Astropy and matplotlib installed, and a
few generic kernels loaded: leap seconds, planetary constants and a planetary
ephemeris for 2000-2019.
"""

# %%
# Imports and kernels
# -------------------
# Run this cell first. The first run downloads Pyodide and the packages, so it
# can take a little while.

import numpy as np
import scipy
import sympy
import astropy
import astropy.units as u
from astropy.time import Time
import matplotlib

matplotlib.use("AGG")
import matplotlib.pyplot as plt
from pyscript import display
import spiceypy as spice

spice.furnsh(
    [
        "scratchpad/naif0012.tls",  # leap seconds
        "scratchpad/pck00010.tpc",  # body radii and orientation
        "scratchpad/gm_de431.tpc",  # body GM values
        "scratchpad/de440s_2000_to_2020_simplified.bsp",  # planet barycenters
    ]
)
print(f"SpiceyPy {spice.__version__} ({spice.tkvrsn('TOOLKIT')})")
print(f"NumPy {np.__version__}, SciPy {scipy.__version__}, SymPy {sympy.__version__}")
print(f"Astropy {astropy.__version__}, matplotlib {matplotlib.__version__}")
print(f"Loaded {spice.ktotal('ALL')} kernels")

# %%
# A starter plot
# --------------
# The inner planets' orbits around the solar system barycenter during 2019, in
# the ecliptic plane. Plot with ``display(fig, target=..., append=False)``,
# which draws the figure in the box below the cell.

ets = np.linspace(spice.str2et("2019-01-01"), spice.str2et("2019-12-31"), 1000)
fig, ax = plt.subplots(figsize=(6, 6))
for planet in ["MERCURY", "VENUS", "EARTH", "MARS"]:
    pos, _ = spice.spkpos(f"{planet} BARYCENTER", ets, "ECLIPJ2000", "NONE", "0")
    au = pos / spice.convrt(1, "AU", "KM")
    ax.plot(au[:, 0], au[:, 1], label=planet.title())
    ax.plot(au[0, 0], au[0, 1], "o", color=ax.lines[-1].get_color())
ax.set_aspect("equal")
ax.set_xlabel("x (AU)")
ax.set_ylabel("y (AU)")
ax.set_title("Inner planets during 2019 (dots: Jan 1)")
ax.legend(loc="upper right")
display(fig, target="mpl_starter", append=False)
print(f"Plotted {len(ax.lines) // 2} orbits from {len(ets)} times each")

# %%
# Your turn
# ---------
# This cell is yours: replace it with anything SpiceyPy related. A few ideas:
# where Mars was on your birthday (if it was in 2000-2019), Saturn's distance
# from Earth over the years, or when Venus and Mars line up as seen from Earth
# (:py:func:`~spiceypy.spiceypy.gfsep`).

# Astropy times convert with spice.str2et(Time(...).isot).
# To plot here, use display(fig, target="scratch", append=False)
et = spice.str2et(Time("2019-06-10", scale="utc").isot)
# Jupiter was at opposition, closest to Earth for the year, on 2019-06-10
pos, lt = spice.spkpos("JUPITER BARYCENTER", et, "J2000", "LT+S", "EARTH")
print(f"On {spice.et2utc(et, 'C', 0)}, light took {lt / 60:.1f} minutes from Jupiter")
