import time
from collections import deque
from copy import copy
from itertools import cycle

from ecd import get_inputs

EVENT = 3
QUEST = 2

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """.......
.......
.......
.#.@...
.......
.......
.......""",
    """.......
.......
.......
.#.@...
.......
.......
.......""",
    """................................................................
.........................###.........###........................
....................##...###########.#####......#.......###.....
.........##.............############....####.............##.....
.......######..............#############.###....................
.........##................#############.###.......##...........
...............##...........########....####....................
...............................####.#######...........##........
........................##################...........####.......
....#.........#########################.....##......######......
..............#.##......##....##..##.##...............##........
..............................##....##..........##..............
........####....#################..######...................##..
........###.....###...####..###..##...##.########...............
.................####....###..##.##.##..###....##.....##........
....##...........#######.....##..##..##......#####..........#...
...........##......#########......#....##.######..........#####.
...........##........###########################....#.......#...
.........######............##################.......#...........
...........##.............#########.............................
............#.........#############....................#........
.....#...........##..####......###......##........#.............
.............##................###..........#.....#.............
..................##...........##...................##..........
..........................###.####.####.........................
................#.###########..###.############.#...............
.....#####....###...............................###.............
.....#####...#############......@......#############............
.....#########.###################################.#............
...###########..##.....###################.....##..##...........
...######...#######.##...###.........##...##...###.##...........
.....##.########........#####..###..####.......#.########.......
............#########################################...........
..............#####################################.............
...............................###..............................
................................................................""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test).splitlines()
    start = next(
        (x, y) for y, line in enumerate(data) for x, c in enumerate(line) if c == "@"
    )
    goal = next(
        (x, y) for y, line in enumerate(data) for x, c in enumerate(line) if c == "#"
    )
    visited = set()
    moves = 0
    location = start
    for direction in cycle("URDL"):
        if location == goal:
            return moves

        visited.add(location)

        dx = 1 if direction == "R" else -1 if direction == "L" else 0
        dy = 1 if direction == "D" else -1 if direction == "U" else 0
        next_location = (location[0] + dx, location[1] + dy)

        if next_location in visited:
            continue

        location = next_location
        moves += 1


def is_surrounded(
    location: tuple[int, int], walls: set[tuple[int, int]]
) -> tuple[bool, set[tuple[int, int]]]:
    visited = set()
    queue = deque([location])

    while queue:
        loc = queue.popleft()
        if loc in visited or loc in walls:
            continue
        visited.add(loc)
        if len(visited) > 100:
            return False, set()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_loc = (loc[0] + dx, loc[1] + dy)
            queue.append(next_loc)
    return True, visited


def part2(test: bool = False):
    data = get_input(2, test).splitlines()
    return run(data, "URDL")


def part3(test: bool = False):
    data = get_input(3, test).splitlines()
    return run(data, "UUURRRDDDLLL")


def run(data: list[str], direction_order: str) -> int:
    start = next(
        (x, y) for y, line in enumerate(data) for x, c in enumerate(line) if c == "@"
    )
    bones = {
        (x, y) for y, line in enumerate(data) for x, c in enumerate(line) if c == "#"
    }
    visited = copy(bones)

    # Fill surrounded areas between bones
    for bone in bones:
        x, y = bone
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            surrounded, points = is_surrounded((x + dx, y + dy), visited)
            if surrounded:
                visited |= points

    direction_map = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}
    moves = 0
    location = start
    for direction in cycle(direction_order):
        visited.add(location)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            surrounded, points = is_surrounded(
                (location[0] + dx, location[1] + dy), visited
            )
            if surrounded:
                visited |= points

        if all(
            (bone[0] + dx, bone[1] + dy) in visited
            for bone in bones
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        ):
            break

        dx, dy = direction_map[direction]
        next_location = (location[0] + dx, location[1] + dy)

        if next_location in visited:
            continue

        location = next_location
        moves += 1

    return moves


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

    total_time = time.perf_counter() - start

    print("Time:", total_time)


if __name__ == "__main__":
    main()
