import re
import time
from collections import defaultdict

test_inputs = [
    """2456:rrrrrr ggGgGG bbbbBB
7689:rrRrrr ggGggg bbbBBB
3145:rrRrRr gggGgg bbbbBB
6710:rrrRRr ggGGGg bbBBbB""",
    """2456:rrrrrr ggGgGG bbbbBB sSsSsS
7689:rrRrrr ggGggg bbbBBB ssSSss
3145:rrRrRr gggGgg bbbbBB sSsSsS
6710:rrrRRr ggGGGg bbBBbB ssSSss""",
    """15437:rRrrRR gGGGGG BBBBBB sSSSSS
94682:RrRrrR gGGggG bBBBBB ssSSSs
56513:RRRrrr ggGGgG bbbBbb ssSsSS
76346:rRRrrR GGgggg bbbBBB ssssSs
87569:rrRRrR gGGGGg BbbbbB SssSss
44191:rrrrrr gGgGGG bBBbbB sSssSS
49176:rRRrRr GggggG BbBbbb sSSssS
85071:RRrrrr GgGGgg BBbbbb SSsSss
44303:rRRrrR gGggGg bBbBBB SsSSSs
94978:rrRrRR ggGggG BBbBBb SSSSSS
26325:rrRRrr gGGGgg BBbBbb SssssS
43463:rrrrRR gGgGgg bBBbBB sSssSs
15059:RRrrrR GGgggG bbBBbb sSSsSS
85004:RRRrrR GgGgGG bbbBBB sSssss
56121:RRrRrr gGgGgg BbbbBB sSsSSs
80219:rRRrRR GGGggg BBbbbb SssSSs""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]
    return open(f"round{part}.txt", "r").read().strip()


def value_of_color(c: str) -> int:
    if not c:
        return 0
    rest, last = c[:-1], c[-1]
    return value_of_color(rest) * 2 + last.isupper()


def part1(test: bool = False):
    data = get_input(1, test).splitlines()
    s = 0
    for line in data:
        _id, r, g, b = re.split(r"[:\s]+", line)
        values = list(map(value_of_color, (r, g, b)))
        if values[0] < values[1] > values[2]:
            s += int(_id)
    return s


def part2(test: bool = False):
    data = get_input(2, test).splitlines()

    best = (0, 0, 0)  # (shine, -darkness, _id)
    for line in data:
        _id, r, g, b, shine = re.split(r"[:\s]+", line)
        *values, shine_value = map(value_of_color, (r, g, b, shine))
        val = (shine_value, -sum(values), int(_id))
        if val > best:
            best = val

    return best[-1]


def part3(test: bool = False):
    data = get_input(3, test).splitlines()
    combined = defaultdict(list)
    for line in data:
        _id, r, g, b, shine = re.split(r"[:\s]+", line)
        *values, shine_value = map(value_of_color, (r, g, b, shine))

        dominant_color_value = max(values)
        if values.count(dominant_color_value) > 1:
            continue
        dominant = ["red", "green", "blue"][values.index(dominant_color_value)]

        if shine_value <= 30:
            combined[dominant + "-matte"].append(int(_id))
        if shine_value >= 33:
            combined[dominant + "-shiny"].append(int(_id))

    return sum(max(combined.values(), key=lambda x: len(x)))


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
