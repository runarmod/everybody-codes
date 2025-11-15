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


def part1(test: bool = False):
    data = get_input(1, test)
    a = re.findall(r"-?\d+", data)
    a = [int(a[0]), int(a[1])]
    result = [0, 0]
    for _ in range(3):
        result = [result[0] ** 2 - result[1] ** 2, result[0] * result[1] * 2]
        result = [result[0] // 10, result[1] // 10]
        result = [result[0] + a[0], result[1] + a[1]]
    return f"[{result[0]},{result[1]}]"


def part2(test: bool = False):
    data = get_input(2, test)
    corner = re.findall(r"-?\d+", data)
    corner = [int(corner[0]), int(corner[1])]
    opposite_corner = [corner[0] + 1000, corner[1] + 1000]

    s = 0
    for point_x in range(corner[0], opposite_corner[0] + 1, 10):
        for point_y in range(corner[1], opposite_corner[1] + 1, 10):
            result = [0, 0]
            for _ in range(100):
                result = [result[0] ** 2 - result[1] ** 2, result[0] * result[1] * 2]
                result = [int(result[0] / 100000), int(result[1] / 100000)]
                result = [result[0] + point_x, result[1] + point_y]
                if not (
                    -1000000 <= result[0] <= 1000000
                    and -1000000 <= result[1] <= 1000000
                ):
                    break
            else:
                s += 1
    return s


def part3(test: bool = False):
    data = get_input(3, test)
    corner = re.findall(r"-?\d+", data)
    corner = [int(corner[0]), int(corner[1])]
    opposite_corner = [corner[0] + 1000, corner[1] + 1000]

    s = 0
    for point_x in range(corner[0], opposite_corner[0] + 1, 1):
        for point_y in range(corner[1], opposite_corner[1] + 1, 1):
            result_x, result_y = [0, 0]
            for _ in range(100):
                result_x, result_y = result_x**2 - result_y**2, result_x * result_y * 2
                result_x, result_y = int(result_x / 100000), int(result_y / 100000)
                result_x, result_y = result_x + point_x, result_y + point_y
                if not (
                    -1000000 <= result_x <= 1000000 and -1000000 <= result_y <= 1000000
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
