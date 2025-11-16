import time
from collections import Counter

from ecd import get_inputs

EVENT = 2025
QUEST = 3

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """10,5,1,10,3,8,5,2,2""",
    """4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,48,61,14,40,77""",
    """4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,48,61,14,40,77""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    return sum(set(map(int, get_input(1, test).split(","))))


def part2(test: bool = False):
    return sum(sorted(set(map(int, get_input(2, test).split(","))))[:20])


def part3(test: bool = False):
    return Counter(map(int, get_input(3, test).split(","))).most_common(1)[0][1]


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
