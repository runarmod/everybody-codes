import re
import time

test_inputs = [
    """ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]""",
    """ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
SWAP 1
SWAP 5
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]""",
    """ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
SWAP 1
SWAP 5
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]
SWAP 2""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]
    return open(f"round{part}.txt", "r").read().strip()


class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = int(value) if isinstance(value, str) else value
        self.left = None
        self.right = None

    def add_child(self, node: "Node"):
        if node.value < self.value:
            if self.left is None:
                self.left = node
            else:
                self.left.add_child(node)
        else:
            if self.right is None:
                self.right = node
            else:
                self.right.add_child(node)


def nodes_on_each_level(node: Node, level=0, levels=None):
    if levels is None:
        levels = {}
    if node is None:
        return levels
    if level not in levels:
        levels[level] = []
    levels[level].append(node)
    nodes_on_each_level(node.left, level + 1, levels)
    nodes_on_each_level(node.right, level + 1, levels)
    return levels


def get_nodes_on_densest_level(tree: Node):
    return max(nodes_on_each_level(tree).items(), key=lambda x: len(x[1]))[1]


def get_names(nodes):
    return "".join([node.name for node in nodes])


def run(raw_data, swapfunc):
    data = re.findall(
        r"SWAP (\d+)|ADD id=(\d+) left=\[(\d+),(.+)\] right=\[(\d+),(.+)\]", raw_data
    )
    left_tree: Node | None = None
    right_tree: Node | None = None

    ids = {}

    for line in data:
        swap_id, _id, left_value, left_name, right_value, right_name = line
        if swap_id:
            left, right = ids[swap_id]
            swapfunc(left, right)
        else:
            left = Node(left_name, left_value)
            right = Node(right_name, right_value)
            if left_tree is None:
                left_tree = left
            else:
                left_tree.add_child(left)
            if right_tree is None:
                right_tree = right
            else:
                right_tree.add_child(right)
            ids[_id] = (left, right)

    left_nodes = get_nodes_on_densest_level(left_tree)
    right_nodes = get_nodes_on_densest_level(right_tree)

    return get_names(left_nodes) + get_names(right_nodes)


def part1(test: bool = False):
    return run(get_input(1, test), lambda left, right: None)


def part2(test: bool = False):
    def swapfunc(left, right):
        left.name, left.value, right.name, right.value = (
            right.name,
            right.value,
            left.name,
            left.value,
        )

    return run(get_input(2, test), swapfunc)


def part3(test: bool = False):
    def swapfunc(left, right):
        (
            left.name,
            left.value,
            left.left,
            left.right,
            right.name,
            right.value,
            right.left,
            right.right,
        ) = (
            right.name,
            right.value,
            right.left,
            right.right,
            left.name,
            left.value,
            left.left,
            left.right,
        )

    return run(get_input(3, test), swapfunc)


def main():
    start = time.perf_counter()
    for test in [True, False]:
        print(f"{['', '(TEST) '][test]}Part 1:", part1(test))
        print(f"{['', '(TEST) '][test]}Part 2:", part2(test))
        print(f"{['', '(TEST) '][test]}Part 3:", part3(test))
        print()
    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
