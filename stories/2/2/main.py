import time
from collections import deque
from itertools import cycle
from typing import Literal

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
        # Bolt survives all balloons of the same color as it.
        while len(data) and data[0] == c:
            data.popleft()

        # If there is 0 balloons left, we are done.
        # If there is 1 balloon left, it will be popped and we are done.
        if len(data) <= 1:
            return s

        # Final balloon destroys bolt.
        data.popleft()


def run_balloon_circle(data: list[Literal["R", "G", "B"]], repeat: int = 1) -> int:
    repeated_data = data * repeat
    (half1, half2) = (
        deque(repeated_data[: len(repeated_data) // 2]),
        deque(repeated_data[len(repeated_data) // 2 :]),
    )

    for s, c in enumerate(cycle("RGB")):
        if len(half1) == 0 and len(half2) == 0:
            return s

        popped = half1.popleft()

        if (len(half1) + 1 + len(half2)) % 2 != 0:
            # Bolt will go between balloons on other side,
            # so only the very first balloon popped.
            continue

        if popped == c:
            # Made it through the first balloon.
            # Will pop the other side as well guaranteed.
            half2.popleft()
            continue

        # Bolt didn't make it through the first balloon.
        # Rotate the opposite-side-balloon to the first half.
        half1.append(half2.popleft())


def part2(test: bool = False):
    return run_balloon_circle(get_input(2, test), 100)


def part3(test: bool = False):
    return run_balloon_circle(get_input(3, test), 100_000)


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
