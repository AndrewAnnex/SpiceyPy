# cython: language_level = 3
"""
main cython wrapper code
"""

import numpy as np
cimport numpy as np
np.import_array()

cpdef b1900():
    return b1900_c()

# cpdef b1900_loop(int N):
#     r = np.zeros(N, dtype=np.double)
#     for i in range(N):
#         r[i] = b1900_c()
#     return r

cpdef void furnsh(str s):
    furnsh_c(s.encode('utf8'))

# cpdef int ktotal(str s):
#     "test docstring"
#     cdef int count
#     ktotal_c(s.encode('utf8'), &count)
#     return count
