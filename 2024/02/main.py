import colorama

colorama.init(autoreset=True)


def main(do_visualize=False):
    s = part1()
    print("Part 1:", s)

    s = part2()
    print("Part 2:", s)

    indexes = part3(do_visualize)
    print("Part 3:", len(indexes))


def part1():
    words, sentence = open("round1.txt").read().strip().split("\n\n")
    words = words[6:].split(",")
    s = 0
    for word in words:
        s += sentence.count(word)
    return s


def part2():
    words, sentences = open("round2.txt").read().strip().split("\n\n")
    words = words[6:].split(",")
    sentences = sentences.split("\n")
    s = 0
    for sentence in sentences:
        indexes = set()
        for word in words:
            for i in range(len(sentence) - len(word) + 1):
                if sentence[i : i + len(word)] == word:
                    for j in range(i, i + len(word)):
                        indexes.add(j)
                if sentence[i : i + len(word)] == word[::-1]:
                    for j in range(i, i + len(word)):
                        indexes.add(j)
        s += len(indexes)
    return s


def part3(do_visualize):
    words, sentences = open("round3.txt").read().strip().split("\n\n")
    words = words[6:].split(",")
    sentences = sentences.split("\n")

    indexes = thing(words, sentences)
    _sentences = ["".join(t) for t in zip(*sentences)]
    indexes_2 = thing(words, _sentences, second=True)
    indexes.update({(y, x) for x, y in indexes_2})

    width, height = len(sentences[0]), len(sentences)
    indexes = {(x % width, y % height) for x, y in indexes}

    def visualize(indexes):
        for y, sentence in enumerate(sentences):
            for x in range(len(sentence)):
                if (x, y) in indexes:
                    print(f"{colorama.Fore.RED}{sentence[x]}", end="")
                else:
                    print(sentence[x], end="")
            print()

    if do_visualize:
        visualize(indexes)
    return indexes


def thing(words, sentences, second=False):
    indexes: set[tuple[int, int]] = set()
    for word in words:
        # Horizontal
        for y, sentence in enumerate(sentences):
            for i in range(len(sentence)):
                if second:
                    _sentence = sentence
                else:
                    _sentence = sentence + sentence
                if _sentence[i : i + len(word)] == word:
                    indexes.update((x, y) for x in range(i, i + len(word)))
                if _sentence[i : i + len(word)] == word[::-1]:
                    indexes.update((x, y) for x in range(i, i + len(word)))
    return indexes


if __name__ == "__main__":
    main(visualize=False)
