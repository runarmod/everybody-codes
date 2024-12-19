from sympy import symbols
from sympy.solvers.diophantine import diophantine
from itertools import combinations
import sys


def neighbours4(x, y):
    return [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]


def neighbours8(x, y):
    return [
        (x, y - 1),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y - 1),
        (x + 1, y + 1),
    ]


STAMP_DOTS = [
    [1, 3, 5, 10],
    [1, 3, 5, 10, 15, 16, 20, 24, 25, 30],
    [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101],
]


def minCoins(coins, m, sum):
    # table[i] will be storing the minimum
    # number of coins required for i value.
    # So table[sum] will have result
    table = [0 for i in range(sum + 1)]

    # Base case (If given value sum is 0)
    table[0] = 0

    # Initialize all table values as Infinite
    for i in range(1, sum + 1):
        table[i] = sys.maxsize

    # Compute minimum coins required
    # for all values from 1 to sum
    for i in range(1, sum + 1):
        # Go through all coins smaller than i
        for j in range(m):
            if coins[j] <= i:
                sub_res = table[i - coins[j]]
                if sub_res != sys.maxsize and sub_res + 1 < table[i]:
                    table[i] = sub_res + 1

    if table[sum] == sys.maxsize:
        return -1

    return table[sum]


# def findMin(V, task_nr):
#     deno = STAMP_DOTS[task_nr - 1]
#     n = len(deno)
#     ans = []
#     i = n - 1
#     while i >= 0:
#         while V >= deno[i]:
#             V -= deno[i]
#             ans.append(deno[i])
#         i -= 1
#     return len(ans)


def task(txt: str, task_nr: int):
    txt = list(map(int, txt.split("\n")))
    return sum(
        minCoins(STAMP_DOTS[task_nr - 1], len(STAMP_DOTS[task_nr - 1]), V) for V in txt
    )


def main():
    for task_nr in range(1, 3):
        task_input = open(f"round{task_nr}.txt", "r").read().strip()
        print(f"Part {task_nr}:", task(task_input, task_nr))
    task_input = list(map(int, open(f"round{3}.txt", "r").read().strip().split("\n")))

    dots = STAMP_DOTS[-1]
    x, y = symbols("x, y", integer=True, positive=True)
    for num in task_input:
        for dot1, dot2 in combinations(dots, 2):
            for i in range(101):
                try:
                    a, b = next(iter(diophantine(dot1 * x + dot2 * y - i)))

                except StopIteration:
                    continue
    print(f"Part {3}:", 1)


if __name__ == "__main__":
    main()
