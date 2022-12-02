from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def get_score(a: str, b: str) -> int:
    play_pts = ord(b) - 87
    opp_pts = ord(a) - 64
    score = ((play_pts - opp_pts + 1)%3)*3
    return score + play_pts

def compute(s: str) -> int:
    lines = s.splitlines()
    scores = []
    for line in lines:
        scores.append(get_score(*line.split()))
    return sum(scores)


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
