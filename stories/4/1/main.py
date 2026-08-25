import time

from ecd import get_inputs

EVENT = 4
QUEST = 1

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """1,1,1,1,1
5,1,2,3,4,5,1,2,3,4
2,1,1,2,1,1,2,1,1,2,1,1
5,1,2,1,2,7,1,2,1,2,7,1,2,1,2"""
] * 3


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test)
    s = 0
    for a in data.split("\n"):
        c = 0
        visited = set()
        for b in a.split(","):
            x = int(b)
            if c - x > 0 and c - x not in visited:
                c -= x
            else:
                c += x
            visited.add(c)
        s += c
    return s


def part2(test: bool = False):
    data = get_input(2, test)
    s = 0
    for a in data.split("\n"):
        c = 0
        visited = set()
        for b in a.split(","):
            x = int(b)
            if c - x > 0 and c - x not in visited:
                c -= x
            else:
                while c + x in visited:
                    x += 1
                c += x
            visited.add(c)
        s += c
    return s


def part3(test: bool = False):
    data = get_input(3, test)
    s = 0
    for a in data.split("\n"):
        c = 0
        even_jumps = set()
        odd_jumps = set()
        visited = {0}
        even = True

        def valid_jump(lo1, hi1, jumps, actual_to) -> bool:
            if actual_to < 0:
                return False
            if actual_to in visited:
                return False

            for lo2, hi2 in jumps:
                if not (lo2 < lo1 < hi2) and (lo2 < hi1 < hi2):
                    return False
                if (lo2 < lo1 < hi2) and not (lo2 < hi1 < hi2):
                    return False
            return True

        for b in a.split(","):
            x = int(b)
            if valid_jump(c - x, c, even_jumps if even else odd_jumps, c - x):
                jumps = even_jumps if even else odd_jumps
                jumps.add((c - x, c))
                c -= x
                even = not even
            else:
                counter = 0
                while not valid_jump(
                    c, c + x, even_jumps if even else odd_jumps, c + x
                ):
                    if counter > 500:  # NOTE: Might need to be increased
                        break
                    x += 1
                    counter += 1
                else:
                    jumps = even_jumps if even else odd_jumps
                    jumps.add((c, c + x))
                    c += x
                    even = not even
            visited.add(c)
        s += c
    return s


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
