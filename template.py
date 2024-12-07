import time


def get_input(part: int):
    return open(f"round{part}.txt", "r").read().strip()


def part1():
    data = """"""
    data = get_input(1).split("\n")  # noqa: F841


def part2():
    data = """"""
    data = get_input(2).split("\n")  # noqa: F841


def part3():
    data = """"""
    data = get_input(3).split("\n")  # noqa: F841


def main():
    start = time.perf_counter()
    print("Part 1:", part1())
    print("Part 2:", part2())
    print("Part 3:", part3())
    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
