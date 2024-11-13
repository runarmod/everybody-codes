import itertools
import math
from itertools import cycle, permutations

loop2 = """
S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--
-                                                                     -
=                                                                     =
+                                                                     +
=                                                                     +
+                                                                     =
=                                                                     =
-                                                                     -
--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-""".strip()

loop3 = """
S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--
- + +   + =   =     =      =   == = - -     - =  =         =-=        -
= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++
+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=       
= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =          
+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==
=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =
-               = = = =   +  +  ==+ = = +   =        ++    =          -
-               = + + =   +  -  = + = = +   =        +     =          -
--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-""".strip()


def next_coord_in_loop(grid, x, y, prev_x, prev_y):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            if grid[new_y][new_x] != " " and (new_x, new_y) != (prev_x, prev_y):
                return new_x, new_y

    assert False


def from_loop(loop: str):
    loop: list[str] = loop.split("\n")
    x, y = 1, 0
    prev_x, prev_y = 0, 0
    result = loop[y][x]
    while loop[y][x] != "S":
        new_coord = next_coord_in_loop(loop, x, y, prev_x, prev_y)
        prev_x, prev_y = x, y
        x, y = new_coord
        result += loop[y][x]
    return result


def calculate_scores(loop_string, loops_repeats, tracks):
    results = {}
    for chariot, track in tracks.items():
        v = 10
        total = 0
        for knight, track_action in zip(
            itertools.chain.from_iterable(itertools.repeat(loop_string, loops_repeats)),
            cycle(track),
        ):
            if knight == "S" or knight == "=":
                if track_action == "+":
                    v += 1
                elif track_action == "-":
                    v -= 1
            elif knight == "+":
                v += 1
            elif knight == "-":
                v -= 1
            total += v
        results[chariot] = total
    return results


def task1(txt: str):
    tracks = {line[0]: line[2:].split(",") for line in txt.split("\n")}
    results = calculate_scores("=" * 10, 1, tracks)
    return "".join(sorted(results, key=lambda x: results[x], reverse=True))


def task2(txt: str):
    tracks = {line[0]: line[2:].split(",") for line in txt.split("\n")}
    loop_string = from_loop(loop2)
    results = calculate_scores(loop_string, 10, tracks)
    return "".join(sorted(results, key=lambda x: results[x], reverse=True))


def task3(txt: str):
    track = txt[2:].split(",")
    loop_string = from_loop(loop3)

    plan = "+" * 5 + "-" * 3 + "=" * 3
    perms = set(permutations(plan, len(plan)))

    # We can reduce the number of loops we need to do, since after a certain point,
    # every "state" has already been visited
    lcm = math.lcm(len(plan), len(loop_string))
    loop_cycle_count = lcm // len(loop_string)

    # Make sure we actually are simulating as if we are doing 2024 loops
    loop_cycle_count += 2024 % loop_cycle_count

    wins = 0
    for perm in perms:
        peeps = {"rival": track, "me": perm}
        results = calculate_scores(loop_string, loop_cycle_count, peeps)
        wins += results["me"] > results["rival"]
    return wins


def task(txt: str, task_nr: int):
    return [task1, task2, task3][task_nr - 1](txt)


def main():
    for task_nr in range(1, 4):
        task_input = open(f"round{task_nr}.txt", "r").read().strip()
        print(f"Part {task_nr}:", task(task_input, task_nr))


if __name__ == "__main__":
    main()
