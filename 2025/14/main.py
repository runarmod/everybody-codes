import itertools
import time

from ecd import get_inputs

EVENT = 2025
QUEST = 14

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """.#.##.
##..#.
..##.#
.#.##.
.###..
###.##""",
    """.#.##.
##..#.
..##.#
.#.##.
.###..
###.##""",
    """#......#
..#..#..
.##..##.
...##...
...##...
.##..##.
..#..#..
#......#""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def iterate(active: set[tuple[int, int]], w: int, h: int):
    new_active = set()
    for x, y in itertools.product(range(w), range(h)):
        n_active = 0
        for dx, dy in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            if (x + dx, y + dy) in active:
                n_active += 1

        if (x, y) in active:
            if n_active % 2 == 1:
                new_active.add((x, y))
        else:
            if n_active % 2 == 0:
                new_active.add((x, y))
    return new_active


def part_1_and_2(grid: list[str], rounds: int):
    w, h = len(grid[0]), len(grid)

    active = set()
    for x, y in itertools.product(range(w), range(h)):
        if grid[y][x] == "#":
            active.add((x, y))

    score = 0
    for _ in range(rounds):
        active = iterate(active, w, h)
        score += len(active)
    return score


def part1(test: bool = False):
    data = get_input(1, test).split("\n")
    return part_1_and_2(data, 10)


def part2(test: bool = False):
    data = get_input(2, test).split("\n")
    return part_1_and_2(data, 2025)


def is_special(entire: set[tuple[int, int]], special: list[str]) -> bool:
    for x, y in itertools.product(range(len(special[0])), range(len(special))):
        # TODO: Generalize offset
        if (
            special[y][x] == "#"
            and (x + 13, y + 13) not in entire
            or special[y][x] == "."
            and (x + 13, y + 13) in entire
        ):
            return False
    return True


def part3(test: bool = False):
    special = get_input(3, test).split("\n")
    w, h = 34, 34
    rounds = 1000000000

    active = set()
    seen: dict[frozenset, tuple[int, int]] = {}  # (round, score)
    score = 0

    round = 0
    while round < rounds:
        active = iterate(active, w, h)

        if is_special(active, special):
            score += len(active)

        fs = frozenset(active)
        if fs in seen:
            # Cycle detected
            old_round, old_score = seen[fs]
            cycle_length = round - old_round
            remaining_rounds = rounds - round
            cycles = remaining_rounds // cycle_length
            cycle_score = score - old_score
            score += cycle_score * cycles
            round += cycles * cycle_length
        else:
            seen[fs] = (round, score)

        round += 1

    return score


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
