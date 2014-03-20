import string
from itertools import product

letters = string.uppercase[:25]  # no Z!
indices = range(len(letters))
WIDTH, HEIGHT = 5, 5


def load_data():
    words = []
    with open("words", 'r') as f:
        words = f.read().split()
    adjacencies = get_adjacencies(words)

    lines = []
    with open("board", 'r') as f:
        lines = f.readlines()
    fixed_letters = get_fixed_letters(lines)
    floating_letters = get_floating_letters(fixed_letters)
    return dict(fixed_letters.items() + floating_letters.items()), adjacencies


def get_adjacencies(words):
    """Return adjacency lists from input words
    """
    adj = {letter: [] for letter in letters}
    for word in words:
        for n in range(len(word) - 1):
            first_letter, second_letter = word[n], word[n + 1]
            adj[first_letter].append(second_letter)
            adj[second_letter].append(first_letter)
    return adj


def get_fixed_letters(lines):
    fixed_letters = {}
    for j, line in enumerate(lines):
        for i, letter in enumerate(line.strip().replace(' ', '')):
            if not letter == '_':
                fixed_letters[letter] = set(((i, j),))
    return fixed_letters


def get_floating_letters(fixed_letters):
    fixed_places = reduce(set.union, fixed_letters.values())
    all_places = set(product(range(WIDTH), range(HEIGHT)))
    available_places = all_places - fixed_places
    unsolved = {L: available_places for L in letters if L not in fixed_letters}
    return unsolved


def print_result(positions):
    inv_map = {list(v)[0]: k for k, v in positions.items()}
    for j in range(HEIGHT):
        print [inv_map[(i, j)] for i in range(WIDTH)]


# ----------------------------------------------------------------------------


def fixed(letter_positions):
    return len(letter_positions) == 1


def floating_letters(positions):
    for k, v in positions.iteritems():
        if len(v) > 1:
            yield k


def set_neighbourhood(positions, letter):
    fixed_positions = reduce(set.union,
                            (v for v in positions.itervalues() if fixed(v)))
    nhd_union = reduce(set.union,
                       [neighbourhood(*p) for p in positions[letter]], set())
    return nhd_union - fixed_positions


def neighbourhood(x, y):
    return set(product(range(max(0, x - 1), min(WIDTH, x + 2)),
                       range(max(0, y - 1), min(HEIGHT, y + 2))))


def unsolved(positions):
    return any(len(v) > 1 for v in positions.itervalues())


def main():
    positions, adjacencies = load_data()

    while unsolved(positions):
        for floating_letter in floating_letters(positions):
            for adjacent_letter in adjacencies[floating_letter]:
                nhd = set_neighbourhood(positions, adjacent_letter)
                positions[floating_letter] = nhd & positions[floating_letter]
                if fixed(positions[floating_letter]):
                    break
    print_result(positions)

if __name__ == "__main__":
    main()
