from __future__ import annotations

import argparse
import os.path
import re
from collections import defaultdict
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class CrateMove:
    n_crates: int
    move_from: int
    move_to: int

    def __init__(self, match: re.Match[str]):
        self.n_crates = int(match.group('crate_n'))
        self.move_from = int(match.group('move_from'))
        self.move_to = int(match.group('move_to'))


def parse_input(lines: list[str]) -> tuple[defaultdict[int, list[str]], list[CrateMove], int]:

    n_cols = (len(lines[0]) + 1)//4
    crate_stacks = defaultdict(list)
    move_orders = []

    move_re = re.compile(
        r'move (?P<crate_n>\d*) from (?P<move_from>\d*) to (?P<move_to>\d*)',
    )
    crate_s = ''.join([
        r'(\[(?P<crate_{}>\w*)\]|\s{}) '.format(i, '{3}')
        for i in range(1, n_cols+1)
    ])
    crate_s = crate_s[:-1]
    crate_re = re.compile(crate_s)

    for line in lines:
        if move_match := move_re.match(line):
            move_orders.append(CrateMove(move_match))
        elif crate_match := crate_re.match(line):
            for crate_n in range(1, n_cols+1):
                if crate_id := crate_match.group(f'crate_{crate_n}'):
                    crate_stacks[crate_n].append(crate_id)

    return crate_stacks, move_orders, n_cols


def compute(s: str) -> str:
    lines = s.splitlines()
    crate_stacks, move_orders, n_cols = parse_input(lines)

    for order in move_orders:
        for move_n in range(order.n_crates):
            to_move = crate_stacks[order.move_from].pop(0)
            crate_stacks[order.move_to].insert(0, to_move)

    return ''.join(crate_stacks[i][0] for i in range(1, n_cols+1))


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: str) -> None:
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
