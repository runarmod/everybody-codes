import time
from enum import Enum
from functools import lru_cache

from ecd import get_inputs

EVENT = 2025
QUEST = 10

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """...SSS.......
.S......S.SS.
..S....S...S.
..........SS.
..SSSS...S...
.....SS..S..S
SS....D.S....
S.S..S..S....
....S.......S
.SSS..SS.....
.........S...
.......S....S
SS.....S..S..""",
    """...SSS##.....
.S#.##..S#SS.
..S.##.S#..S.
.#..#S##..SS.
..SSSS.#.S.#.
.##..SS.#S.#S
SS##.#D.S.#..
S.S..S..S###.
.##.S#.#....S
.SSS.#SS..##.
..#.##...S##.
.#...#.S#...S
SS...#.S.#S..""",
    """SSS.S
.....
#.#.#
.#.#.
#.D.#""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def get_reachable(x, y, w, h):
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for dx, dy in moves:
        if 0 <= x + dx < w and 0 <= y + dy < h:
            yield (x + dx, y + dy)


def part1(test: bool = False):
    data = get_input(1, test).split("\n")
    w, h = len(data[0]), len(data)
    s = 0
    move_count = 4 if not test else 3
    positions = [(w // 2, h // 2)]
    visited = set()
    for _ in range(move_count):
        new_positions = []
        for _ in range(len(positions)):
            x, y = positions.pop(0)
            for nx, ny in get_reachable(x, y, w, h):
                visited.add((nx, ny))
                new_positions.append((nx, ny))
        positions = new_positions

    for x, y in visited:
        if data[y][x] == "S":
            s += 1
    return s


def part2(test: bool = False):
    data = get_input(2, test).split("\n")
    w, h = len(data[0]), len(data)
    s = 0
    move_count = 20 if not test else 3
    positions = {((w // 2), (h // 2))}

    sheep_locations = {(x, y) for y in range(h) for x in range(w) if data[y][x] == "S"}
    hideout_locations = {
        (x, y) for y in range(h) for x in range(w) if data[y][x] == "#"
    }

    for _ in range(move_count):
        new_positions = set()
        for _ in range(len(positions)):
            x, y = positions.pop()
            for nx, ny in get_reachable(x, y, w, h):
                new_positions.add((nx, ny))
                if (nx, ny) in sheep_locations and (nx, ny) not in hideout_locations:
                    sheep_locations.remove((nx, ny))
                    s += 1
        sheep_locations = {(x, y + 1) for (x, y) in sheep_locations}
        positions = new_positions
        for x, y in positions:
            if (x, y) in sheep_locations and (x, y) not in hideout_locations:
                sheep_locations.remove((x, y))
                s += 1
    return s


class TO_MOVE(Enum):
    DRAGON = 1
    SHEEP = 2


def part3(test: bool = False):
    data = get_input(3, test).split("\n")
    w, h = len(data[0]), len(data)

    og_dragon = next((x, y) for y in range(h) for x in range(w) if data[y][x] == "D")
    og_sheep_locations = [
        (x, y) for y in range(h) for x in range(w) if data[y][x] == "S"
    ]
    hideout_locations = {
        (x, y) for y in range(h) for x in range(w) if data[y][x] == "#"
    }

    @lru_cache(None)
    def number_eatable_ways(
        dragon_pos: tuple[int, int],
        sheep_locs: frozenset[tuple[int, int]],
        to_move: TO_MOVE,
    ) -> int:
        if not sheep_locs:
            return 1
        if any(y >= h for _, y in sheep_locs):
            return 0
        if to_move == TO_MOVE.SHEEP:
            movable_sheep = [
                (x, y)
                for x, y in sheep_locs
                if (x, y + 1) != dragon_pos or (x, y + 1) in hideout_locations
            ]
            if not movable_sheep:
                return number_eatable_ways(dragon_pos, sheep_locs, TO_MOVE.DRAGON)
            ans = 0
            for sx, sy in movable_sheep:
                new_sheep = frozenset(
                    {item for item in sheep_locs if item != (sx, sy)} | {(sx, sy + 1)}
                )
                ans += number_eatable_ways(dragon_pos, new_sheep, TO_MOVE.DRAGON)
            return ans
        else:  # TO_MOVE.DRAGON
            ans = 0
            for nx, ny in get_reachable(dragon_pos[0], dragon_pos[1], w, h):
                if (nx, ny) in sheep_locs and (nx, ny) not in hideout_locations:
                    ans += number_eatable_ways(
                        (nx, ny), frozenset(sheep_locs - {(nx, ny)}), TO_MOVE.SHEEP
                    )
                else:
                    ans += number_eatable_ways((nx, ny), sheep_locs, TO_MOVE.SHEEP)
            return ans

    return number_eatable_ways(og_dragon, frozenset(og_sheep_locations), TO_MOVE.SHEEP)


def main():
    start = time.perf_counter()
    print("(TEST) Part 1:", part1(test=True))
    print("(TEST) Part 2:", part2(test=True))
    print("(TEST) Part 3:", part3(test=True))
    print()

    print("Part 1:", part1(test=False))
    print("Part 2:", part2(test=False))
    print("Part 3:", part3(test=False))
    print()

    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
