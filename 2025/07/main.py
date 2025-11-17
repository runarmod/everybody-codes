import time

from ecd import get_inputs

EVENT = 2025
QUEST = 7

assert EVENT is not None
assert QUEST is not None

test_inputs = [
    """Oronris,Urakris,Oroneth,Uraketh

r > a,i,o
i > p,w
n > e,r
o > n,m
k > f,r
a > k
U > r
e > t
O > r
t > h""",
    """Xanverax,Khargyth,Nexzeth,Helther,Braerex,Tirgryph,Kharverax

r > v,e,a,g,y
a > e,v,x,r
e > r,x,v,t
h > a,e,v
g > r,y
y > p,t
i > v,r
K > h
v > e
B > r
t > h
N > e
p > h
H > e
l > t
z > e
X > a
n > v
x > z
T > i""",
    """Khara,Xaryt,Noxer,Kharax

r > v,e,a,g,y
a > e,v,x,r,g
e > r,x,v,t
h > a,e,v
g > r,y
y > p,t
i > v,r
K > h
v > e
B > r
t > h
N > e
p > h
H > e
l > t
z > e
X > a
n > v
x > z
T > i""",
]


def get_input(part: int, test: bool = False) -> str:
    if test:
        return test_inputs[part - 1]

    return get_inputs(event=EVENT, quest=QUEST)[str(part)]


def parse_input(part: int, test: bool = False):
    names, rules = get_input(part, test).split("\n\n")

    names = names.split(",")
    rules = rules.strip().split("\n")
    rules = [line.split(" > ") for line in rules]
    rules = {k: v.split(",") for k, v in rules}
    return names, rules


def name_valid(name, rules):
    for a, b in zip(name, name[1:]):
        if b not in rules.get(a, []):
            return False
    return True


def part1(test: bool = False):
    names, rules = parse_input(1, test)

    for name in names:
        if name_valid(name, rules):
            return name


def part2(test: bool = False):
    names, rules = parse_input(2, test)

    s = 0
    for i, name in enumerate(names):
        if name_valid(name, rules):
            s += i + 1
    return s


def part3(test: bool = False):
    names, rules = parse_input(3, test)

    seen = set()

    def iterate_names(name, rules):
        stack = [name]
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            if len(name) > 11:
                continue
            if len(name) >= 7:
                yield name
            for b in rules.get(name[-1], []):
                stack.append(name + b)

    s = 0
    for name in names:
        if not name_valid(name, rules):
            continue
        s += sum(1 for _ in iterate_names(name, rules))

    return s


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

    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
