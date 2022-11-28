The `KernelPool` context manager
====================================================
The KernelPool context manager provides a convenient way to load, and 
unload SPICE kernels, guaranteeing that the kernel database will still 
be cleared if an exception is raised.

Basic usage
-------------------
A typical program using SpiceyPy starts with 
:py:exc:`spiceypy.spiceypy.furnsh()`, and ends 
with `spice.kclear()` or `spice.unload()`. If an exception is raised while 
loading kernels or executing user code, the `kclear()` function won't be 
executed, and the kernel database won't be cleared. To avoid this issue, 
a `try...finally` clause is often used.

```python
import spiceypy as spice

try:
	spice.furnsh("path/to/kernels")
	# user code
finally:
	spice.kclear()
```

The `KernelPool` context manager provides the exact same result as the 
previous example, but with a simpler syntax.

```python
import spiceypy as spice

with spice.KernelPool("path/to/kernels"):
	
	# user code
```

Local and global kernels
----------------------------------------
The set of kernels that the context manager takes as input are known as 
*local kernels*. Any kernel that was loaded before the `with` statement 
is know as a *global kernel*. `KernelPool` creates an isolated environment 
from which only *local kernels* are accessible. 

```python
import spiceypy as spice

spice.furnsh(["A", "B"])
function_1()
with spice.KernelPool(["A", "C", "D"]):
	function_2()
function_3()
```

In the previous example, `function_1()` and `function_3()` have access to 
kernels A, and B (global kernels); while `function_2()` has access to 
kernels A, C, and D (local kernels).

Compatibility with kernel-pool assignment functions
----------------------------------------------------
In order to create an isolated environment for local kernels, `KernelPool` 
performs a series of steps:
1. Unload *global kernels* using `kclear()`.
2. Load *local kernels* using `furnsh()`.
3. Execute user code.
4. Unload *local kernels* using `kclear()`.
5. Load *global kernels* using `furnsh()`.

In addition to `furnsh()`, SpiceyPy provides a series of functions 
(kernel-pool assignment functions) to add user defined variables to the 
kernel pool, such as `pcpool()`, `pdpool()`, or `pipool()`. As `KernelPool` 
unloads, and then reloads global kernels, these user defined variables are 
not restored after the `with` statement.

```python
import spiceypy as spice

spice.furnsh(["A", "B"])
spice.pipool("VAR", [13])
function_1()
with spice.KernelPool(["A", "C", "D"]):
	function_2()
function_3()
```

In this example, though `function_1()` has access to `VAR`,  `function_2()` 
and `function_3()` don't.
