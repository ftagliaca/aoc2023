from __future__ import annotations

import argparse
import os.path

import pytest

import support
import re

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIGIT_MAP = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}
re_str = 'zero|one|two|three|four|five|six|seven|eight|nine'
re_str_rev = re_str[::-1]

def compute(s: str) -> int:
    lines = s.splitlines()
    ret = 0
    for line in lines:
        res = re.search(fr'\d|{re_str}', line).group()
        res_rev = re.search(fr'\d|{re_str_rev}', line[::-1]).group()[::-1]
        r = res + res_rev
        r_s = re.sub(re_str, lambda x: DIGIT_MAP[x.group()], r)
        ret += int(r_s)
    return ret


INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
EXPECTED = 281


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
