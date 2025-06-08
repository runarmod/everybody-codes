import os
from collections import defaultdict
from itertools import count


def all_tris():
    total = 1
    width = 1
    for i in count(start=1):
        yield i, width, total
        width += 2
        total += width


def task1(txt: str, test: bool = False):
    num = int(txt) if not test else 13
    for i, width, tri in all_tris():
        if tri >= num:
            break
    return (tri - num) * width


def part2_layers(num, test: bool = False):
    counter = 1
    for i in count(start=1):
        yield i, counter
        counter *= num
        counter %= 1111 if not test else 5


def task2(txt: str, test: bool = False):
    num = int(txt) if not test else 3
    available_blocks = 20240000 if not test else 50
    volume = 0
    for i, thickness in part2_layers(num, test):
        width = 2 * i - 1
        volume += thickness * width
        if volume > available_blocks:
            break
    return (volume - available_blocks) * width


def part3_layers(num, test: bool = False):
    counter = 1
    for i in count(start=1):
        yield i, counter
        counter *= num
        counter %= 10 if not test else 5
        counter += 10 if not test else 5


def task3(txt: str, test: bool = False):
    num = int(txt) if not test else 2
    heights = defaultdict(int)
    heights[0] = 0

    available_blocks = 202400000 if not test else 160
    volume = 0
    for i, thickness in part3_layers(num, test):
        width = 2 * i - 1
        volume += thickness * width
        for x in range(-i + 1, i):
            heights[x] += thickness
        if volume > available_blocks:
            break

    # Remove
    empties = {}
    width = len(heights)
    edge_i = max(heights.keys())
    for col_i, col_h in heights.items():
        if abs(col_i) == edge_i:
            # Outer edges should not be empty
            empties[col_i] = 0
            continue
        empty = (width * num * col_h) % (10 if not test else 5)
        empties[col_i] = empty

    return volume - sum(empties.values()) - available_blocks


def main():
    for test in [True, False]:
        for task_nr in range(1, 4):
            task = [task1, task2, task3][task_nr - 1]
            task_input = (
                open(os.path.join(os.path.dirname(__file__), f"round{task_nr}.txt"))
                .read()
                .strip()
            )
            print(f"{'(TEST) ' if test else ''}Part {task_nr}:", task(task_input, test))
        print()


if __name__ == "__main__":
    main()
