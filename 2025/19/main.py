import re
import time
from collections import defaultdict
from itertools import batched
from math import ceil

from ecd import get_inputs

EVENT = 2025
QUEST = 19

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """7,7,2
12,0,4
15,5,3
24,1,6
28,5,5
40,8,2""",
    """7,7,2
7,1,3
12,0,4
15,5,3
24,1,6
28,5,5
40,3,3
40,8,2""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def get_openings(data: str) -> dict[int, set[range]]:
    nums = batched(map(int, re.findall(r"-?\d+", data)), 3)
    openings = defaultdict(set)
    for x, y, size in nums:
        openings[x].add(range(y, y + size))
    return openings


def count_flaps(openings: dict[int, set[range]]) -> int:
    highest_xy = 0

    for x, ys in openings.items():
        lowest_y = min(r.start for r in ys)
        highest_xy = max(highest_xy, x + lowest_y)
    return ceil(highest_xy / 2)


def part1(test: bool = False):
    return count_flaps(get_openings(get_input(1, test)))


def part2(test: bool = False):
    return count_flaps(get_openings(get_input(2, test)))


def part3(test: bool = False):
    return count_flaps(get_openings(get_input(3, test)))


def main():
    start = time.perf_counter()
    print("(TEST) Part 1:", part1(test=True))
    print("(TEST) Part 2:", part2(test=True))
    print()

    print("Part 1:", part1(test=False))
    print("Part 2:", part2(test=False))
    print("Part 3:", part3(test=False))
    print()

    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
