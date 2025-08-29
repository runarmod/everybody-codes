import re
import time
from itertools import count

test_inputs = [
    """1: faces=[1,2,3,4,5,6] seed=7
2: faces=[-1,1,-1,1,-1] seed=13
3: faces=[9,8,7,8,9] seed=17""",
    """1: faces=[1,2,3,4,5,6,7,8,9] seed=13
2: faces=[1,2,3,4,5,6,7,8,9] seed=29
3: faces=[1,2,3,4,5,6,7,8,9] seed=37
4: faces=[1,2,3,4,5,6,7,8,9] seed=43

51257284""",
    """1: faces=[1,2,3,4,5,6,7,8,9] seed=339211
2: faces=[1,2,3,4,5,6,7,8,9] seed=339517
3: faces=[1,2,3,4,5,6,7,8,9] seed=339769
4: faces=[1,2,3,4,5,6,7,8,9] seed=339049
5: faces=[1,2,3,4,5,6,7,8,9] seed=338959
6: faces=[1,2,3,4,5,6,7,8,9] seed=340111
7: faces=[1,2,3,4,5,6,7,8,9] seed=339679
8: faces=[1,2,3,4,5,6,7,8,9] seed=339121
9: faces=[1,2,3,4,5,6,7,8,9] seed=338851

94129478611916584144567479397512595367821487689499329543245932151
45326719759656232865938673559697851227323497148536117267854241288
44425936468288462848395149959678842215853561564389485413422813386
64558359733811767982282485122488769592428259771817485135798694145
17145764554656647599363636643624443394141749674594439266267914738
89687344812176758317288229174788352467288242171125512646356965953
72436836424726621961424876248346712363842529736689287535527512173
18295771348356417112646514812963612341591986162693455745689374361
56445661964557624561727322332461348422854112571195242864151143533
77537797151985578367895335725777225518396231453691496787716283477
37666899356978497489345173784484282858559847597424967325966961183
26423131974661694562195955939964966722352323745667498767153191712
99821139398463125478734415536932821142852955688669975837535594682
17768265895455681847771319336534851247125295119363323122744953158
25655579913247189643736314385964221584784477663153155222414634387
62881693835262899543396571369125158422922821541597516885389448546
71751114798332662666694134456689735288947441583123159231519473489
94932859392146885633942828174712588132581248183339538341386944937
53828883514868969493559487848248847169557825166338328352792866332
54329673374115668178556175692459528276819221245996289611868492731
97799599164121988455613343238811122469229423272696867686953891233
56249752581283778997317243845187615584225693829653495119532543712
39171354221177772498317826968247939792845866251456175433557619425
56425749216121421458547849142439211299266255482219915528173596421
48679971256541851497913572722857258171788611888347747362797259539
32676924489943265499379145361515824954991343541956993467914114579
45733396847369746189956225365375253819969643711633873473662833395
42291594527499443926636288241672629499242134451937866578992236427
47615394883193571183931424851238451485822477158595936634849167455
16742896921499963113544858716552428241241973653655714294517865841
57496921774277833341488566199458567884285639693339942468585269698
22734249697451127789698862596688824444191118289959746248348491792
28575193613471799766369217455617858422158428235521423695479745656
74234343226976999161289522983885254212712515669681365845434541257
43457237419516813368452247532764649744546181229533942414983335895""",
]


class Die:
    def __init__(self, _id, faces, seed):
        self.id = _id
        self.faces = faces
        self.seed = seed
        self.pulse = seed
        self.rolls = 0
        self.face = 0
        self.position = 0

    def roll(self):
        self.rolls += 1
        spin = self.rolls * self.pulse

        self.face = (self.face + spin) % len(self.faces)

        self.pulse += spin
        self.pulse %= self.seed
        self.pulse += 1 + self.rolls + self.seed

        return self.faces[self.face]


def get_input(part: int, test: bool = False):
    data = open(f"round{part}.txt", "r").read() if not test else test_inputs[part - 1]
    data = data.strip().split("\n\n")

    dies: list[Die] = []
    for line in data[0].split("\n"):
        die_nr, *faces, seed = list(map(int, re.findall(r"-?\d+", line)))
        dies.append(Die(die_nr, faces, seed))

    if part == 1:
        return dies
    if part == 2:
        return dies, data[1]
    if part == 3:
        return dies, data[1].split("\n")

    assert False, "Invalid part"


def part1(test: bool = False):
    dies: list[Die] = get_input(1, test)

    s = 0
    for roll_nr in count(start=1):
        for die in dies:
            s += die.roll()
        if s >= 10000:
            return roll_nr


def part2(test: bool = False):
    data: tuple[list[Die], str] = get_input(2, test)
    dies, track = data

    placements = []
    while len(placements) != len(dies):
        for die in dies:
            if die.id in placements:
                continue

            roll = die.roll()
            if track[die.position] != str(roll):
                continue

            die.position += 1
            if die.position >= len(track):
                placements.append(die.id)
    return ",".join(map(str, placements))


def part3(test: bool = False):
    data: tuple[list[Die], list[str]] = get_input(3, test)
    dies, grid = data

    all_pos = set()
    for die in dies:
        num = die.roll()
        check = {
            (x, y)
            for x in range(len(grid[0]))
            for y in range(len(grid))
            if grid[y][x] == str(num)
        }
        all_pos |= check
        while len(check):
            num = die.roll()
            next_check = set()
            for x, y in check:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
                    if not (0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid)):
                        continue
                    if grid[y + dy][x + dx] == str(num):
                        next_check.add((x + dx, y + dy))
            all_pos |= next_check
            check = next_check

    draw(all_pos, grid)

    return len(all_pos)


def draw(all_pos: set[tuple[int, int]], grid):
    from PIL import Image

    img = Image.new("RGB", (len(grid[0]), len(grid)), "black")
    pixels = img.load()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in all_pos:
                pixels[x, y] = (0, 0, 0)
            else:
                pixels[x, y] = (255, 255, 255)
    img.save("output.png")


def main():
    start = time.perf_counter()
    test = True
    print("(TEST) Part 1:", part1(test))
    print("(TEST) Part 2:", part2(test))
    print("(TEST) Part 3:", part3(test))
    print()

    test = False
    print("Part 1:", part1(test))
    print("Part 2:", part2(test))
    print("Part 3:", part3(test))
    print()

    print("Time:", time.perf_counter() - start)


if __name__ == "__main__":
    main()
