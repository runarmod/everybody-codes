import os
import time

from ecd import get_inputs, submit

test_inputs = [
    """Vyrdax,Drakzyph,Fyrryn,Elarzris

R3,L2,R3,L1""",
    """Vyrdax,Drakzyph,Fyrryn,Elarzris

R3,L2,R3,L1""",
    """Vyrdax,Drakzyph,Fyrryn,Elarzris

R3,L2,R3,L3""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=2025, quest=1)[str(part)]


def part1(test: bool = False):
    things, moves = get_input(1, test).split("\n\n")
    things = things.split(",")
    moves = moves.split(",")
    moves = [(m[0], int(m[1:])) for m in moves]
    i = 0
    for direction, amount in moves:
        if direction == "R":
            i = min(len(things) - 1, max(0, (i + amount)))
        else:
            i = min(len(things) - 1, max(0, (i - amount)))
    return things[i]


def part2(test: bool = False):
    things, moves = get_input(2, test).split("\n\n")
    things = things.split(",")
    moves = moves.split(",")
    moves = [(m[0], int(m[1:])) for m in moves]
    i = 0
    for direction, amount in moves:
        if direction == "R":
            i = (i + amount) % len(things)
        else:
            i = (i - amount) % len(things)
    return things[i]


def part3(test: bool = False):
    things, moves = get_input(3, test).split("\n\n")
    things = things.split(",")
    moves = moves.split(",")
    moves = [(m[0], int(m[1:])) for m in moves]
    for direction, amount in moves:
        i = (amount * (1 if direction == "R" else -1)) % len(things)
        things[0], things[i] = things[i], things[0]
    return things[0]


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
        resp = submit(event=2025, quest=1, part=part, answer=ans)
        if resp.status == 200 and resp.json().get("correct"):
            os.close(os.open(f"correct_part_{part}", os.O_CREAT))

    print("Time:", total_time)


if __name__ == "__main__":
    main()
