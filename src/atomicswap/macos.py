# Implement atomic file swap/exchange for Darwin (macOS).

# Copyright 2022 Nicko van Someren
# SPDX: MIT
# See LICENSE.md for the full license text.

from ctypes import CDLL, get_errno
from os import strerror

from typing import Union
from pathlib import PurePath

PathLike = Union[str, PurePath]

libc = CDLL("libc.dylib", use_errno=True)
swap_function = libc.renameatx_np
SWAP_FLAGS = 2
SWAP_AT_CWD = -2


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
    result = swap_function(
        first_dir_fd, str(first).encode(),
        second_dir_fd, str(second).encode(),
        SWAP_FLAGS
    )
    if result != 0:
        errno = get_errno()
        raise OSError(errno, strerror(errno))
