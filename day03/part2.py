from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def get_priority(c: str) -> int:
    val = ord(c.swapcase()) - 64
    val -= 0 if val < 27 else 6
    return val

def compute(s: str) -> int:
    lines = s.splitlines()
    ret = 0
    for i, line in enumerate(lines[::3]):
        ii = i*3
        ie = ii + 3
        r1, r2, r3 = map(set, lines[ii:ie])
        common = r1.intersection(r2, r3)
        priority = [get_priority(c) for c in common]
        ret += sum(priority)
    return ret


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 70


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
