from __future__ import annotations
from attrs import define
import re


@define
class Draw:
    red: int
    blue: int
    green: int

    def __eq__(self, other: Draw) -> bool:
        return self.red == other.red and self.blue == other.blue and self.green == other.green
    
    def __lt__(self, other: Draw) -> bool:
        return (self.red, self.blue, self.green) < (other.red, other.blue, other.green)
    
    def __gt__(self, other: Draw) -> bool:
        return self.red > other.red or self.blue > other.blue or self.green > other.green

    @property
    def power(self) -> int:
        return self.red * self.blue * self.green

@define
class Game:
    game_id: int
    draws: list[Draw]

def parse_draw(s: str) -> Draw:
    r, g, b = 0, 0, 0
    for color in s.split(','):
        color = color.strip()
        if color.endswith('red'):
            r = int(color.split()[0])
        elif color.endswith('green'):
            g = int(color.split()[0])
        elif color.endswith('blue'):
            b = int(color.split()[0])
        else:
            raise ValueError(f'invalid color: {color!r}')
    
    return Draw(r, g, b)

def parse_game(s: str) -> Game:
    game_re = re.compile(r'Game (?P<game_id>\d+): (?P<draws>.*)')
    game_data = game_re.match(s)
    game_id = int(game_data['game_id'])
    draws = [parse_draw(draw) for draw in game_data['draws'].split(';')]
    return Game(game_id, draws)