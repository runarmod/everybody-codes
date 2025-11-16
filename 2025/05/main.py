import re
import time
from operator import itemgetter

from ecd import get_inputs

EVENT = 2025
QUEST = 5

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """58:5,3,7,8,9,10,4,5,7,8,8""",
    """1:2,4,1,1,8,2,7,9,8,6
2:7,9,9,3,8,3,8,8,6,8
3:4,7,6,9,1,8,3,7,2,2
4:6,4,2,1,7,4,5,5,5,8
5:2,9,3,8,3,9,5,2,1,4
6:2,4,9,6,7,4,1,7,6,8
7:2,3,7,6,2,2,4,1,4,2
8:5,1,5,6,8,3,1,8,3,9
9:5,7,7,3,7,2,3,8,6,7
10:4,1,9,3,8,5,4,3,5,5""",
    """1:7,1,9,1,6,9,8,3,7,2
2:6,1,9,2,9,8,8,4,3,1
3:7,1,9,1,6,9,8,3,8,3
4:6,1,9,2,8,8,8,4,3,1
5:7,1,9,1,6,9,8,3,7,3
6:6,1,9,2,8,8,8,4,3,5
7:3,7,2,2,7,4,4,6,3,1
8:3,7,2,2,7,4,4,6,3,7
9:3,7,2,2,7,4,1,6,3,7""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    _id, *nums = list(map(int, re.findall(r"\d+", get_input(1, test))))
    bone = [[None] * 3]
    for num in nums:
        for i in range(len(bone)):
            if bone[i][1] is None:
                bone[i][1] = num
                break
            if num < bone[i][1] and bone[i][0] is None:
                bone[i][0] = num
                break
            if num > bone[i][1] and bone[i][2] is None:
                bone[i][2] = num
                break
        else:
            bone = bone + [[None, num, None]]
    return "".join(map(str, (b for _, b, _ in bone)))


def part2(test: bool = False):
    worst, best = float("inf"), float("-inf")
    for bone_thing in get_input(2, test).strip().split("\n"):
        _id, *nums = list(map(int, re.findall(r"\d+", bone_thing)))
        bone = [[None] * 3]
        for num in nums:
            for i in range(len(bone)):
                if bone[i][1] is None:
                    bone[i][1] = num
                    break
                if num < bone[i][1] and bone[i][0] is None:
                    bone[i][0] = num
                    break
                if num > bone[i][1] and bone[i][2] is None:
                    bone[i][2] = num
                    break
            else:
                bone = bone + [[None, num, None]]
        value = int("".join(map(str, (b for _, b, _ in bone))))
        worst = min(worst, value)
        best = max(best, value)
    return best - worst


def part3(test: bool = False):
    comparables = []
    for bone_thing in get_input(3, test).strip().split("\n"):
        _id, *nums = list(map(int, re.findall(r"\d+", bone_thing)))
        bone = [[None] * 3]
        for num in nums:
            for i in range(len(bone)):
                if bone[i][1] is None:
                    bone[i][1] = num
                    break
                if num < bone[i][1] and bone[i][0] is None:
                    bone[i][0] = num
                    break
                if num > bone[i][1] and bone[i][2] is None:
                    bone[i][2] = num
                    break
            else:
                bone = bone + [[None, num, None]]

        spine = list(b for _, b, _ in bone)
        spine_quality = int("".join(map(str, spine)))
        rowwise_quality = []
        for row in bone:
            s = ""
            for n in row:
                if n is not None:
                    s += str(n)
            rowwise_quality.append(int(s))
        comparable = (spine_quality, rowwise_quality, _id)  # Sort priority
        comparables.append(comparable)

    comparables.sort(reverse=True)
    ids_ = list(map(itemgetter(-1), comparables))
    checksum = sum(ids_[i] * (i + 1) for i in range(len(ids_)))
    return checksum


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
