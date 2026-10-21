"""
The next solar eclipse over Santa Monica
========================================

SPICE's geometry finder (GF) searches time for *when* something happens. Here
it finds every solar eclipse visible from Santa Monica, California between
October 2026 and 2033: when the Moon passes near the Sun, when it actually blocks it, and
which of those happen while the Sun is above the horizon.

Introduces :py:func:`~spiceypy.spiceypy.boddef`,
:py:func:`~spiceypy.spiceypy.lmpool`, :py:func:`~spiceypy.spiceypy.spkw08`,
:py:func:`~spiceypy.spiceypy.gfsep`, :py:func:`~spiceypy.spiceypy.gfoclt` and
:py:func:`~spiceypy.spiceypy.gfposc`.
"""

# %%
# Load the kernels
# ----------------
# A leapseconds kernel, the Sun, Earth and Moon shapes and orientations, and a
# cut of the DE438 planetary ephemeris covering October 2026 through 2033.

import os
from zoneinfo import ZoneInfo
import spiceypy as spice

pacific = ZoneInfo("America/Los_Angeles")
spice.furnsh(
    [
        "santa_monica_eclipse/lsk/naif0012.tls",
        "santa_monica_eclipse/pck/pck00010_sun_earth_moon.tpc",
        "santa_monica_eclipse/spk/de438s_2026_2033.bsp",
    ]
)
print(f'Loaded {spice.ktotal("ALL")} kernels')

# %%
# Make a Santa Monica frame
# -------------------------
# :py:func:`~spiceypy.spiceypy.boddef` names a new body, and
# :py:func:`~spiceypy.spiceypy.lmpool` defines a topocentric frame for it from
# strings, exactly as a frame kernel would: +Z up, +X north, fixed to the Earth.

lon, lat = -118.4912, 34.0195  # Santa Monica, degrees
spice.boddef("SANTA_MONICA", 399901)
spice.lmpool(
    [
        "FRAME_SANTA_MONICA_TOPO = 1399901",
        "FRAME_1399901_NAME = 'SANTA_MONICA_TOPO'",
        "FRAME_1399901_CLASS = 4",
        "FRAME_1399901_CLASS_ID = 1399901",
        "FRAME_1399901_CENTER = 399901",
        "TKFRAME_1399901_RELATIVE = 'IAU_EARTH'",
        "TKFRAME_1399901_SPEC = 'ANGLES'",
        "TKFRAME_1399901_UNITS = 'DEGREES'",
        "TKFRAME_1399901_AXES = (3, 2, 3)",
        f"TKFRAME_1399901_ANGLES = ({-lon}, {lat - 90}, 180)",
    ]
)
print(f"Defined frame {spice.frmnam(1399901)} for {spice.bodc2n(399901)}")

# %%
# ...and an SPK for where it is
# -----------------------------
# :py:func:`~spiceypy.spiceypy.georec` turns longitude and latitude into a
# position on the Earth's ellipsoid, and :py:func:`~spiceypy.spiceypy.spkw08`
# writes it to a new SPK file that covers the same span as the ephemeris.
# Reading the position back with :py:func:`~spiceypy.spiceypy.spkpos` checks
# that the new kernel loaded.

re, _, rp = spice.bodvrd("EARTH", "RADII", 3)[1]
site = spice.georec(lon * spice.rpd(), lat * spice.rpd(), 0, re, 1 - rp / re)
state = [*site, 0, 0, 0]  # fixed to the ground: no velocity in IAU_EARTH
et0, et1 = spice.str2et("2026 OCT 01"), spice.str2et("2034 JAN 02")
if os.path.exists("santa_monica.bsp"):
    os.remove("santa_monica.bsp")
handle = spice.spkopn("santa_monica.bsp", "Santa Monica", 0)
spice.spkw08(
    handle, 399901, 399, "IAU_EARTH", et0, et1, "Santa Monica",
    1, 2, [state, state], et0, et1 - et0,
)
spice.spkcls(handle)
spice.furnsh("santa_monica.bsp")
# read it back: how far is Santa Monica from the center of the Earth?
pos, _ = spice.spkpos("SANTA_MONICA", et0, "IAU_EARTH", "NONE", "EARTH")
print(f"Santa Monica is {spice.vnorm(pos):.1f} km from the center of the Earth")

# %%
# When is the Moon near the Sun?
# ------------------------------
# :py:func:`~spiceypy.spiceypy.gfsep` searches from October 19, 2026 through
# 2033 for the times the Moon is within 2° of the Sun. The start date is fixed
# so this page's results don't change as eclipses pass; try your own.

start = spice.str2et("2026 OCT 19")
search = spice.cell_double(2)
spice.wninsd(start, spice.str2et("2034 JAN 01"), search)
close = spice.cell_double(1000)
spice.gfsep(
    "MOON", "SPHERE", "IAU_MOON", "SUN", "SPHERE", "IAU_SUN",
    "LT", "SANTA_MONICA", "<", 2 * spice.rpd(), 0.0,
    spice.spd(), 500, search, close,
)
print(f"The Moon passes within 2° of the Sun {spice.wncard(close)} times")

# %%
# When does the Moon block the Sun?
# ---------------------------------
# :py:func:`~spiceypy.spiceypy.gfoclt` finds when one body occults another.
# Searching only inside the ``close`` windows from the last step keeps it fast.
# This is pure geometry, so some of these eclipses happen at night.

eclipses = spice.cell_double(1000)
spice.gfoclt(
    "ANY", "MOON", "ELLIPSOID", "IAU_MOON", "SUN", "ELLIPSOID", "IAU_SUN",
    "LT", "SANTA_MONICA", 180.0, close, eclipses,
)
# a window of [start, end] intervals
for i in range(spice.wncard(eclipses)):
    times = spice.et2datetime(spice.wnfetd(eclipses, i))
    start, end = [t.astimezone(pacific) for t in times]
    print(f"{start:%a %b %d %Y, %I:%M %p} to {end:%I:%M %p %Z}")

# %%
# ...while the Sun is up?
# -----------------------
# :py:func:`~spiceypy.spiceypy.gfposc` finds when a coordinate meets a
# condition. The Sun's elevation is its latitude in the site's topocentric
# frame, so ``LATITUDE > 0`` means the Sun is above the horizon. Using the
# eclipse windows as the confinement window gives eclipse *and* Sun up.

visible = spice.cell_double(1000)
spice.gfposc(
    "SUN", "SANTA_MONICA_TOPO", "LT+S", "SANTA_MONICA",
    "LATITUDINAL", "LATITUDE", ">", 0.0, 0.0,
    3600.0, 500, eclipses, visible,
)
for i in range(spice.wncard(visible)):
    times = spice.et2datetime(spice.wnfetd(visible, i))
    start, end = [t.astimezone(pacific) for t in times]
    print(f"{start:%a %b %d %Y, %I:%M %p} to {end:%I:%M %p %Z}")

# %%
# When is each eclipse deepest?
# -----------------------------
# The peak is when the Sun and Moon are closest together on the sky, which
# ``gfsep`` finds with the ``ABSMIN`` relation. Compare with `time.now
# <https://time.now/los-angeles/eclipses/>`_'s maximum for Los Angeles:
# 8:20 AM on Jan 14 2029, 1:40 PM on Nov 14 2031 and 10:20 AM on Mar 30 2033.

for i in range(spice.wncard(visible)):
    eclipse = spice.cell_double(2)
    spice.wninsd(*spice.wnfetd(visible, i), eclipse)
    peak = spice.cell_double(2)
    spice.gfsep(
        "MOON", "SPHERE", "IAU_MOON", "SUN", "SPHERE", "IAU_SUN",
        "LT+S", "SANTA_MONICA", "ABSMIN", 0.0, 0.0,
        60.0, 1, eclipse, peak,
    )
    when = spice.et2datetime(spice.wnfetd(peak, 0)[0]).astimezone(pacific)
    print(f"peak at {when:%a %b %d %Y, %I:%M %p %Z}")

# %%
# How much of the Sun is covered?
# -------------------------------
# Sample the next visible eclipse and work out the fraction of the Sun's disk
# hidden behind the Moon: the overlap of two circles whose angular radii come
# from each body's radius and distance. Compare the peak with time.now's 51.6%
# for the January 2029 eclipse.

import numpy as np
import matplotlib

matplotlib.use("AGG")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pyscript import display

start, end = spice.wnfetd(visible, 0)
ets = np.linspace(start, end, 300)
moon, _ = spice.spkpos("MOON", ets, "J2000", "LT+S", "SANTA_MONICA")
sun, _ = spice.spkpos("SUN", ets, "J2000", "LT+S", "SANTA_MONICA")
dm, ds = np.linalg.norm(moon, axis=1), np.linalg.norm(sun, axis=1)
d = np.arccos(np.sum(moon * sun, axis=1) / (dm * ds))  # Moon-Sun separation
rm = np.arcsin(spice.bodvrd("MOON", "RADII", 3)[1][0] / dm)  # angular radii
rs = np.arcsin(spice.bodvrd("SUN", "RADII", 3)[1][0] / ds)
# area of the lens where the two disks overlap, as a fraction of the Sun's disk
d = np.clip(d, np.abs(rs - rm) + 1e-12, rs + rm)
lens = (
    rm**2 * np.arccos((d**2 + rm**2 - rs**2) / (2 * d * rm))
    + rs**2 * np.arccos((d**2 + rs**2 - rm**2) / (2 * d * rs))
    - 0.5 * np.sqrt((-d + rm + rs) * (d + rm - rs) * (d - rm + rs) * (d + rm + rs))
)
covered = 100 * lens / (np.pi * rs**2)
local = [t.astimezone(pacific) for t in spice.et2datetime(ets)]
print(f"{covered.max():.1f}% of the Sun covered at {local[covered.argmax()]:%I:%M %p %Z}")

fig, ax = plt.subplots(figsize=(7, 4))
ax.fill_between(local, covered, color="#f5a623", alpha=0.35)
ax.plot(local, covered, color="#c47d0e")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%I:%M %p", tz=pacific))
ax.set_ylim(0, None)
ax.set_ylabel("Sun's disk covered by the Moon (%)")
ax.set_title(f"Solar eclipse from Santa Monica, {local[0]:%b %d %Y}")
fig.tight_layout()
display(fig, target="mpl_eclipse", append=False)
spice.kclear()  # tidy the kernel pool
