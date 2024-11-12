from collections import deque


def neighbours(x, y, diag=False):
    for dx in (-1, 1):
        yield (x + dx, y)

    for dy in (-1, 1):
        yield (x, y + dy)

    if not diag:
        return

    for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        yield (x + dx, y + dy)


def task(txt: str, task_nr: int):
    txt = txt.split("\n")
    txt = [f".{line}." for line in txt]
    txt = ["." * len(txt[0])] + txt + ["." * len(txt[0])]

    WIDTH = len(txt[0])
    HEIGHT = len(txt)

    depth = {
        (x, y): 0 if txt[y][x] == "." else 1
        for y in range(HEIGHT)
        for x in range(WIDTH)
    }
    queue = deque()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if txt[y][x] == "#":
                queue.append((x, y))

    while len(queue):
        x, y = queue.popleft()
        if all(
            depth[(x, y)] <= depth[(nx, ny)]
            for nx, ny in neighbours(x, y, diag=task_nr == 3)
        ):
            depth[x, y] += 1
            queue.append((x, y))

    return sum(depth.values())


def main():
    for task_nr in range(1, 4):
        task_input = open(f"round{task_nr}.txt", "r").read().strip()
        print(f"Part {task_nr}:", task(task_input, task_nr))


if __name__ == "__main__":
    main()
