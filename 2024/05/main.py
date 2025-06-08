import time
from collections import Counter
from itertools import count

test_inputs = [
    """2 3 4 5
3 4 5 2
4 5 2 3
5 2 3 4""",
    """2 3 4 5
6 7 8 9""",
    """2 3 4 5
6 7 8 9""",
]


def get_input(part: int, test: bool = False) -> str:
    raw_data = (
        test_inputs[part - 1] if test else open(f"round{part}.txt", "r").read().strip()
    )
    return list(
        map(
            list,
            zip(*[[int(x) for x in line.split()] for line in raw_data.split("\n")]),
        )
    )


def move_clapper(cols, col_count, round):
    clapper = cols[round % col_count].pop(0)
    target_col_id = (round + 1) % col_count
    target_col = cols[target_col_id]
    position = (clapper - 1) % (2 * len(target_col))
    if position >= len(target_col):
        position = 2 * len(target_col) - position
    target_col.insert(position, clapper)


def shout(cols):
    return int("".join(map(str, (col[0] for col in cols))))


def part1(test: bool = False):
    cols = get_input(1, test)

    col_count = len(cols)
    for round in range(10):
        move_clapper(cols, col_count, round)

    return shout(cols)


def part2(test: bool = False):
    cols = get_input(2, test)

    shout_counts = Counter()
    col_count = len(cols)
    for round in count():
        move_clapper(cols, col_count, round)

        shouting = shout(cols)
        shout_counts[shouting] += 1
        shount_count = shout_counts[shouting]
        if shount_count == 2024:
            return (round + 1) * shouting


def part3(test: bool = False):
    cols = get_input(3, test)

    seen = {}
    col_count = len(cols)
    for round in count():
        move_clapper(cols, col_count, round)

        frozen = tuple(map(tuple, cols))
        if frozen in seen:
            return max(seen.values())

        seen[frozen] = shout(cols)


def main():
    start = time.perf_counter()
    for test in [True, False]:
        print(f"{['', '(TEST) '][test]}Part 1:", part1(test))
        print(f"{['', '(TEST) '][test]}Part 2:", part2(test))
        print(f"{['', '(TEST) '][test]}Part 3:", part3(test))
        print()
    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
