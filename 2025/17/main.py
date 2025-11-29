import time
from itertools import product
from math import ceil

import networkx
from ecd import get_inputs

# from colorama import Back, Fore

EVENT = 2025
QUEST = 17

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """189482189843433862719
279415473483436249988
432746714658787816631
428219317375373724944
938163982835287292238
627369424372196193484
539825864246487765271
517475755641128575965
685934212385479112825
815992793826881115341
1737798467@7983146242
867597735651751839244
868364647534879928345
519348954366296559425
134425275832833829382
764324337429656245499
654662236199275446914
317179356373398118618
542673939694417586329
987342622289291613318
971977649141188759131""",
    """4547488458944
9786999467759
6969499575989
7775645848998
6659696497857
5569777444746
968586@767979
6476956899989
5659745697598
6874989897744
6479994574886
6694118785585
9568991647449""",
    """545233443422255434324
5222533434S2322342222
523444354223232542432
553522225435232255242
232343243532432452524
245245322252324442542
252533232225244224355
523533554454232553332
522332223232242523223
524523432425432244432
3532242243@4323422334
542524223994422443222
252343244322522222332
253355425454255523242
344324325233443552555
423523225325255345522
244333345244325322335
242244352245522323422
443332352222535334325
323532222353523253542
553545434425235223552""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test).split("\n")
    w, h = len(data[0]), len(data)
    mx, my = w // 2, h // 2
    s = 0
    for y in range(h):
        for x in range(w):
            if data[y][x] == "@":
                continue
            if (mx - x) ** 2 + (my - y) ** 2 <= 10**2:
                s += int(data[y][x])
    return s


def get_points_within_radius(data: list[str], radius: int):
    w, h = len(data[0]), len(data)
    mx, my = w // 2, h // 2
    points = []
    s = 0
    for y in range(h):
        for x in range(w):
            if data[y][x] == "@":
                continue
            if (mx - x) ** 2 + (my - y) ** 2 <= radius**2:
                points.append((x, y))
                s += int(data[y][x])
    return points, s


def part2(test: bool = False):
    data = get_input(2, test).split("\n")
    w, h = len(data[0]), len(data)
    radius = 0
    best = 0
    best_i = -1
    while any(data[y][x] != "@" for x in range(w) for y in range(h)):
        points, score = get_points_within_radius(data, radius)
        if score > best:
            best = score
            best_i = radius
        for x, y in points:
            data[y] = data[y][:x] + "@" + data[y][x + 1 :]

        radius += 1

    return best * best_i


def part3(test: bool = False):
    data = get_input(3, test).split("\n")
    w, h = len(data[0]), len(data)
    start = next((x, y) for y in range(h) for x in range(w) if data[y][x] == "S")
    start = tuple(map(int, start))
    data[start[1]] = data[start[1]][: start[0]] + "0" + data[start[1]][start[0] + 1 :]
    mx, my = w // 2, h // 2
    assert data[my][mx] == "@", "Assuming volcano is in the center"

    start_node = (start[0], start[1], 0)
    goal_node = (start[0], start[1], 3)
    graph = networkx.DiGraph()  # Nodes are (x, y, height)
    for x, y in product(range(w), range(h)):
        if data[y][x] == "@":
            continue
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if nx not in range(w) or ny not in range(h):
                continue
            if data[ny][nx] == "@":
                continue
            weight = int(data[ny][nx]) if data[ny][nx].isdigit() else 0
            for height in range(4):
                graph.add_edge((x, y, height), (nx, ny, height), weight=weight)
            if (
                x > mx and y == my and dx == 0 and dy == 1
            ):  # right side edge (downwards)
                graph.add_edge((x, y, 0), (nx, ny, 1), weight=weight)
            if x < mx and y == my and dx == 0 and dy == -1:  # left side edge (upwards)
                graph.add_edge((x, y, 2), (nx, ny, 3), weight=weight)
            if (
                x == mx and y > my and dx == -1 and dy == 0
            ):  # bottom side edge (leftwards)
                graph.add_edge((x, y, 1), (nx, ny, 2), weight=weight)

    volcano_radius = -1
    while True:
        volcano_radius += 1
        max_time = (volcano_radius + 1) * 30

        g = graph.copy()
        lava_points, _ = get_points_within_radius(data, volcano_radius)
        for x, y in lava_points:
            for height in range(4):
                g.remove_node((x, y, height))

        # VISUALIZATION:
        # path = networkx.shortest_path(g, start_node, goal_node, weight="weight")
        # path_coords = {(x, y) for x, y, _ in path}
        # for y in range(h):
        #     for x in range(w):
        #         if (x, y) in lava_points + [(mx, my)]:
        #             print(f"{Back.RED}{data[y][x]}{Back.RESET}", end="")
        #         elif (x, y) in path_coords:
        #             print(f"{Fore.GREEN}{data[y][x]}{Fore.RESET}", end="")
        #         else:
        #             print(data[y][x], end="")
        #     print()

        used_time = networkx.shortest_path_length(
            g, start_node, goal_node, weight="weight"
        )
        if used_time <= max_time:
            return used_time * volcano_radius

        # Estimate next radius to try
        too_much_time = used_time - max_time
        estimated_additional_radius = ceil(too_much_time / 30)
        volcano_radius += estimated_additional_radius - 1


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

    print(time.perf_counter() - start)


if __name__ == "__main__":
    main()
