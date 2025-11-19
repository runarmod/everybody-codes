import re
import time

from ecd import get_inputs

EVENT = 2025
QUEST = 13

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """72
58
47
61
67""",
    """10-15
12-13
20-21
19-23
30-37""",
    """""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test)
    nums = list(map(int, re.findall(r"-?\d+", data)))
    wheel = [1] + [None] * len(nums)
    direction = 1
    for i, n in enumerate(nums):
        wheel[direction * (i // 2 + 1)] = n
        direction *= -1
    return wheel[2025 % len(wheel)]


def create_ranges(nums: list[int]) -> list[range]:
    nums = [range(a, b + 1) for a, b in zip(nums[::2], nums[1::2])]
    return nums


def create_wheel(nums: list[range]) -> list[range]:
    right = nums[::2]
    left = [range(r.stop - 1, r.start - 1, -1) for r in nums[1::2]]
    wheel = [range(1, 2)] + right + left[::-1]
    return wheel


def spin_wheel(ranges: list[range], index: int) -> int:
    total = sum(map(len, ranges))
    index = index % total

    s = 0
    for r in ranges:
        s += len(r)
        if s > index:
            too_far = s - index
            return list(r)[-too_far]
    return None


def part2(test: bool = False):
    data = get_input(2, test)
    nums = list(map(int, re.findall(r"\d+", data)))
    nums = create_ranges(nums)
    wheel = create_wheel(nums)

    return spin_wheel(wheel, 20252025)


def part3(test: bool = False):
    data = get_input(3, test)
    nums = list(map(int, re.findall(r"\d+", data)))
    nums = create_ranges(nums)
    wheel = create_wheel(nums)

    return spin_wheel(wheel, 202520252025)


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
