from decimal import Decimal
import math
import re
import time

from ecd import get_inputs

EVENT = 2025
QUEST = 4

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """102
75
50
35
13""",
    """102
75
50
35
13""",
    """5
7|21
18|36
27|27
10|50
10|50
11""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = list(map(int, get_input(1, test).split("\n")))
    return math.floor(2025 * Decimal(data[0]) / Decimal(data[-1]))


def part2(test: bool = False):
    data = list(map(int, get_input(2, test).split("\n")))
    return math.ceil(10000000000000 / (Decimal(data[0]) / Decimal(data[-1])))


def part3(test: bool = False):
    first, *middle, last = list(map(int, re.findall(r"\d+", get_input(3, test))))
    multiplier = Decimal(first) / Decimal(last)
    for i in range(0, len(middle), 2):
        from_ = Decimal(middle[i])
        to_ = Decimal(middle[i + 1])
        multiplier *= to_ / from_
    return math.floor(100 * multiplier)


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
