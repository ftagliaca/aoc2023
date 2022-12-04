from __future__ import annotations

import argparse
import os.path
from typing import Tuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def make_range(r: str) -> set:
    begin, end = map(int, r.split("-"))
    return set(range(begin, end + 1))


def get_assignment_ranges(line: str) -> Tuple[set, set]:
    r1, r2 = line.split(",")
    return (make_range(r1), make_range(r2))


def compute(s: str) -> int:
    n_overlap = 0
    lines = s.splitlines()
    for line in lines:
        s1, s2 = get_assignment_ranges(line)
        n_overlap += 1 if (s1 <= s2) or (s1 >= s2) else 0
    return n_overlap


INPUT_S = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
EXPECTED = 2


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
