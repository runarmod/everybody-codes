import os
import time

from ecd import get_inputs, submit

EVENT = 2025
QUEST = None

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """""",
    """""",
    """""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    return None
    data = get_input(1, test)


def part2(test: bool = False):
    return None
    data = get_input(2, test)


def part3(test: bool = False):
    return None
    data = get_input(3, test)


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
