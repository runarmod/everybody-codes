import time
from itertools import combinations

import networkx
from ecd import get_inputs

EVENT = 2025
QUEST = 9

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """1:CAAGCGCTAAGTTCGCTGGATGTGTGCCCGCG
2:CTTGAATTGGGCCGTTTACCTGGTTTAACCAT
3:CTAGCGCTGAGCTGGCTGCCTGGTTGACCGCG""",
    """1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG""",
    """1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = [a.split(":")[1] for a in get_input(1, test).split("\n")]

    s1, s2 = 0, 0
    for a, b, c in zip(*data):
        s1 += a == c
        s2 += b == c
    return s1 * s2


def is_child(parent1: str, parent2: str, child: str) -> bool:
    scores = [0, 0]
    for a, b, c in zip(parent1, parent2, child):
        if c != a and c != b:
            return 0
        scores[0] += a == c
        scores[1] += b == c
    return scores[0] * scores[1]


def part2(test: bool = False):
    data = [a.split(":")[1] for a in get_input(2, test).split("\n")]
    s = 0
    for i1, i2 in combinations(range(len(data)), 2):
        for i3 in range(len(data)):
            if i3 == i1 or i3 == i2:
                continue
            s += is_child(data[i1], data[i2], data[i3])
    return s


def part3(test: bool = False):
    data = [a.split(":")[1] for a in get_input(3, test).split("\n")]

    graph = networkx.Graph()
    for i1, i2 in combinations(range(len(data)), 2):
        for i3 in range(len(data)):
            if i3 == i1 or i3 == i2:
                continue
            if not is_child(data[i1], data[i2], data[i3]):
                continue
            graph.add_edge(i1 + 1, i2 + 1)
            graph.add_edge(i1 + 1, i3 + 1)
            graph.add_edge(i2 + 1, i3 + 1)
    return sum(max(networkx.connected_components(graph), key=len))


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
