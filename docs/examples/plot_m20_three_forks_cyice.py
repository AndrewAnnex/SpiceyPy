"""
Perseverance at the Three Forks sample depot, with cyice
========================================================

The :doc:`plot_m20_three_forks` example again, using the compiled
:doc:`cyice </cyice>` functions in place of their ctypes counterparts.
Where cyice isn't available (spiceypy releases whose Pyodide wheel predates
it), the example falls back to the ctypes functions, so it runs either way.

Introduces :py:func:`~spiceypy.cyice.cyice.furnsh`,
:py:func:`~spiceypy.cyice.cyice.str2et`, :py:func:`~spiceypy.cyice.cyice.spkpos`,
:py:func:`~spiceypy.cyice.cyice.reclat` and :py:func:`~spiceypy.cyice.cyice.et2utc`.
"""

# %%
# Setup
# -----
# The first run downloads Pyodide, the packages and 20 subset SPICE kernels
# (about 2 MB) in the background, so it can take a little while.
# cyice ships inside the spiceypy package, so there is nothing extra to install.
# ``sp`` is cyice when it imports, and the ctypes functions otherwise; both
# take the same arguments.

import numpy as np
import matplotlib

matplotlib.use("AGG")
import matplotlib.pyplot as plt
from pyscript import display
import spiceypy as spice

try:
    from spiceypy import cyice
except ImportError:
    cyice = None
sp = cyice if cyice is not None else spice
backend = "cyice" if cyice is not None else "ctypes"

print(f"ready! using the {backend} functions")

# %%
# Load the kernels
# ----------------
# :py:func:`~spiceypy.cyice.cyice.furnsh` loads kernels just like
# :py:func:`~spiceypy.spiceypy.furnsh`. cyice and the ctypes functions share
# one copy of CSPICE, so :py:func:`~spiceypy.spiceypy.ktotal` sees the
# kernels cyice loaded.

import os

if os.path.isdir("m20_three_forks_demo"):
    os.chdir("m20_three_forks_demo")
sp.furnsh("m2020_v16_221216_230201.tm")
print(f"We loaded {spice.ktotal('ALL')} Kernel files")

# %%
# Define start and end dates and sample points
# --------------------------------------------
# :py:func:`~spiceypy.cyice.cyice.str2et` converts a date string to ephemeris
# time: seconds past J2000 (TDB), leap seconds included.

sol_648 = sp.str2et("2022-12-16")
sol_693 = sp.str2et("2023-01-31")
times = np.linspace(sol_648, sol_693, num=45 * 24 * 20, endpoint=True)
print(f"Sampling {len(times)} times over 45 sols")

# %%
# Grab the positions
# ------------------
# Given an array of times, :py:func:`~spiceypy.cyice.cyice.spkpos` loops over
# them in compiled code and returns all 21,600 positions at once.
# :py:func:`~spiceypy.cyice.cyice.reclat` is vectorized too: pass it the whole
# N x 3 array of positions to get N rows of radius, longitude and latitude.
# The ctypes :py:func:`~spiceypy.spiceypy.reclat` takes one position at a time.

positions, lttimes = sp.spkpos("M2020", times, "IAU_MARS", "lt+s", "MARS")
print(f"Successfully grabbed {len(positions)} positions in IAU_MARS frame.")
# convert from rectangular to latitudinal coordinates (in radians).
if cyice is not None:
    r, lon, lat = cyice.reclat(positions).T
else:
    r, lon, lat = np.array([spice.reclat(p) for p in positions]).T
# convert to degrees
lon, lat = np.degrees(lon), np.degrees(lat)

# %%
# Compare with the ctypes functions
# ---------------------------------
# The same positions come back from :py:func:`~spiceypy.spiceypy.spkpos`;
# cyice just skips the per-call ctypes overhead.

import time

if cyice is None:
    print("cyice isn't available in this spiceypy, so there is nothing to compare")
else:
    start = time.perf_counter()
    ctypes_positions, _ = spice.spkpos("M2020", times, "IAU_MARS", "lt+s", "MARS")
    ctypes_seconds = time.perf_counter() - start
    start = time.perf_counter()
    cyice.spkpos("M2020", times, "IAU_MARS", "lt+s", "MARS")
    cyice_seconds = time.perf_counter() - start
    print(f"positions match: {np.allclose(positions, ctypes_positions)}")
    print(
        f"spiceypy.spkpos: {ctypes_seconds:.3f} s, cyice.spkpos: {cyice_seconds:.3f} s"
    )

# %%
# Plot the rover's traverse
# -------------------------
# Points are colored by time, so the drive runs from purple to yellow.
# :py:func:`~spiceypy.cyice.cyice.et2utc` converts the first and last ephemeris
# times back to UTC strings to label the ends of the drive.

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.plot(lon, lat)
ax.scatter(lon, lat, c=times)
ax.ticklabel_format(useOffset=False, style="plain")
ax.tick_params(axis="x", labelrotation=45)
ax.set_xlabel("longitude (°E)")
ax.set_ylabel("latitude (°N)")
ax.set_title(f"M20 Rover Traverse Sols 648-693 ({backend})")
first, last = sp.et2utc(np.array([times[0], times[-1]]), "ISOC", 0)
for i, utc in ((0, first), (-1, last)):
    ax.annotate(utc[:10], (lon[i], lat[i]), textcoords="offset points", xytext=(6, 6))
fig.tight_layout()
display(fig, target="mpl_m20_cyice", append=False)
print(f"Plotted {len(times)} positions from {first} to {last} UTC")
spice.kclear()  # tidy the kernel pool
