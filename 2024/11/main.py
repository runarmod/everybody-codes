import time
from collections import Counter

from ecd import get_inputs
from more_itertools import minmax

EVENT = 2024
QUEST = 11

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """A:B,C
B:C,A
C:A""",
    """""",
    """A:B,C
B:C,A,A
C:A""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def parse_input(part: int, test: bool = False) -> dict[str, list[str]]:
    data = get_input(part, test)
    lines = (line.split(":") for line in data.split("\n"))
    return {k: v.split(",") for k, v in lines}


def get_final_population_size(rules: dict[str, list[str]], inital: str, gen_count: int):
    c = Counter()
    c[inital] += 1
    for _ in range(gen_count):
        nc = Counter()
        for k, vs in c.items():
            for nw in rules[k]:
                nc[nw] += vs
        c = nc
    return sum(c.values())


def part1(test: bool = False):
    rules = parse_input(1, test)
    return get_final_population_size(rules, "A", 4)


def part2(test: bool = False):
    if test:
        return -1

    rules = parse_input(2, test)
    return get_final_population_size(rules, "Z", 10)


def part3(test: bool = False):
    rules = parse_input(3, test)

    lo, hi = minmax(get_final_population_size(rules, k, 20) for k in rules)
    return hi - lo


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
