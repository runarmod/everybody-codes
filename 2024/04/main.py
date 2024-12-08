import time


def get_input(part: int):
    return open(f"round{part}.txt", "r").read().strip()


def part1():
    data = list(map(int, get_input(1).split("\n")))
    m = min(data)
    return sum(n - m for n in data)


def part2():
    data = list(map(int, get_input(2).split("\n")))
    m = min(data)
    return sum(n - m for n in data)


def part3():
    data = list(map(int, get_input(3).split("\n")))
    best = float("inf")
    for h in range(min(data), max(data) + 1):
        best = min(best, sum(abs(h - n) for n in data))
    return best


def main():
    start = time.perf_counter()
    print("Part 1:", part1())
    print("Part 2:", part2())
    print("Part 3:", part3())
    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
