# Implement atomic file swap/exchange for Windows.

# Copyright 2022 Nicko van Someren
# SPDX: MIT
# See LICENSE.md for the full license text.

from os import PathLike
from os.path import commonpath, join
from tempfile import TemporaryDirectory

from win32transaction import CreateTransaction, CommitTransaction
from win32file import MoveFileWithProgress


def swap(first: PathLike, second: PathLike) -> None:
    """Atomically swap the files at the paths `first` and `second`.

    The function returns None, or raises an OSError is an error occurs.
    """
    common = commonpath([first, second])
    with TemporaryDirectory(dir=common) as temp_dir:
        temp_path = join(temp_dir, "temp_file")

        handle = CreateTransaction()

        MoveFileWithProgress(first, temp_path, Transaction=handle)
        MoveFileWithProgress(second, first, Transaction=handle)
        MoveFileWithProgress(temp_path, second, Transaction=handle)

        CommitTransaction(handle)
        handle.close()
