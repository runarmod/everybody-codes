import math
import re
import time
from itertools import batched

from sympy.ntheory.modular import crt

test_inputs = [
    """x=1 y=2
x=2 y=3
x=3 y=4
x=4 y=4""",
    """x=3 y=1
x=3 y=9
x=1 y=5
x=4 y=10
x=5 y=3""",
    """""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]
    return open(f"round{part}.txt", "r").read().strip()


def score_snails(snails: set[tuple[int, int]]) -> int:
    score = 0
    for x, y in snails:
        score += (x + 1) + (y + 1) * 100
    return score


def extract_snail_positions(raw_input):
    return set(
        batched(
            map(lambda x: int(x) - 1, re.findall(r"(\d+)", raw_input)),
            2,
            strict=True,
        )
    )


def part1(test: bool = False):
    snails = extract_snail_positions(get_input(1, test))
    days = 100

    loop_times = set(sum(x) + 1 for x in snails)

    # Optimize the number of days to simulate by using the least common multiple
    # of the loop times of all snails.
    # Does not matter if days is small :(
    lcm = math.lcm(*loop_times)
    days -= lcm * (days // lcm)

    for _ in range(days):
        new_snails = set()
        for snail in snails:
            x, y = snail
            new_x, new_y = x + 1, y - 1
            if new_y < 0:
                new_x = 0
                new_y = x + y
            x, y = new_x, new_y
            new_snails.add((x, y))
        snails = new_snails
    return score_snails(snails)


def generate_moduli_and_residues(snails):
    moduli = []
    residues = []
    x, y = 0, 0
    while len(moduli) < len(snails):
        if (x, y) in snails:
            # For this snail, we have to travel y steps, then (x + y + 1) * n extra steps (for some n)
            moduli.append(x + y + 1)
            residues.append(y)
        x += 1
        y -= 1
        if y < 0:
            y = x + y + 1
            x = 0
    return moduli, residues


def part2(test: bool = False):
    snails = extract_snail_positions(get_input(2, test))
    moduli, residues = generate_moduli_and_residues(snails)
    return crt(moduli, residues)[0]


def part3(test: bool = False):
    if test:
        return "No test input for part 3"
    snails = extract_snail_positions(get_input(3, test))
    moduli, residues = generate_moduli_and_residues(snails)
    return crt(moduli, residues)[0]


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
