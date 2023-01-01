# Implement atomic file swap/exchange for Linux.

# Copyright 2022 Nicko van Someren
# SPDX: MIT
# See LICENSE.md for the full license text.

from ctypes import CDLL, get_errno
from os import strerror, PathLike, fsencode

libc = CDLL("libc.so.6", use_errno=True)
syscall_function = libc.syscall
SYSCALL_RENAMEAT2 = 316
SWAP_FLAGS = 2
SWAP_AT_CWD = -100


def swap(
        first: PathLike, second: PathLike,
        *,
        first_dir_fd: int = SWAP_AT_CWD, second_dir_fd: int = SWAP_AT_CWD) -> None:
    """Atomically swap the files at the paths `first` and `second`. If either path is
    relative then these will be relative to the current working directory unless
    `first_dir_fd` and/or `second_dir_fd` are provided, in which case they must be
    file descriptors for directories from which the respective paths are relative.

    The function returns None, or raises an OSError is an error occurs.
    """
    result = syscall_function(
        SYSCALL_RENAMEAT2,
        first_dir_fd, fsencode(first),
        second_dir_fd, fsencode(second),
        SWAP_FLAGS
    )
    if result != 0:
        errno = get_errno()
        raise OSError(errno, strerror(errno))
