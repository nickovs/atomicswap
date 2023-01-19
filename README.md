# Atomic file swapping

Sadly, this is not a nuclear-powered utility to swap files. 

`atomicswap` is a Python module that implements the swapping of two files on a filesystem
in a single operation that can't be broken up; either the entire operation
completes correctly or none of it completes. This prevents the filesystem
from being left in an inconsistent state and avoids certain race conditions.

The API is very simple; only a single `swap()` function is provided.  The
function takes two file paths for the two files to be swapped. In the event
that either path is a relative path, you may also provide file descriptors
for directories that the relative paths should start from; if either is
missing then the path is relative to the current working directory. Paths
can be provided either as Python strings or `pathlib` paths.

## Installation

The latest stable version of `atomicswap` can be installed from the [Python
Package Index](https://pypi.org) using `pip` in the normal manner:
```
pip install atomicswap
```
If you want to try out the latest code then you can install it from the
GitHub repository:
```
pip install atomicswap@git+https://github.com/nickovs/atomicswap.git
```


## Example

Swapping the files `/etc/something/active` and `/etc/something/standby` in 
a single operation can be performed as follows:
```python
from atomicswap import swap
...
swap("/etc/something/active", "/etc/something/standby")
```
Alternatively, if using `Path` objects, this could be implemented as:
```python
from pathlib import Path
from atomicswap import swap
...
base_dir = Path("/etc/something")
swap(base_dir / "active", base_dir / "standby")
```

## Platform support

Currently `atomicswap` supports Linux and macOS. There is also a Windows
implementation but since I don't have a Windows system this is completely
untested.


## Dependencies

On both macOS and Linux `atomicswap` is not dependent on any non-standard
libraries or third party packages. On Windows it requires
[`pywin32`](https://pypi.org/project/pywin32/).


## Implementation details

Both Linux and macOS have kernel system calls that provide the simultaneous,
atomic swapping of the names of two files. On Linux the system call is named
`renameat2` while on macOS it is named `renameatx_np` but the operation is
much the same: passing a specific flag to the extended version of the rename
function causes it to swap the names of two existing files rather than just
changing the name of one file. On macOS the `renameatx_np` is exposed in the
standard C library and can be called directly. Not all Linux distributions expose
the `renameat2` system call in their C library so the `syscall` wrapper function
is used instead.

While there is no equivalent single function to perform the same operation on
Windows, it is possible to perform an atomic swap operation using the Windows
[Kernel Transaction Manager](https://learn.microsoft.com/en-us/windows/win32/ktm/kernel-transaction-manager-portal) and
[Transactional NTFS](https://learn.microsoft.com/en-us/windows/win32/fileio/transactional-ntfs-portal).
Unfortunately Microsoft have stated that _"TxF may not be available in future versions of 
Microsoft Windows"_, which potentially limits the utility of this sort of
implementation. The implementation here is untested because I don't have a
Windows system on which to test it.


## License

`atomicswap` is released under the MIT license. See LICENSE.md for details.
