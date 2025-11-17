import itertools
import re
import time

from ecd import get_inputs
from PIL import Image

EVENT = 2025
QUEST = 2
VISUALIZE = True

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
    result = complex(int(result.real), int(result.imag))
    result += adder
    return result


def part1(test: bool = False):
    data = get_input(1, test)
    complex_num = complex(*map(int, re.findall(r"-?\d+", data)))
    result = 0j + 0
    for _ in range(3):
        result = loop(result, 10, complex_num)
    return f"[{int(result.real)},{int(result.imag)}]"


def is_valid(point: complex) -> bool:
    result = 0j + 0
    for _ in range(100):
        result = loop(result, 100_000, point)
        if not (
            -1000000 <= result.real <= 1000000 and -1000000 <= result.imag <= 1000000
        ):
            return False
    return True


def count_valid_points(
    corner: complex, width: int, step: int, image: Image.Image
) -> int:
    valid = 0
    for offset_x, offset_y in itertools.product(range(0, width, step), repeat=2):
        if is_valid(corner + offset_x + offset_y * 1j):
            valid += 1
            image.putpixel((offset_x // step, offset_y // step), 0)
    return valid


def part2(test: bool = False):
    data = get_input(2, test)
    corner = complex(*map(int, re.findall(r"-?\d+", data)))

    image = Image.new("1", (101, 101), "white")
    count = count_valid_points(corner, 1001, 10, image)
    if VISUALIZE:
        image.save(f"2025_02{'_test' if test else ''}_part2.png")
    return count


def part3(test: bool = False):
    data = get_input(3, test)
    corner = complex(*map(int, re.findall(r"-?\d+", data)))

    image = Image.new("1", (1001, 1001), "white")
    count = count_valid_points(corner, 1001, 1, image)
    if VISUALIZE:
        image.save(f"2025_02{'_test' if test else ''}_part3.png")
    return count


def main():
    start = time.perf_counter()
    print("(TEST) Part 1:", part1(test=True))
    print("(TEST) Part 2:", part2(test=True))
    print("(TEST) Part 3:", part3(test=True))
    print()

    print("Part 1:", part1(test=False))
    print("Part 2:", part2(test=False))
    print("Part 3:", part3(test=False))
    print()

    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
