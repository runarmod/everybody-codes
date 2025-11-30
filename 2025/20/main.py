import itertools
import time
from collections import deque

from ecd import get_inputs

EVENT = 2025
QUEST = 20

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """T#TTT###T##
.##TT#TT##.
..T###T#T..
...##TT#...
....T##....
.....#.....""",
    """TTTTTTTTTTTTTTTTT
.TTTT#T#T#TTTTTT.
..TT#TTTETT#TTT..
...TT#T#TTT#TT...
....TTT#T#TTT....
.....TTTTTT#.....
......TT#TT......
.......#TT.......
........S........""",
    """T####T#TTT##T##T#T#
.T#####TTTT##TTT##.
..TTTT#T###TTTT#T..
...T#TTT#ETTTT##...
....#TT##T#T##T....
.....#TT####T#.....
......T#TT#T#......
.......T#TTT.......
........TT#........
.........S.........""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def get_neighbor_coords(x: int, y: int):
    yield x - 1, y
    yield x + 1, y
    if (x + y) % 2 == 1:
        yield x, y + 1
    else:
        yield x, y - 1


def get_neighbor_trampolines(
    x: int, y: int, grid: list[str], include_self: bool = False
):
    for nx, ny in get_neighbor_coords(x, y):
        if nx in range(len(grid[0])) and ny in range(len(grid)):
            if grid[ny][nx] == "T":
                yield nx, ny
    if include_self and grid[y][x] == "T":
        yield x, y


def part1(test: bool = False):
    data = get_input(1, test).split("\n")
    connections: set[tuple[tuple[int, int], tuple[int, int]]] = (
        set()
    )  # The tuple is sorted with lowest coord first (to ensure no duplicates)
    for x, y in itertools.product(range(len(data[0])), range(len(data))):
        if data[y][x] != "T":
            continue
        for nx, ny in get_neighbor_trampolines(x, y, data):
            connections.add(tuple(sorted(((x, y), (nx, ny)))))
    return len(connections)


def part2(test: bool = False):
    data = get_input(2, test).split("\n")
    start = next(
        (x, y)
        for x, y in itertools.product(range(len(data[0])), range(len(data)))
        if data[y][x] == "S"
    )
    goal = next(
        (x, y)
        for x, y in itertools.product(range(len(data[0])), range(len(data)))
        if data[y][x] == "E"
    )
    data[start[1]] = data[start[1]][: start[0]] + "T" + data[start[1]][start[0] + 1 :]
    data[goal[1]] = data[goal[1]][: goal[0]] + "T" + data[goal[1]][goal[0] + 1 :]

    q = deque([(*start, 0)])
    visited: set[tuple[int, int]] = set()
    while True:
        x, y, dist = q.popleft()
        if (x, y) == goal:
            return dist
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for nx, ny in get_neighbor_trampolines(x, y, data):
            q.append((nx, ny, dist + 1))


def rotate(grid: list[str]):
    # See https://github.com/mkern75/EverybodyCodes/blob/738e04e3c36e51bcf228aac474968d737e1621b3/TheSongOfDucksAndDragons2025/q20.py#L80
    W, H = len(grid[0]), len(grid)
    grid_new = [["." for _ in range(W)] for _ in range(H)]
    for c in range(0, W, 2):
        rn = c // 2
        cn = W - 1 - c // 2
        for r in range(H):
            if r + c < W and grid[r][r + c] != ".":
                grid_new[rn][cn] = grid[r][r + c]
                cn -= 1
            if r + c + 1 < W and grid[r][r + c + 1] != ".":
                grid_new[rn][cn] = grid[r][r + c + 1]
                cn -= 1
    return ["".join(line) for line in grid_new]


def part3(test: bool = False):
    data = get_input(3, test).split("\n")

    start = next(
        (x, y)
        for x, y in itertools.product(range(len(data[0])), range(len(data)))
        if data[y][x] == "S"
    )

    data[start[1]] = data[start[1]][: start[0]] + "T" + data[start[1]][start[0] + 1 :]

    rotations = [data]
    rotations.append(rotate(rotations[-1]))
    rotations.append(rotate(rotations[-1]))

    goals = []
    for i in range(len(rotations)):
        goal = next(
            (x, y)
            for x, y in itertools.product(range(len(data[0])), range(len(data)))
            if rotations[i][y][x] == "E"
        )
        rotations[i][goal[1]] = (
            rotations[i][goal[1]][: goal[0]]
            + "T"
            + rotations[i][goal[1]][goal[0] + 1 :]
        )
        goals.append(goal)

    q = deque([(*start, 0, [start])])
    visited: set[tuple[int, int, int]] = set()
    while True:
        x, y, dist, path = q.popleft()
        if (x, y) == goals[dist % 3]:
            return dist
        if (x, y, dist % 3) in visited:
            continue
        visited.add((x, y, dist % 3))

        for nx, ny in get_neighbor_trampolines(
            x, y, rotations[(dist + 1) % 3], include_self=True
        ):
            q.append((nx, ny, dist + 1, path + [(nx, ny)]))


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
