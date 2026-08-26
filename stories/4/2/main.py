import re
import time
from collections import deque

from ecd import get_inputs
from PIL import Image

EVENT = 4
QUEST = 2

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """START=[5,0]
A=[0,0]
B=[10,0]
C=[5,10]
MOVES=ABCCBABCA""",
    """START=[5,0]
A=[0,0]
B=[10,0]
C=[5,10]
MOVES=BABCAABBCABCCCBBABCCCAAACABABCBCBBCAABBABBCACCBAABCBCBBBCBBBBBCCCAACAACB""",
    """START=[0,0]
A=[0,0]
B=[80,15]
C=[5,30]""",
]


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def coords_to_image(
    coords: set[tuple[int, int]],
    name: str,
    green_coords: set[tuple[int, int]] | None = None,
):
    all_coords = set(coords)
    if green_coords:
        all_coords |= green_coords

    if not all_coords:
        image = Image.new("RGB", (1, 1), "white")
        image.save(name + ".png")
        return image

    xs = [x for x, _ in all_coords]
    ys = [y for _, y in all_coords]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    image = Image.new("RGB", (max_x - min_x + 1, max_y - min_y + 1), "white")
    pixels = image.load()
    for x, y in coords:
        pixels[x - min_x, max_y - y] = (0, 0, 0)
    if green_coords:
        for x, y in green_coords:
            pixels[x - min_x, max_y - y] = (0, 255, 0)
    image.save(name + ".png")
    return image


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test).split("\n")
    start = nums(data[0])
    beacons = {"A": nums(data[1]), "B": nums(data[2]), "C": nums(data[3])}
    moves = data[4].split("=")[1]

    pos = start
    lights = {pos}
    for b in moves:
        curr = beacons[b]
        pos = (pos[0] + curr[0]) // 2, (pos[1] + curr[1]) // 2
        lights.add(pos)

    coords_to_image(lights, "part1" + ("_test" if test else ""))

    return len(lights)


def part2(test: bool = False):
    data = get_input(2, test).split("\n")
    start = nums(data[0])
    beacons = {"A": nums(data[1]), "B": nums(data[2]), "C": nums(data[3])}
    moves = data[4].split("=")[1]

    pos = start
    lights = {pos}
    for b in moves:
        curr = beacons[b]
        pos = (pos[0] + curr[0]) // 2, (pos[1] + curr[1]) // 2
        lights.add(pos)

    new_lights = set()
    for light in lights:
        new_lights.add((light[0] + 1, light[1]))
        new_lights.add((light[0] - 1, light[1]))
        new_lights.add((light[0], light[1] + 1))
        new_lights.add((light[0], light[1] - 1))

    coords_to_image(
        lights, "part2" + ("_test" if test else ""), green_coords=new_lights - lights
    )

    return len(new_lights - lights)


def part3(test: bool = False):
    data = get_input(3, test).split("\n")
    start = nums(data[0])
    beacons = {"A": nums(data[1]), "B": nums(data[2]), "C": nums(data[3])}

    lights = {start}
    q = deque([start])
    while q:
        # For each posible possition for the swarm...
        pos = q.popleft()
        for beacon in beacons.values():
            # ... navigate to each of the beacons...
            new_pos = (pos[0] + beacon[0]) // 2, (pos[1] + beacon[1]) // 2
            if new_pos not in lights:
                # ... iteratively
                q.append(new_pos)
            lights.add(new_pos)

    new_lights = set()
    for light in lights:
        new_lights.add((light[0] + 1, light[1]))
        new_lights.add((light[0] - 1, light[1]))
        new_lights.add((light[0], light[1] + 1))
        new_lights.add((light[0], light[1] - 1))

    coords_to_image(
        lights, "part3" + ("_test" if test else ""), green_coords=new_lights - lights
    )

    return len(new_lights - lights)


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

    total_time = time.perf_counter() - start

    print("Time:", total_time)


if __name__ == "__main__":
    main()
