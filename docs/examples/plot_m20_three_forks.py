"""
Perseverance at the Three Forks sample depot
============================================

Use SPICE kernels from the Mars 2020 mission to plot the Perseverance rover's
drive over sols 648-693, when it laid down the Three Forks sample depot in
Jezero crater.

Introduces :py:func:`~spiceypy.spiceypy.furnsh`,
:py:func:`~spiceypy.spiceypy.str2et`, :py:func:`~spiceypy.spiceypy.spkpos`,
:py:func:`~spiceypy.spiceypy.reclat` and :py:func:`~spiceypy.spiceypy.et2utc`.
"""

# %%
# Setup
# -----
# The first run downloads Pyodide, the packages and 20 subset SPICE kernels
# (about 2 MB) in the background, so it can take a little while.

import numpy as np
import matplotlib

matplotlib.use("AGG")
import matplotlib.pyplot as plt
from pyscript import display
import spiceypy as spice

print("ready!")

# %%
# Load the kernels
# ----------------
# :py:func:`~spiceypy.spiceypy.furnsh` loads kernels. A metakernel is a text
# kernel listing other kernels to load; its ``PATH_VALUES`` are relative to
# the working directory, so change into the folder that holds it first.

import os

if os.path.isdir("m20_three_forks_demo"):
    os.chdir("m20_three_forks_demo")
spice.furnsh("m2020_v16_221216_230201.tm")
print(f"We loaded {spice.ktotal('ALL')} Kernel files")

# %%
# Define start and end dates and sample points
# --------------------------------------------
# :py:func:`~spiceypy.spiceypy.str2et` converts a date string to ephemeris
# time: seconds past J2000 (TDB), leap seconds included.

sol_648 = spice.str2et("2022-12-16")
sol_693 = spice.str2et("2023-01-31")
times = np.linspace(sol_648, sol_693, num=45 * 24 * 20, endpoint=True)
print(f"Sampling {len(times)} times over 45 sols")

# %%
# Grab the positions
# ------------------
# :py:func:`~spiceypy.spiceypy.spkpos` answers "where is the target, seen from
# the observer?", and is vectorized over times: one call, 21,600 positions.
# :py:func:`~spiceypy.spiceypy.reclat` converts each x, y, z to radius,
# longitude and latitude.

positions, lttimes = spice.spkpos("M2020", times, "IAU_MARS", "lt+s", "MARS")
print(f"Successfully grabbed {len(positions)} positions in IAU_MARS frame.")
# convert from rectangular to latitudinal coordinates (in radians).
r, lon, lat = np.array([spice.reclat(p) for p in positions]).T
# convert to degrees
lon, lat = np.degrees(lon), np.degrees(lat)

# %%
# Plot the rover's traverse
# -------------------------
# Points are colored by time, so the drive runs from purple to yellow.
# :py:func:`~spiceypy.spiceypy.et2utc` converts the first and last ephemeris
# times back to UTC strings to label the ends of the drive.

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.plot(lon, lat)
ax.scatter(lon, lat, c=times)
ax.ticklabel_format(useOffset=False, style="plain")
ax.tick_params(axis="x", labelrotation=45)
ax.set_xlabel("longitude (°E)")
ax.set_ylabel("latitude (°N)")
ax.set_title("M20 Rover Traverse Sols 648-693")
first, last = spice.et2utc([times[0], times[-1]], "ISOC", 0)
for i, utc in ((0, first), (-1, last)):
    ax.annotate(utc[:10], (lon[i], lat[i]), textcoords="offset points", xytext=(6, 6))
fig.tight_layout()
display(fig, target="mpl_m20", append=False)
print(f"Plotted {len(times)} positions from {first} to {last} UTC")
spice.kclear()  # tidy the kernel pool
