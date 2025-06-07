import time

test_inputs = [
    """""",
    """""",
    """""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]
    return open(f"round{part}.txt", "r").read().strip()


def part1(test: bool = False):
    data = get_input(1, test)


def part2(test: bool = False):
    data = get_input(2, test)


def part3(test: bool = False):
    data = get_input(3, test)


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
