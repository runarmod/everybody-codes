import re
import time
from itertools import cycle

from ecd import get_inputs

EVENT = 2026
QUEST = 3

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """ISO-3210 7654
ISO-8742 2468
ISO-1111 1111""",
    """ISO-3210 7654
ISO-8742 2468
ISO-1 1111
ISO-13 777
ISO-34 140856
ISO-789 2465112
ISO-2341 945""",
    """ISO2-3 23
ISO2-61 149
ISO2-978 99
ISO2-5887 5923
ISO2-76988 123749
ISO2-435657 929977
ISO2-3949 870737""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]
    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def calc_iso(part1, part2):
    a = 0
    for i, (n, e) in enumerate(zip(reversed(part2), cycle(reversed(part1)))):
        a += int(n) * int(e) ** i
    return a


def part1(test: bool = False):
    data = re.findall(r"ISO-(\d+) (\d+)", get_input(1, test))
    ans = 0
    for part1, part2 in data:
        ans += calc_iso(part1, part2)
    return ans


def part2(test: bool = False):
    data = re.findall(r"ISO-(\d+) (\d+)", get_input(2, test))
    ans = 0
    for part1, part2 in data:
        ans += calc_iso(part1, part2)
    return ans


def part3(test: bool = False):
    data = re.findall(r"ISO2-(\d+) (\d+)", get_input(3, test))
    ans = 0

    for part1, part2 in data:
        correct = calc_iso(part1, part2)

        for t_part2 in range(1, int(part2)):
            if calc_iso(part1, str(t_part2)) == correct:
                break
        else:
            ans += correct

    return ans


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

    total_time = time.perf_counter() - start
    print("Time:", total_time)


if __name__ == "__main__":
    main()
