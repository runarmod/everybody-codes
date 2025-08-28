STAMP_DOTS = [
    [1, 3, 5, 10],
    [1, 3, 5, 10, 15, 16, 20, 24, 25, 30],
    [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 50, 50, 74, 75, 100, 101],
]


def create_min_beetles(stamps, m, sum):
    # table[i] will be storing the minimum
    # number of stamps required for i value.
    # So table[sum] will have result
    table = [0 for _ in range(sum + 1)]

    # Base case (If given value sum is 0)
    table[0] = 0

    # Initialize all table values as Infinite
    for i in range(1, sum + 1):
        table[i] = float("inf")

    # Compute minimum stamps required
    # for all values from 1 to sum
    for i in range(1, sum + 1):
        # Go through all stamps smaller than i
        for j in range(m):
            if stamps[j] > i:
                continue
            sub_res = table[i - stamps[j]]
            if sub_res != float("inf") and sub_res + 1 < table[i]:
                table[i] = sub_res + 1

    return table


def task1(brightnesses: list[int], stamps: list[int]) -> int:
    return sum(
        create_min_beetles(stamps, len(stamps), brightness)[brightness]
        for brightness in brightnesses
    )


def task2(brightnesses: list[int], stamps: list[int]) -> int:
    # Same task with different brightnesses
    return task1(brightnesses, stamps)


def task3(brightnesses: list[int], stamps: list[int]) -> int:
    largest = max(brightnesses)
    beetle_table = create_min_beetles(stamps, len(stamps), largest + 1)

    s = 0
    for num in brightnesses:
        best = float("inf")
        mid = num // 2
        for bright1 in range(max(0, mid - 50), min(num - 1, mid + 51)):
            bright2 = num - bright1
            if not abs(bright1 - bright2) <= 100:
                continue

            score = beetle_table[bright1] + beetle_table[bright2]
            best = min(best, score)
        s += best

    return s


def main():
    def get_input(part: int):
        return list(map(int, open(f"round{part}.txt", "r").read().strip().splitlines()))

    print("Part 1:", task1(get_input(1), STAMP_DOTS[0]))
    print("Part 2:", task2(get_input(2), STAMP_DOTS[1]))
    print("Part 3:", task3(get_input(3), STAMP_DOTS[2]))


if __name__ == "__main__":
    main()
