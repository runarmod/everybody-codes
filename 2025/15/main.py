import heapq
import time

from ecd import get_inputs
from PIL import Image

EVENT = 2025
QUEST = 15

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """L6,L3,L6,R3,L6,L3,L3,R6,L6,R6,L6,L6,R3,L3,L3,R3,R3,L6,L6,L3""",
    """""",
    """""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test).split(",")
    data = [(line[0], int(line[1:])) for line in data]
    return solve(data)


def part2(test: bool = False):
    data = get_input(2, test).split(",")
    data = [(line[0], int(line[1:])) for line in data]
    return solve(data)


def part3(test: bool = False):
    data = get_input(3, test).split(",")
    data = [(line[0], int(line[1:])) for line in data]

    return solve(data)


def solve(data: list[tuple[str, int]]):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direction_i = 0
    corners = [(0, 0)]

    xs = set([0])
    ys = set([0])

    pos = (0, 0)
    for direction, distance in data:
        direction_i = (direction_i + (direction == "R") - (direction == "L")) % len(
            directions
        )

        d = directions[direction_i]

        pos = (pos[0] + d[0] * distance, pos[1] + d[1] * distance)
        corners.append(pos)
        xs.add(pos[0])
        ys.add(pos[1])

        # Ensure we have space around walls
        xs.add(pos[0] + 1)
        xs.add(pos[0] - 1)
        ys.add(pos[1] + 1)
        ys.add(pos[1] - 1)

    goal = pos

    xs = sorted(xs)
    ys = sorted(ys)

    x_to_compressed = {x: i for i, x in enumerate(xs)}
    y_to_compressed = {y: i for i, y in enumerate(ys)}

    compressed_grid = [[" " for _ in range(len(xs))] for _ in range(len(ys))]

    image = Image.new("RGB", (len(xs), len(ys)), "white")
    for c1, c2 in zip(corners, corners[1:]):
        x1, y1 = x_to_compressed[c1[0]], y_to_compressed[c1[1]]
        x2, y2 = x_to_compressed[c2[0]], y_to_compressed[c2[1]]
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                compressed_grid[y][x] = "#"
                image.putpixel((x, y), (0, 0, 0))

    image.putpixel((x_to_compressed[0], y_to_compressed[0]), (255, 0, 0))
    image.putpixel((x_to_compressed[goal[0]], y_to_compressed[goal[1]]), (0, 255, 0))

    compressed_grid[y_to_compressed[0]][x_to_compressed[0]] = "S"
    compressed_grid[y_to_compressed[goal[1]]][x_to_compressed[goal[0]]] = "E"

    q = [
        (
            0,
            x_to_compressed[0],
            y_to_compressed[0],
            [(x_to_compressed[0], y_to_compressed[0])],
        )
    ]
    while q:
        length, compressed_x, compressed_y, path = heapq.heappop(q)
        x, y = xs[compressed_x], ys[compressed_y]

        grid_value = compressed_grid[compressed_y][compressed_x]
        if grid_value == "E":
            for px, py in path:
                image.putpixel((px, py), (0, 0, 255))
            image.save("2025_15_solution.png")
            return length
        if grid_value != " " and grid_value != "S":
            continue

        # Mark as visited
        compressed_grid[compressed_y][compressed_x] = "V"

        for dx, dy in directions:
            nx, ny = compressed_x + dx, compressed_y + dy
            if not (nx in range(len(xs)) and ny in range(len(ys))):
                continue
            extra_cost = abs(xs[nx] - xs[compressed_x]) + abs(ys[ny] - ys[compressed_y])
            heapq.heappush(q, (length + extra_cost, nx, ny, path + [(nx, ny)]))


def main():
    start = time.perf_counter()
    print("(TEST) Part 1:", part1(test=True))
    print()

    print("Part 1:", part1(test=False))
    print("Part 2:", part2(test=False))
    print("Part 3:", part3(test=False))
    print()

    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
