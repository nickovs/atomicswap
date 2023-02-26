# atomicswap

# Copyright 2022 Nicko van Someren
# SPDX: MIT
# See LICENSE.md for the full license text.

"""
atomicswap provides a simple API to swap two files on a filesystem atomically.
This means that after making the call to swap files at paths A and B, ether the
contents of A will be the former contents of B and the contents of B will be the
former contents of A, or an error will have occurred and the files will be as
they were before. The exchange is done in such a way that this there will not be
any point during the swapping when another process would be able to change the
outcome (although of course another process might be able to do so immediately
before or after).
"""

from sys import platform

__version__ = "0.2.3"

if platform == "darwin":
    from .macos import swap
elif platform == "linux":
    from .linux import swap
elif platform == "win32":
    from .windows import swap
else:
    raise NotImplementedError(f"Platform '{platform} is not currently supported")

# exchange is just an alias for swap
exchange = swap

__all__ = ["__version__", "exchange", "swap"]
