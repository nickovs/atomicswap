# Tests for atomicswap

import os
from atomicswap import swap


A_DUMMY = "AAAA"
B_DUMMY = "BBBB"


def test_swap_str(tmp_path):
    file_a = str(tmp_path / "a")
    file_b = str(tmp_path / "b")

    with open(file_a, "w") as fh:
        fh.write(A_DUMMY)
    with open(file_b, "w") as fh:
        fh.write(B_DUMMY)

    swap(file_a, file_b)

    a_contents = open(file_a).read()
    assert(a_contents == B_DUMMY)
    b_contents = open(file_b).read()
    assert(b_contents == A_DUMMY)


def test_swap_path(tmp_path):
    file_a = tmp_path / "a"
    file_b = tmp_path / "b"

    with open(file_a, "w") as fh:
        fh.write(A_DUMMY)
    with open(file_b, "w") as fh:
        fh.write(B_DUMMY)

    swap(file_a, file_b)

    a_contents = open(file_a).read()
    assert(a_contents == B_DUMMY)
    b_contents = open(file_b).read()
    assert(b_contents == A_DUMMY)


def test_relative_cwd(tmp_path):
    os.chdir(tmp_path)

    file_a = "a"
    file_b = "b"

    with open(file_a, "w") as fh:
        fh.write(A_DUMMY)
    with open(file_b, "w") as fh:
        fh.write(B_DUMMY)

    swap(file_a, file_b)

    a_contents = open(file_a).read()
    assert(a_contents == B_DUMMY)
    b_contents = open(file_b).read()
    assert(b_contents == A_DUMMY)


def test_relative_dir_fd(tmp_path):
    dir_a = tmp_path / "A"
    dir_b = tmp_path / "B"

    os.mkdir(dir_a)
    os.mkdir(dir_b)

    with open(dir_a / "a", "w") as fh:
        fh.write(A_DUMMY)
    with open(dir_b / "b", "w") as fh:
        fh.write(B_DUMMY)

    dir_a_fd = os.open(dir_a, os.O_RDONLY)
    dir_b_fd = os.open(dir_b, os.O_RDONLY)

    swap("a", "b", first_dir_fd=dir_a_fd, second_dir_fd=dir_b_fd)

    a_contents = open(dir_a / "a").read()
    assert(a_contents == B_DUMMY)
    b_contents = open(dir_b / "b").read()
    assert(b_contents == A_DUMMY)


def test_relative_dir_mixed(tmp_path):
    os.chdir(tmp_path)

    dir_a = tmp_path / "A"
    dir_b = tmp_path / "B"

    os.mkdir(dir_a)
    os.mkdir(dir_b)

    with open(dir_a / "a", "w") as fh:
        fh.write(A_DUMMY)
    with open(dir_b / "b", "w") as fh:
        fh.write(B_DUMMY)

    dir_a_fd = os.open(dir_a, os.O_RDONLY)
    dir_b_fd = os.open(dir_b, os.O_RDONLY)

    swap("a", "B/b", first_dir_fd=dir_a_fd)

    a_contents = open(dir_a / "a").read()
    assert(a_contents == B_DUMMY)
    b_contents = open(dir_b / "b").read()
    assert(b_contents == A_DUMMY)

    swap("A/a", "b", second_dir_fd=dir_b_fd)

    a_contents = open(dir_a / "a").read()
    assert(a_contents == A_DUMMY)
    b_contents = open(dir_b / "b").read()
    assert(b_contents == B_DUMMY)

    swap("a", dir_b / "b", first_dir_fd=dir_a_fd)

    a_contents = open(dir_a / "a").read()
    assert(a_contents == B_DUMMY)
    b_contents = open(dir_b / "b").read()
    assert(b_contents == A_DUMMY)

    swap(dir_a / "a", "b", second_dir_fd=dir_b_fd)

    a_contents = open(dir_a / "a").read()
    assert(a_contents == A_DUMMY)
    b_contents = open(dir_b / "b").read()
    assert(b_contents == B_DUMMY)
