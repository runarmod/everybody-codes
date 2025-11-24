import functools
import re
import time
from typing import Iterable

from ecd import get_inputs

EVENT = 2025
QUEST = 16

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """1,2,3,5,9""",
    """1,2,2,2,2,3,1,2,3,3,1,3,1,2,3,2,1,4,1,3,2,2,1,3,2,2""",
    """1,2,2,2,2,3,1,2,3,3,1,3,1,2,3,2,1,4,1,3,2,2,1,3,2,2""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def count_blocks(nums: Iterable[int], length: int):
    return sum(len(range(num - 1, length, num)) for num in nums)


def part1(test: bool = False):
    data = get_input(1, test)
    return count_blocks(map(int, re.findall(r"\d+", data)), 90)


def infer_used_blocks(nums: list[int]) -> list[int]:
    blocks = []
    for i in range(len(nums)):
        if nums[i] == 0:
            continue

        blocks.append(i + 1)
        for j in range(i, len(nums), i + 1):
            nums[j] -= 1

    return blocks


def part2(test: bool = False):
    data = get_input(2, test)
    nums = list(map(int, re.findall(r"\d+", data)))

    blocks = infer_used_blocks(nums)
    return functools.reduce(lambda a, b: a * b, blocks, 1)


def part3(test: bool = False):
    data = get_input(3, test)
    nums = list(map(int, re.findall(r"\d+", data)))

    block_count_num = 202520252025000
    blocks = infer_used_blocks(nums)

    # Binary search for length
    left, right = 1, 10**18
    while left < right:
        mid = (left + right) // 2
        count = count_blocks(blocks, mid)
        if count < block_count_num:
            left = mid + 1
        else:
            right = mid

    # I'm not 100% sure why I have off-by-one
    return left - 1


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
