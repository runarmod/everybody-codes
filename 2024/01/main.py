from itertools import batched


def task(string: str, sub_length: int):
    _map = {"A": 0, "B": 1, "C": 3, "D": 5, "x": 0}
    pairs = batched(string, sub_length)
    s = 0
    for chars in pairs:
        non_empty_count = sub_length - chars.count("x")
        s += sum(_map[char] for char in chars)
        s += (non_empty_count - 1) * non_empty_count
    return s


def main():
    for task_nr in range(1, 4):
        task_input = open(f"round{task_nr}.txt", "r").read().strip()
        print(f"Part {task_nr}:", task(task_input, task_nr))


if __name__ == "__main__":
    main()
