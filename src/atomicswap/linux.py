# Implement atomic file swap/exchange for Linux.

# Copyright 2022 Nicko van Someren
# SPDX: MIT
# See LICENSE.md for the full license text.

from ctypes import CDLL, get_errno
from os import strerror, PathLike, fsencode
from platform import machine

SYSCALL_ARCH_MAP = {
    "x86_64": 316,
    "armv7l": 382,
    "aarch64": 276,
    "i386": 353,
}

libc = CDLL("libc.so.6", use_errno=True)
syscall_function = libc.syscall
ARCH = machine()
SWAP_FLAGS = 2
SWAP_AT_CWD = -100

if ARCH not in SYSCALL_ARCH_MAP:
    raise NotImplementedError(f"Unsupported architecture: {ARCH}")

SYSCALL_RENAMEAT2 = SYSCALL_ARCH_MAP[ARCH]


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
