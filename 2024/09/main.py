STAMP_DOTS = [
    [1, 3, 5, 10],
    [1, 3, 5, 10, 15, 16, 20, 24, 25, 30],
    [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 50, 50, 74, 75, 100, 101],
]


def createMinCoinsTable(coins, m, sum):
    # table[i] will be storing the minimum
    # number of coins required for i value.
    # So table[sum] will have result
    table = [0 for i in range(sum + 1)]

    # Base case (If given value sum is 0)
    table[0] = 0

    # Initialize all table values as Infinite
    for i in range(1, sum + 1):
        table[i] = float("inf")

    # Compute minimum coins required
    # for all values from 1 to sum
    for i in range(1, sum + 1):
        # Go through all coins smaller than i
        for j in range(m):
            if coins[j] <= i:
                sub_res = table[i - coins[j]]
                if sub_res != float("inf") and sub_res + 1 < table[i]:
                    table[i] = sub_res + 1

    return table


def task(txt: str, task_nr: int):
    txt = list(map(int, txt.split("\n")))
    return sum(
        createMinCoinsTable(STAMP_DOTS[task_nr - 1], len(STAMP_DOTS[task_nr - 1]), V)[V]
        for V in txt
    )


def main():
    for task_nr in range(1, 3):
        task_input = open(f"round{task_nr}.txt", "r").read().strip()
        print(f"Part {task_nr}:", task(task_input, task_nr))

    task_input = list(map(int, open(f"round{3}.txt", "r").read().strip().split("\n")))

    dots = STAMP_DOTS[-1]
    largest = max(task_input)
    coins = createMinCoinsTable(dots, len(dots), largest + 1)

    s = 0
    for num in task_input:
        best = float("inf")
        mid = num // 2
        for dot1 in range(max(0, mid - 50), min(num - 1, mid + 51)):
            dot2 = num - dot1
            if not abs(dot1 - dot2) <= 100:
                continue
            score = coins[dot1] + coins[dot2]
            best = min(best, score)
        s += best

    print("Part 3:", s)


if __name__ == "__main__":
    main()
