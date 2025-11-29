import re
import time

import networkx
from ecd import get_inputs

EVENT = 2025
QUEST = 18

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 17:
- branch to Plant 1 with thickness 15
- branch to Plant 2 with thickness 3

Plant 5 with thickness 24:
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13

Plant 6 with thickness 15:
- branch to Plant 3 with thickness 14

Plant 7 with thickness 10:
- branch to Plant 4 with thickness 15
- branch to Plant 5 with thickness 21
- branch to Plant 6 with thickness 34""",
    """Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 10:
- branch to Plant 1 with thickness -25
- branch to Plant 2 with thickness 17
- branch to Plant 3 with thickness 12

Plant 5 with thickness 14:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -26
- branch to Plant 3 with thickness 15

Plant 6 with thickness 150:
- branch to Plant 4 with thickness 5
- branch to Plant 5 with thickness 6


1 0 1
0 0 1
0 1 1""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def part1(test: bool = False):
    data = get_input(1, test).split("\n\n")

    G = build_graph(data)
    return final_value_test_case(G, {n for n, d in G.in_degree() if d == 0})


def part2(test: bool = False):
    data, test_cases = get_input(2, test).split("\n\n\n")
    data = data.split("\n\n")

    G = build_graph(data)

    return sum(
        final_value_test_case(G, free_branch_plants)
        for free_branch_plants in free_branches_from_test_case(test_cases)
    )


def part3(test: bool = False):
    data, test_cases = get_input(3, test).split("\n\n\n")
    data = data.split("\n\n")

    G = build_graph(data)

    best = []

    # Get best beginner nodes to activate
    beginner_nodes = [n for n, d in G.in_degree() if d == 0]
    for bn in beginner_nodes:
        out_thickness = [
            _data["thickness"] for _in, _out, _data in G.out_edges(bn, data=True)
        ]
        all_neg = int(all(t < 0 for t in out_thickness))
        all_pos = int(all(t > 0 for t in out_thickness))
        assert all_neg or all_pos
        best.append(all_pos)

    best_score = final_value_test_case(G, set(i + 1 for i, v in enumerate(best) if v))

    s = 0
    for free_branch_plants in free_branches_from_test_case(test_cases):
        local_score = final_value_test_case(G, free_branch_plants)
        if local_score != 0:
            s += best_score - local_score
    return s


def build_graph(data: list[str]) -> networkx.DiGraph:
    G = networkx.DiGraph()

    for plant_section in data:
        nums = list(map(int, re.findall(r"-?\d+", plant_section)))
        plant_id, thickness, *rest = nums
        G.add_node(plant_id, thickness=thickness)
        if len(rest) % 2 == 1:
            continue

        for i in range(0, len(rest), 2):
            neighbor_id = rest[i]
            branch_thickness = rest[i + 1]
            G.add_edge(
                neighbor_id,
                plant_id,
                thickness=branch_thickness,
            )

    return G


def free_branches_from_test_case(test_cases: str):
    for test_case in test_cases.split("\n"):
        test_case = list(map(int, test_case.split(" ")))
        free_branch_plants = set()
        for i in range(len(test_case)):
            if test_case[i] == 1:
                free_branch_plants.add(i + 1)
        yield free_branch_plants


def final_value_test_case(G: networkx.DiGraph, free_branch_plants: set[int]) -> int:
    sorted_plants = list(networkx.topological_sort(G))

    incomming_energy = {plant: 0 for plant in G.nodes()}
    for plant in free_branch_plants:
        incomming_energy[plant] = 1
    thickness = {plant: G.nodes[plant]["thickness"] for plant in G.nodes()}
    plant_energy = {plant: 0 for plant in G.nodes()}

    for plant in sorted_plants:
        total_energy = incomming_energy[plant]
        if total_energy >= thickness[plant]:
            plant_energy[plant] = total_energy

        for neighbor in G.successors(plant):
            branch_thickness = G.edges[plant, neighbor]["thickness"]
            incomming_energy[neighbor] += branch_thickness * plant_energy[plant]

    last_plant = max(plant_energy.keys())
    return plant_energy[last_plant]


def main():
    start = time.perf_counter()
    print("(TEST) Part 1:", part1(test=True))
    print("(TEST) Part 2:", part2(test=True))
    print()

    print("Part 1:", part1(test=False))
    print("Part 2:", part2(test=False))
    print("Part 3:", part3(test=False))
    print()

    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
