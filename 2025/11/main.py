from itertools import count
import re
import time

from ecd import get_inputs

EVENT = 2025
QUEST = 11

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """9
1
1
4
9
6""",
    """805
706
179
48
158
150
232
885
598
524
423""",
    """805
706
179
48
158
150
232
885
598
524
423""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test)
    nums = list(map(int, re.findall(r"-?\d+", data)))
    rounds = 10
    phase = 1
    for _ in range(rounds):
        something_happened = False
        if phase == 1:
            for i in range(len(nums) - 1):
                if nums[i] > nums[i + 1]:
                    nums[i + 1] += 1
                    nums[i] -= 1
                    something_happened = True
            if something_happened:
                continue
            phase = 2

        for i in range(len(nums) - 1):
            if nums[i] < nums[i + 1]:
                nums[i + 1] -= 1
                nums[i] += 1
    s = 0
    for i, num in enumerate(nums, start=1):
        s += i * num
    return s


def part2(test: bool = False):
    data = get_input(2, test)
    nums = list(map(int, re.findall(r"-?\d+", data)))
    phase = 1

    for round in count(start=1):
        something_happened = False
        if phase == 1:
            for i in range(len(nums) - 1):
                if nums[i] > nums[i + 1]:
                    nums[i + 1] += 1
                    nums[i] -= 1
                    something_happened = True
            if something_happened:
                continue
            phase = 2

        for i in range(len(nums) - 1):
            if nums[i] < nums[i + 1]:
                nums[i + 1] -= 1
                nums[i] += 1
        if all(num == nums[0] for num in nums):
            return round


def part3(test: bool = False):
    nums = list(map(int, re.findall(r"-?\d+", get_input(3, test))))
    assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), (
        "The code assumes that we do not need to do anything in phase 1."
    )

    mean = sum(nums) // len(nums)
    return sum(mean - num for num in nums if num < mean)


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
