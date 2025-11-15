import os
import re
import time

from ecd import get_inputs, submit

EVENT = 2025
QUEST = 2

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """A=[25,9]""",
    """A=[35300,-64910]""",
    """A=[35300,-64910]""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def loop(result: complex, divider: int, adder: complex) -> complex:
    result *= result
    result /= divider
    result = int(result.real) + int(result.imag) * 1j
    result += adder
    return result


def part1(test: bool = False):
    data = get_input(1, test)
    a = re.findall(r"-?\d+", data)
    a = int(a[0]) + int(a[1]) * 1j
    result = 0j + 0
    for _ in range(3):
        result = loop(result, 10, a)
    return f"[{int(result.real)},{int(result.imag)}]"


def part2(test: bool = False):
    data = get_input(2, test)
    corner = re.findall(r"-?\d+", data)
    corner = int(corner[0]) + int(corner[1]) * 1j

    s = 0
    for offset_x in range(0, 1001, 10):
        for offset_y in range(0, 1001, 10):
            point = corner + offset_x + offset_y * 1j
            result = 0j + 0
            for _ in range(100):
                result = loop(result, 100_000, point)
                if not (
                    -1000000 <= result.real <= 1000000
                    and -1000000 <= result.imag <= 1000000
                ):
                    break
            else:
                s += 1
    return s


def part3(test: bool = False):
    data = get_input(3, test)
    corner = re.findall(r"-?\d+", data)
    corner = int(corner[0]) + int(corner[1]) * 1j

    s = 0
    for offset_x in range(1001):
        for offset_y in range(1001):
            point = corner + offset_x + offset_y * 1j
            result = 0j + 0
            for _ in range(100):
                result = loop(result, 100_000, point)
                if not (
                    -1000000 <= result.real <= 1000000
                    and -1000000 <= result.imag <= 1000000
                ):
                    break
            else:
                s += 1
    return s


def main():
    start = time.perf_counter()
    print("(TEST) Part 1:", part1(test=True))
    print("(TEST) Part 2:", part2(test=True))
    print("(TEST) Part 3:", part3(test=True))
    print()

    answers = []
    answers.append(part1(test=False))
    print("Part 1:", answers[-1])
    answers.append(part2(test=False))
    print("Part 2:", answers[-1])
    answers.append(part3(test=False))
    print("Part 3:", answers[-1])
    print()

    total_time = time.perf_counter() - start

    for part, ans in enumerate(answers, start=1):
        if ans is None or os.path.exists(f"correct_part_{part}"):
            continue
        user_answer = input(f"Submit {part}: '{ans}'? (y/N) ").strip().lower()
        if user_answer != "y":
            continue
        resp = submit(event=EVENT, quest=QUEST, part=part, answer=ans)
        if resp.status == 200 and resp.json().get("correct"):
            os.close(os.open(f"correct_part_{part}", os.O_CREAT))

    print("Time:", total_time)


if __name__ == "__main__":
    main()
