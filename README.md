# Atomic file swapping

Sadly, no, this is not a nuclear-powered utility to swap files. `atomicswap`
is a Python module that implements the swapping of two files no a filesystem
in a single operation that can't be broken up; either the entire operation
completes correctly or none of it completes. This prevents the filesystem
from being left in an inconsistent state and avoids certain race conditions.

The API is very simple; only a single function is provided: `swap()` The
function takes two file paths for the two files to be swapped. In the event
that either path is a relative path, you may also provide file descriptors
for directories that the relative paths should start from; if either is
missing then the path is relative to the current working directory. Paths
can be provided either as Python strings or `pathlib` paths.

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

Currently `atomicswap` supports Linux and macOS. A Windows version is a
possibility in the future.

## License

`atomicswap` is released under the 