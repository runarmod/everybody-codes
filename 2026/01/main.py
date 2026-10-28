import math
import time

from ecd import get_inputs

EVENT = 2026
QUEST = 1

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """3,11,12,16,24,25""",
    """3,11,12,16,24,25""",
    """3,11,12,16,24,25""",
]


def part1(data: str, test: bool = False):
    ans = 0
    for num in map(int, data.split(",")):
        ans += math.ceil(math.sqrt(num)) ** 2 - num
    return ans


def to_frame(side_len):
    return (side_len - 1) * 4


def to_side(frame_count):
    return frame_count // 4 + 1


def part2(data: str, test: bool = False):
    ans = 0
    for num in map(int, data.split(",")):
        if num < 8:
            ans += 8 - num
            continue
        if to_frame(to_side(num)) == num:
            continue
        ans += to_frame(to_side(num) + 1) - num

    return ans


def part3(data: str, test: bool = False):
    ans = 0
    for num in map(int, data.split(",")):
        if num < 8:
            ans += 8 - num
            continue

        pretend_num = num + 1

        side_len = math.ceil(math.sqrt(pretend_num))
        if side_len % 2 != 1:
            side_len += 1

        ans += side_len**2 - (pretend_num)

    return ans


def main():
    start = time.perf_counter()
    print("(TEST) Part 1:", part1(test_inputs[0], test=True))
    print("(TEST) Part 2:", part2(test_inputs[1], test=True))
    print("(TEST) Part 3:", part3(test_inputs[2], test=True))
    print()

    inputs = get_inputs(event=EVENT, quest=QUEST)
    print("Part 1:", part1(inputs["1"], test=False))
    print("Part 2:", part2(inputs["2"], test=False))
    print("Part 3:", part3(inputs["3"], test=False))
    print()

    total_time = time.perf_counter() - start

    print("Time:", total_time)


if __name__ == "__main__":
    main()
