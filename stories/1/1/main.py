import re
import time


def get_input(part: int):
    return open(f"round{part}.txt", "r").read().strip()


def eni(N, EXP, MOD):
    s = 1
    remainder_list = []
    for _ in range(EXP):
        s = (s * N) % MOD
        remainder_list.append(s)
    return int("".join(map(str, remainder_list[::-1])))


def part1(test):
    data = """A=4 B=4 C=6 X=3 Y=4 Z=5 M=11
A=8 B=4 C=7 X=8 Y=4 Z=6 M=12
A=2 B=8 C=6 X=2 Y=4 Z=5 M=13
A=5 B=9 C=6 X=8 Y=6 Z=8 M=14
A=5 B=9 C=7 X=6 Y=6 Z=8 M=15
A=8 B=8 C=8 X=6 Y=9 Z=6 M=16"""
    if test:
        data = [list(map(int, re.findall(r"\d+", line))) for line in data.split("\n")]
    else:
        data = [
            list(map(int, re.findall(r"\d+", line)))
            for line in get_input(1).split("\n")
        ]
    best = 0
    for line in data:
        s = 0
        for a, b in zip(line[:3], line[3:]):
            s += eni(a, b, line[-1])
        best = max(best, s)
    return best


def eni_opti(N, EXP, MOD, last_n=5):
    remainder_list = []
    for i in range(last_n):
        s = pow(N, EXP - i, MOD)
        remainder_list.append(s)
    return int("".join(map(str, remainder_list)))


def part2(test):
    data = """A=3657 B=3583 C=9716 X=903056852 Y=9283895500 Z=85920867478 M=188
A=6061 B=4425 C=5082 X=731145782 Y=1550090416 Z=87586428967 M=107
A=7818 B=5395 C=9975 X=122388873 Y=4093041057 Z=58606045432 M=102
A=7681 B=9603 C=5681 X=716116871 Y=6421884967 Z=66298999264 M=196
A=7334 B=9016 C=8524 X=297284338 Y=1565962337 Z=86750102612 M=145"""
    if test:
        data = [list(map(int, re.findall(r"\d+", line))) for line in data.split("\n")]
    else:
        data = [
            list(map(int, re.findall(r"\d+", line)))
            for line in get_input(2).split("\n")
        ]
    best = 0
    for line in data:
        s = 0
        for a, b in zip(line[:3], line[3:]):
            s += eni_opti(a, b, line[-1], 5)
        best = max(best, s)
    return best


def sum_all_remainders(N, EXP, MOD):
    sum_remainders = 0
    exp = 0
    lookup = {}
    s = 1
    found = False
    while exp < EXP:
        exp += 1
        new_s = (s * N) % MOD
        sum_remainders += new_s

        if not found and new_s in lookup:
            prev_exp, prev_sum_remainders = lookup[new_s]
            loop_size = exp - prev_exp
            counts = (EXP - exp) // loop_size
            sum_remainders += counts * (sum_remainders - prev_sum_remainders)
            exp += counts * loop_size
            found = True
            s = new_s
            assert exp <= EXP
            continue

        lookup[new_s] = (exp, sum_remainders)
        s = new_s
    return sum_remainders


def part3(test):
    data = """A=3657 B=3583 C=9716 X=903056852 Y=9283895500 Z=85920867478 M=188
A=6061 B=4425 C=5082 X=731145782 Y=1550090416 Z=87586428967 M=107
A=7818 B=5395 C=9975 X=122388873 Y=4093041057 Z=58606045432 M=102
A=7681 B=9603 C=5681 X=716116871 Y=6421884967 Z=66298999264 M=196
A=7334 B=9016 C=8524 X=297284338 Y=1565962337 Z=86750102612 M=145"""
    if test:
        data = [list(map(int, re.findall(r"\d+", line))) for line in data.split("\n")]
    else:
        data = [
            list(map(int, re.findall(r"\d+", line)))
            for line in get_input(3).split("\n")
        ]
    best = 0
    for line in data:
        s = 0
        for a, b in zip(line[:3], line[3:]):
            s += sum_all_remainders(a, b, line[-1])
        best = max(best, s)
    return best


def main():
    start = time.perf_counter()
    for test in (1, 0):
        print(f"{['', '(TEST) '][test]}Part 1:", part1(test))
        print(f"{['', '(TEST) '][test]}Part 2:", part2(test))
        print(f"{['', '(TEST) '][test]}Part 3:", part3(test))
        print()
    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
