from __future__ import annotations

import os
import re
import time

from ecd import get_inputs, submit

EVENT = 3
QUEST = 3

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """id=1, plug=BLUE HEXAGON, leftSocket=GREEN CIRCLE, rightSocket=BLUE PENTAGON, data=?
id=2, plug=GREEN CIRCLE, leftSocket=BLUE HEXAGON, rightSocket=BLUE CIRCLE, data=?
id=3, plug=BLUE PENTAGON, leftSocket=BLUE CIRCLE, rightSocket=BLUE CIRCLE, data=?
id=4, plug=BLUE CIRCLE, leftSocket=RED HEXAGON, rightSocket=BLUE HEXAGON, data=?
id=5, plug=RED HEXAGON, leftSocket=GREEN CIRCLE, rightSocket=RED HEXAGON, data=?""",
    """id=1, plug=RED TRIANGLE, leftSocket=RED TRIANGLE, rightSocket=RED TRIANGLE, data=?
id=2, plug=GREEN TRIANGLE, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=3, plug=BLUE PENTAGON, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=4, plug=RED TRIANGLE, leftSocket=BLUE PENTAGON, rightSocket=GREEN PENTAGON, data=?
id=5, plug=RED PENTAGON, leftSocket=GREEN CIRCLE, rightSocket=GREEN CIRCLE, data=?""",
    """id=1, plug=RED TRIANGLE, leftSocket=BLUE TRIANGLE, rightSocket=GREEN TRIANGLE, data=?
id=2, plug=GREEN TRIANGLE, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=3, plug=BLUE PENTAGON, leftSocket=BLUE CIRCLE, rightSocket=GREEN CIRCLE, data=?
id=4, plug=RED TRIANGLE, leftSocket=BLUE PENTAGON, rightSocket=GREEN PENTAGON, data=?
id=5, plug=BLUE TRIANGLE, leftSocket=GREEN CIRCLE, rightSocket=RED CIRCLE, data=?
id=6, plug=BLUE TRIANGLE, leftSocket=GREEN CIRCLE, rightSocket=RED CIRCLE, data=?""",
]

NODE_RE = re.compile(
    r"id=(\d+), plug=([A-Z]+ [A-Z]+), leftSocket=([A-Z]+ [A-Z]+), rightSocket=([A-Z]+ [A-Z]+), data=.*"
)


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


class Node:
    def __init__(self, id: int, plug: str, left_socket: str, right_socket: str):
        self.id = id
        self.plug = plug
        self.left_socket = left_socket
        self.right_socket = right_socket
        self.child_left: Node | None = None
        self.child_right: Node | None = None
        self.left_strong = False
        self.right_strong = False

    def __repr__(self):
        return f"Node(id={self.id}, child_left={self.child_left}, child_right={self.child_right})"

    def left_match_strong(self, other: Node) -> bool:
        return self.left_socket == other.plug

    def right_match_strong(self, other: Node) -> bool:
        return self.right_socket == other.plug

    def left_match_weak(self, other: Node) -> bool:
        c1, s1 = self.left_socket.split()
        c2, s2 = other.plug.split()
        return s1 == s2 or c1 == c2

    def right_match_weak(self, other: Node) -> bool:
        c1, s1 = self.right_socket.split()
        c2, s2 = other.plug.split()
        return s1 == s2 or c1 == c2

    def _set_left(self, node: Node) -> Node | None:
        old = self.child_left
        self.child_left = node
        self.left_strong = self.left_match_strong(node)
        return old

    def _set_right(self, node: Node) -> Node | None:
        old = self.child_right
        self.child_right = node
        self.right_strong = self.right_match_strong(node)
        return old

    def place(self, node: Node | None, part: int) -> Node | None:
        if node is None:
            return None

        # Try left
        if part < 3:
            if self.child_left is not None:
                node = self.child_left.place(node, part)
            elif self.left_match_strong(node) or (
                part == 2 and self.left_match_weak(node)
            ):
                self._set_left(node)
                return None
        else:
            if self.child_left is None and (
                self.left_match_weak(node) or self.left_match_strong(node)
            ):
                self._set_left(node)
                return None
            elif (
                self.child_left is not None
                and not self.left_strong
                and self.left_match_strong(node)
            ):
                node = self._set_left(node)
            elif self.child_left is not None:
                node = self.child_left.place(node, part)

        if node is None:
            return None

        # Try right
        if part < 3:
            if self.child_right is not None:
                node = self.child_right.place(node, part)
            elif self.right_match_strong(node) or (
                part == 2 and self.right_match_weak(node)
            ):
                self._set_right(node)
                return None
        else:
            if self.child_right is None and (
                self.right_match_weak(node) or self.right_match_strong(node)
            ):
                self._set_right(node)
                return None
            elif (
                self.child_right is not None
                and not self.right_strong
                and self.right_match_strong(node)
            ):
                node = self._set_right(node)
            elif self.child_right is not None:
                node = self.child_right.place(node, part)

        return node


def parse_nodes(data: str):
    return (
        Node(id=int(m[0]), plug=m[1], left_socket=m[2], right_socket=m[3])
        for m in NODE_RE.findall(data)
    )


def checksum(root: Node) -> int:
    visited: set[int] = set()
    total = 0
    idx = 1
    stack = [root]
    while stack:
        node = stack[-1]
        if node.child_left is not None:
            stack.append(node.child_left)
            node.child_left = None
            continue
        if node.id not in visited:
            visited.add(node.id)
            total += node.id * idx
            idx += 1
        if node.child_right is not None:
            stack.append(node.child_right)
            node.child_right = None
            continue
        stack.pop()
    return total


def solve(part: int, data: str) -> int:
    nodes = parse_nodes(data)
    root = next(nodes)
    for node in nodes:
        n = node
        while n is not None:
            # While the placement replaces a node
            start_id = n.id
            n = root.place(n, part)
            assert n is None or n.id != start_id, f"Unable to connect node {n.id}"
    return checksum(root)


def part1(test: bool = False):
    return solve(1, get_input(1, test))


def part2(test: bool = False):
    return solve(2, get_input(2, test))


def part3(test: bool = False):
    return solve(3, get_input(3, test))


def main():
    start = time.perf_counter()
    print("(TEST) Part 1:", part1(test=True))
    print("(TEST) Part 2:", part2(test=True))
    print("(TEST) Part 3:", part3(test=True))
    print()

    answers = []
    answers.append(part1(test=False))
    print("Part 1:", answers[-1])
    answers.append(part2(test=False))
    print("Part 2:", answers[-1])
    answers.append(part3(test=False))
    print("Part 3:", answers[-1])
    print()

    total_time = time.perf_counter() - start

    for part, ans in enumerate(answers, start=1):
        if ans is None or os.path.exists(f"correct_part_{part}"):
            continue
        user_answer = input(f"Submit {part}: '{ans}'? (y/N) ").strip().lower()
        if user_answer != "y":
            continue
        resp = submit(event=EVENT, quest=QUEST, part=part, answer=ans)
        if resp.status == 200 and resp.json().get("correct"):
            os.close(os.open(f"correct_part_{part}", os.O_CREAT))

    print("Time:", total_time)


if __name__ == "__main__":
    main()
