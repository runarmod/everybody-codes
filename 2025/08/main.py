from itertools import combinations
import re
import time
from typing import Iterable

from ecd import get_inputs

EVENT = 2025
QUEST = 8

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """1,5,2,6,8,4,1,7,3""",
    """1,5,2,6,8,4,1,7,3,5,7,8,2""",
    """1,5,2,6,8,4,1,7,3,6""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test)
    nums = list(map(int, re.findall(r"-?\d+", data)))
    nails = 32 if not test else 8
    s = 0
    for n1, n2 in zip(nums, nums[1:]):
        if abs(n2 - n1) == (nails // 2):
            s += 1
    return s


def cross_count(s1: str, s2: str, strings: Iterable[tuple[int, int]]) -> int:
    s = 0
    for c1, c2 in strings:
        # One nail inside the others and one is not inside the others
        if (c1 < s1 < c2 and not (c1 <= s2 <= c2)) or (
            c1 < s2 < c2 and not (c1 <= s1 <= c2)
        ):
            s += 1
    return s


def part2(test: bool = False):
    data = get_input(2, test)
    nums = list(map(int, re.findall(r"-?\d+", data)))
    strings = set()
    s = 0
    for n1, n2 in zip(nums, nums[1:]):
        s += cross_count(n1, n2, strings)
        strings.add((min(n1, n2), max(n1, n2)))
    return s


def part3(test: bool = False):
    data = get_input(3, test)
    nums = list(map(int, re.findall(r"-?\d+", data)))
    nails = 256 if not test else 8
    strings = list()
    for n1, n2 in zip(nums, nums[1:]):
        strings.append((min(n1, n2), max(n1, n2)))

    best = 0
    for c1, c2 in combinations(range(1, nails + 1), r=2):
        c1, c2 = min(c1, c2), max(c1, c2)
        cut_count = cross_count(c1, c2, strings)
        if (c1, c2) in strings:
            cut_count += 1
        best = max(best, cut_count)
    return best


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
