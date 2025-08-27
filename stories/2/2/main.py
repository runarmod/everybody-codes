import time
from collections import deque
from itertools import cycle

test_inputs = [
    """GRBGGGBBBRRRRRRRR""",
    """BBRGGRRGBBRGGBRGBBRRBRRRBGGRRRBGBGG""",
    """""",
]


def get_input(part: int, test: bool = False) -> str:
    data = open(f"round{part}.txt", "r").read() if not test else test_inputs[part - 1]
    return data.strip()


def part1(test: bool = False):
    data = deque(get_input(1, test))

    for s, c in enumerate(cycle("RGB"), start=1):
        # Bolt survives all ballons of the same color as it.
        while len(data) and data[0] == c:
            data.popleft()

        # If there is 0 ballons left, we are done.
        # If there is 1 balloon left, it will be popped and we are done.
        if len(data) <= 1:
            return s

        # Final balloon destroys bolt.
        data.popleft()


def part2(test: bool = False):
    data = deque(get_input(2, test) * 100)

    for s, c in enumerate(cycle("RGB"), start=1):
        # If the first balloon won't destroy the bolt,
        # and there is a balloon at the exact opposite side,
        # the opposite side is guaranteed to pop.
        if data[0] == c and len(data) % 2 == 0:
            del data[len(data) // 2]

        # The first balloon will always pop.
        data.popleft()

        if len(data) == 0:
            return s


def part3(test: bool = False):
    data = get_input(3, test) * 100_000
    half1, half2 = deque(data[: len(data) // 2]), deque(data[len(data) // 2 :])

    for s, c in enumerate(cycle("RGB")):
        if len(half1) == 0 and len(half2) == 0:
            return s

        popped = half1.popleft()

        if (len(half1) + 1 + len(half2)) % 2 != 0:
            # Bolt will go between ballons on other side,
            # so only the very first ballon popped.
            continue

        if popped == c:
            # Made it through the first ballon.
            # Will pop the other side as well guaranteed.
            half2.popleft()
            continue

        # Bolt didn't make it through the first ballon.
        # Rotate the opposite-side-ballon to the first half.
        half1.append(half2.popleft())


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
