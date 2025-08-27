import time
from functools import lru_cache
from itertools import permutations

test_inputs = [
    """*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*...*..
.*.*.*.*.*...*.*.
*.*.....*...*.*.*
.*.*.*.*.*.*.*.*.
*...*...*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*
.*...*...*.*.*.*.
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.

RRRLRLRRRRRL
LLLLRLRRRRRR
RLLLLLRLRLRL
LRLLLRRRLRLR
LLRLLRLLLRRL
LRLRLLLRRRRL
LRLLLLLLRLLL
RRLLLRLLRLRR
RLLLLLRLLLRL""",
    """*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.
..*.*.*.*...*.*...*.*.*..
.*...*.*.*.*.*.*.....*.*.
*.*...*.*.*.*.*.*...*.*.*
.*.*.*.*.*.*.*.*.......*.
*.*.*.*.*.*.*.*.*.*...*..
.*.*.*.*.*.*.*.*.....*.*.
*.*...*.*.*.*.*.*.*.*....
.*.*.*.*.*.*.*.*.*.*.*.*.
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*...*.*.
*.*.*.*.*.*.*.*.*...*.*.*
.*.*.*.*.*.*.*.*.....*.*.
*.*.*.*.*.*.*.*...*...*.*
.*.*.*.*.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*.*.*.*.*
.*...*.*.*.*...*.*.*...*.
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.

RRRLLRRRLLRLRRLLLRLR
RRRRRRRRRRLRRRRRLLRR
LLLLLLLLRLRRLLRRLRLL
RRRLLRRRLLRLLRLLLRRL
RLRLLLRRLRRRLRRLRRRL
LLLLLLLLRLLRRLLRLLLL
LRLLRRLRLLLLLLLRLRRL
LRLLRRLLLRRRRRLRRLRR
LRLLRRLRLLRLRRLLLRLL
RLLRRRRLRLRLRLRLLRRL""",
    """*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*...*..
.*.*.*.*.*...*.*.
*.*.....*...*.*.*
.*.*.*.*.*.*.*.*.
*...*...*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*
.*...*...*.*.*.*.
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.

RRRLRLRRRRRL
LLLLRLRRRRRR
RLLLLLRLRLRL
LRLLLRRRLRLR
LLRLLRLLLRRL
LRLRLLLRRRRL""",
]


def get_input(part: int, test: bool = False) -> tuple[tuple[str], tuple[str]]:
    data = open(f"round{part}.txt", "r").read() if not test else test_inputs[part - 1]
    return tuple(tuple(line.split("\n")) for line in data.strip().split("\n\n"))


@lru_cache(maxsize=None)
def run(grid: tuple[str], moves: str, start_i: int):
    start_pos = 2 * start_i
    pos = start_pos
    y = 0
    moves_iter = iter(moves)

    while y < len(grid):
        move = next(moves_iter)
        y += 1
        pos += (move == "R") * 2 - 1

        if pos < 0:
            pos += 2
        if pos >= len(grid[0]):
            pos -= 2

        if y >= len(grid):
            break

        while y < len(grid) and grid[y][pos] != "*":
            y += 1
    return max(0, ((pos // 2 + 1) * 2) - (start_i + 1))


def part1(test: bool = False):
    grid, movess = get_input(1, test)
    score = 0
    for i, moves in enumerate(movess):
        score += run(grid, moves, i)
    return score


def part2(test: bool = False):
    score = 0
    grid, movess = get_input(2, test)
    for moves in movess:
        best_this_round = 0
        for i in range(len(grid[0]) // 2 + 1):
            best_this_round = max(best_this_round, run(grid, moves, i))
        score += best_this_round

    return score


def part3(test: bool = False):
    grid, movess = get_input(3, test)

    minimum, maximum = float("inf"), -1

    for slots in permutations(range(len(grid[0]) // 2 + 1), len(movess)):
        score = sum(run(grid, movess[i], slots[i]) for i in range(len(movess)))
        minimum, maximum = min(minimum, score), max(maximum, score)

    return f"{minimum} {maximum}"


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
