import os
import time

from ecd import get_inputs, submit

EVENT = 2024
QUEST = 12

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """.............
.C...........
.B......T....
.A......T.T..
=============""",
    """.............
.C...........
.B......H....
.A......T.H..
=============""",
    """""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def get_projectile_positions(power, start_pos):
    x, y = start_pos
    for _ in range(power):
        x += 1
        y -= 1
        yield (x, y)
    for _ in range(power):
        x += 1
        yield (x, y)
    while True:
        x += 1
        y += 1
        yield (x, y)


def get_letter_pos(part: int, test: bool = False):
    data = [[c for c in line] for line in get_input(part, test).split("\n")]

    letter_pos = {}
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c in "ABC":
                letter_pos[c] = x, y
            elif c.isalpha():
                letter_pos.setdefault(c, []).append((x, y))

    assert len(set(letter_pos.keys()) - set("ABCTH")) == 0
    assert letter_pos["A"][0] == letter_pos["B"][0] == letter_pos["C"][0], letter_pos
    assert letter_pos["A"][1] == letter_pos["B"][1] + 1 == letter_pos["C"][1] + 2
    return letter_pos


def ranking(x, _y):
    for y_offset in range(3):
        y = _y - y_offset
        if x < y:
            continue
        if x <= 2 * y:
            return (y_offset + 1) * y
        manhattan = x + y
        if manhattan % 3 == 0:
            return (y_offset + 1) * (manhattan // 3)


def calculate_score(letter_pos):
    h = letter_pos["A"][1]
    s = 0
    for hits_required, letter in enumerate("TH", start=1):
        if letter not in letter_pos:
            continue
        for x, y in letter_pos[letter]:
            s += hits_required * ranking(x - 1, h - y)
    return s


def part1(test: bool = False):
    return calculate_score(get_letter_pos(1, test))


def part2(test: bool = False):
    return calculate_score(get_letter_pos(2, test))


def part3(test: bool = False):
    data = get_input(3, test)
    print(data)


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
