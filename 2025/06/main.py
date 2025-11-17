import time

from ecd import get_inputs

EVENT = 2025
QUEST = 6


test_inputs = [
    """ABabACacBCbca""",
    """ABabACacBCbca""",
    """AABCBABCABCabcabcABCCBAACBCa""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test)
    data = "".join(filter(lambda c: c.lower() == "a", data))
    s = 0
    for i in range(len(data)):
        if not data[i].isupper():
            continue
        for j in range(i + 1, len(data)):
            if not data[j].islower():
                continue
            if data[i] != data[j].upper():
                continue
            s += 1
    return s


def part2(test: bool = False):
    data = get_input(2, test)
    s = 0
    for i in range(len(data)):
        if not data[i].isupper():
            continue
        for j in range(i + 1, len(data)):
            if not data[j].islower():
                continue
            if data[i] != data[j].upper():
                continue
            s += 1
    return s


def calc_pairs(data, size_range, outer_range):
    s = 0
    for i in outer_range:
        if data[i].isupper():
            continue
        for j in range(max(0, i - size_range), min(len(data), i + size_range + 1)):
            if data[j].islower():
                continue
            if data[i].lower() != data[j].lower():
                continue
            s += 1
    return s


def part3(test: bool = False):
    repeat = 1000
    size_range = 1000

    data = get_input(3, test)
    og_length = len(data)
    data = data * repeat

    # Not optimized for this case
    if size_range >= og_length:
        return calc_pairs(data, size_range, range(len(data)))

    # Optimized calculation
    s = 0
    # First segment
    s += calc_pairs(data, size_range, range(og_length))

    # Middle segments
    s += calc_pairs(data, size_range, range(og_length, og_length * 2)) * (repeat - 2)

    # Last segment
    s += calc_pairs(data, size_range, range(len(data) - og_length, len(data)))
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

    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
