# %%
import spiceypy as spice # this imports the version 4.0.0
import os

# %%
import functools
import threading

from spiceypy.spiceypy import spkezr

spicelock = threading.RLock()

def spicelock_for_multithread(f):
    """
    :return:
    """

    @functools.wraps(f)
    def lock(*args, **kwargs):

        with spicelock:
            try:
                res = f(*args, **kwargs)
                return res
            except BaseException:
                raise

    return lock


# %%
from multiprocessing.dummy import Pool as ThreadPool



# %%
b1900 = spice.b1900
tb1900 = spicelock_for_multithread(b1900)

# %%
print('Test thread pool without locking for b1900')
with ThreadPool() as pool:
    test_b1900 = pool.map(lambda x: b1900(), range(10000))

print('Test thread pool with locking for b1900')
with ThreadPool() as pool:
    test_tb1900 = pool.map(lambda x: tb1900(), range(10000))



# %%
pathKernels = 'path/to/kernels'

defKernels = [
    'naif0012.tls',                     # leaps seconds
    'gm_de431.tpc',                     # planetary constants
    'de430.bsp',                        # planetary position and velocity ephemeris
    'earth_fixed.tf',                   # ECEF reference system definition
    'earth_070425_370426_predict.bpc',  # ECEF ephemeris 
    'pck00010.tpc'                      # Other constants
]

for k in defKernels:
    spice.furnsh(os.path.join(pathKernels,k))

# %%
spkezr = spice.spkezr
tspkezr = spicelock_for_multithread(spkezr)
# %%
# testing the spicelock_for_multithread decorator
print('Test thread pool without locking for spkezr')
try:
    with ThreadPool() as pool:
        test_spkezr = pool.map(lambda x: spkezr('EARTH',x,'J2000','NONE','SUN'),test_b1900)
except BaseException as e:
    print(e)


print('Test thread pool with locking for spkezr')
with ThreadPool() as pool:
    test_tspkezr = pool.map(lambda x: tspkezr('EARTH',x,'J2000','NONE','SUN'),test_b1900)

# %%
# testing the wrapt library
import wrapt
wb1900 = wrapt.synchronized(spicelock)(b1900)
wspkezr = wrapt.synchronized(spicelock)(spkezr)
# %%
print('Test thread pool with spicelock_for_multithread decorator for spkezr')
with ThreadPool() as pool:
    test_tspkezr = pool.map(lambda x: tspkezr('EARTH',x,'J2000','NONE','SUN'),test_b1900)

print('Test thread pool with wrapt.synchronized(spicelock) decorator for spkezr')
with ThreadPool() as pool:
    test_wspkezr = pool.map(lambda x: wspkezr('EARTH',x,'J2000','NONE','SUN'),test_b1900)

# %%
