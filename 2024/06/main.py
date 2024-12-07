import time
from collections import defaultdict


def get_input(part: int):
    return open(f"round{part}.txt", "r").read().strip()


def get_paths(data: list[str]):
    graph = {}
    for line in data:
        root, nodes = line.split(":")
        nodes = nodes.split(",")
        graph[root] = nodes

    paths = {}

    def dfs(node: str, path: tuple[str]):
        path = tuple(list(path) + [node])
        if node not in graph:
            if node == "@":
                paths[path] = len(path)
            return  # dead end

        for neighbor in graph[node]:
            if neighbor not in path:
                dfs(neighbor, path)
        return

    dfs("RR", ())
    return paths


def get_best_path(paths: dict[int, list[str]], part: int):
    counter = defaultdict(list)
    for path in paths:
        counter[paths[path]].append(path)

    return next(
        "".join(map(lambda s: s[0], path[0]) if part != 1 else path[0])
        for path in counter.values()
        if len(path) == 1
    )


def run(part: int):
    data = get_input(part).split("\n")
    return get_best_path(get_paths(data), part)


def main():
    start = time.perf_counter()
    print("Part 1:", run(1))
    print("Part 2:", run(2))
    print("Part 3:", run(3))
    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
