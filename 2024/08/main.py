from collections import defaultdict
from itertools import count
from tqdm import tqdm


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


def part2_layers(num):
    counter = 1
    for i in count(start=1):
        yield i, counter
        counter *= num
        counter %= 1111 if not TEST else 5


def task2(txt: str, task_nr: int):
    num = int(txt) if not TEST else 3
    available_blocks = 20240000 if not TEST else 50
    volume = 0
    for i, thickness in part2_layers(num):
        width = 2 * i - 1
        volume += thickness * width
        if volume > available_blocks:
            break
    return (volume - available_blocks) * width


def print_nice(d):
    xs = sorted(d.keys())
    for x in xs:
        print(f"{d[x]:3}", end=" ")
    print()


def part3_layers(num):
    counter = 1
    for i in count(start=0):
        yield i, counter
        counter *= num
        counter %= 10 if not TEST else 5
        counter += 10 if not TEST else 5


TEST = False


def task3(txt: str, task_nr: int):
    num = int(txt) if not TEST else 2
    heights = defaultdict(int)
    heights[0] = 0

    available_blocks = 202400000000 if not TEST else 160
    volume = 0
    for i, thickness in tqdm(part3_layers(num)):
        # print(thickness)
        width = 2 * i - 1
        volume += thickness * width
        if volume > available_blocks:
            break
        for x in range(-i, i + 1):
            heights[x] += thickness
        # print_nice(heights)

    # Remove
    empties = {}
    width = len(heights)
    for col_i, col_h in heights.items():
        if abs(col_i) == width // 2:
            # print(col_i)
            empties[col_i] = 0
            continue
        empty = (width * num * col_h) % (10 if not TEST else 5)
        empties[col_i] = empty
    # print("Empties")
    # print(empties.values())
    return (volume - available_blocks) * width - available_blocks


def all_tris():
    total = 1
    width = 1
    for i in count(start=1):
        yield i, width, total
        width += 2
        total += width


def task1(txt: str, task_nr: int):
    num = int(txt)
    for i, width, tri in all_tris():
        print(tri)
        if tri >= num:
            break
    return (tri - num) * width


def main():
    # for task_nr in range(1, 4):
    # task_nr = 1
    # task_input = open(f"round{task_nr}.txt", "r").read().strip()
    # print(f"Part {task_nr}:", task1(task_input, task_nr))
    # task_nr = 2
    # task_input = open(f"round{task_nr}.txt", "r").read().strip()
    # print(f"Part {task_nr}:", task2(task_input, task_nr))
    task_nr = 3
    task_input = open(f"round{task_nr}.txt", "r").read().strip()
    print(f"Part {task_nr}:", task3(task_input, task_nr))


if __name__ == "__main__":
    main()
