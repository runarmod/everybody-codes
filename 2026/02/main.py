import re
import time

import networkx as nx
from ecd import get_inputs

EVENT = 2026
QUEST = 2

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """4<3 2<5 3>1 1>2 1<5 4<1 3>2 4<2 3>5 4<5
4>1 2>1 3>2 1<5 4>5 2<5 3>1 4>3 2<4 5<3
5>1 5>2 4>1 2<4 3>2 3<4 1>2 3>5 1<3 4>5""",
    """2<5 3>1 1>2 1<5 4<1 3>2 4<2 3>5 4<5
2>1 3>2 1<5 4>5 2<5 3>1 4>3 2<4 5<3
5>1 5>2 4>1 3>2 3<4 1>2 3>5 1<3 4>5""",
    """3>1 1>2 1<5 4<2 3>5
2>1 2<5 3>1 4>3 2<4 5<3
5>1 3<4 1>2 3>5""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]
    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def run(input: str) -> int:
    data = (re.findall(r"(\d+)([\<\>])(\d+)", line) for line in input.split("\n"))

    ans = 0
    for line in data:
        g = nx.DiGraph()
        for num1, dir, num2 in line:
            if dir == ">":
                g.add_edge(num1, num2)
            else:
                g.add_edge(num2, num1)
        ans += int("".join(nx.topological_sort(g)))

    return ans


def part1(test: bool = False):
    return run(get_input(1, test))


def part2(test: bool = False):
    return run(get_input(2, test))


def part3(test: bool = False):
    return run(get_input(3, test))


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
