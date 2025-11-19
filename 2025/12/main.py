import itertools
import time
from collections import deque
from copy import deepcopy

import tqdm
from ecd import get_inputs

EVENT = 2025
QUEST = 12

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """989601
857782
746543
766789""",
    """9589233445
9679121695
8469121876
8352919876
7342914327
7234193437
6789193538
6781219648
5691219769
5443329859""",
    """5411
3362
5235
3112""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def explode(
    start_x: int, start_y: int, exploded: set[tuple[int, int]], grid: list[list[int]]
) -> set[tuple[int, int]]:
    new_exploded = deepcopy(exploded)
    q = deque([(start_x, start_y)])
    w, h = len(grid[0]), len(grid)
    while q:
        x, y = q.popleft()
        if (x, y) in new_exploded:
            continue
        new_exploded.add((x, y))
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nx, ny = x + dx, y + dy
            if not (nx in range(w) and ny in range(h)):
                continue
            if grid[ny][nx] <= grid[y][x]:
                q.append((nx, ny))
    return new_exploded


def part1(test: bool = False):
    grid = [[int(c) for c in line] for line in get_input(1, test).split("\n")]

    return len(explode(0, 0, set(), grid))


def part2(test: bool = False):
    grid = [[int(c) for c in line] for line in get_input(2, test).split("\n")]

    exploded = set()
    for x, y in [(0, 0), (len(grid[0]) - 1, len(grid) - 1)]:
        exploded = explode(x, y, exploded, grid)
    return len(exploded)


def part3(test: bool = False):
    # ASSUMES THAT THERE IS ONLY ONE BEST WAY TO EXPLODE EACH TIME
    grid = [[int(c) for c in line] for line in get_input(3, test).split("\n")]
    w, h = len(grid[0]), len(grid)

    def get_val(pos):
        return grid[pos[1]][pos[0]]

    sorted_coords = sorted(
        # Would be very weird if the best move is to start at a position with value <= 3
        filter(lambda pos: get_val(pos) > 3, itertools.product(range(w), range(h))),
        key=get_val,
        reverse=True,
    )

    tot_exploded = set()
    for _ in range(3):
        cur_best_exploded = set()
        for x, y in tqdm.tqdm(sorted_coords):
            exploded = explode(x, y, tot_exploded, grid)
            if len(exploded) > len(cur_best_exploded):
                cur_best_exploded = exploded
        tot_exploded = cur_best_exploded
        sorted_coords = [pos for pos in sorted_coords if pos not in tot_exploded]
    return len(tot_exploded)


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
