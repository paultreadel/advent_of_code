from collections import Counter
from functools import total_ordering


@total_ordering
class Card:
    def __init__(self, card, joker_wild=False):
        self.card: str = card
        self.joker_wild: bool = joker_wild

    @property
    def rank(self):
        face_to_int = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        if self.joker_wild:
            face_to_int["J"] = 1
        try:
            return int(self.card)
        except ValueError:
            return int(face_to_int[self.card])

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank


@total_ordering
class Node:
    def __init__(self, val, bet, joker_wild=False):
        self.l = None
        self.r = None
        self.v = val
        self.bet = bet
        self.joker_wild = joker_wild

    def __lt__(self, other):
        if isinstance(other, str):
            other = Node(other, None, self.joker_wild)
        if self._hand_strength() < other._hand_strength():
            return True
        elif self._hand_strength() > other._hand_strength():
            return False
        else:
            return not self._break_tie(other)

    def __eq__(self, other):
        # no hand should ever be equal given problem description
        return False

    def __iter__(self):
        l = list(self.l) if self.l else []
        r = list(self.r) if self.r else []
        for x in l + [(self.v, self.bet)] + r:
            yield x

    def _break_tie(self, other):
        pairs = zip(self.v, other.v)
        for self_card, other_card in pairs:
            if self_card == other_card:
                continue
            return Card(self_card, self.joker_wild) > Card(other_card, other.joker_wild)

    def _full_house(self, card_counts, num_wilds):
        if num_wilds == 0:
            return {3, 2}.issubset(card_counts)
        elif num_wilds == 1:
            return self._two_pair(card_counts, 0)
        return False

    @staticmethod
    def _two_pair(card_counts, num_wilds):
        if num_wilds == 0:
            return sum(x == 2 for x in card_counts) == 2
        if num_wilds == 1:
            return {2, 1}.issubset(card_counts)
        return False

    @staticmethod
    def _n_of_a_kind(n, card_counts, num_wilds):
        return any((num_wilds + count) == n for count in card_counts)

    def _hand_strength(self):
        counts_by_card = Counter(self.v)
        if self.joker_wild:
            num_wilds = counts_by_card["J"]
            counts_by_card["J"] = 0  # set joker to zero
        else:
            num_wilds = 0

        card_counts = counts_by_card.values()
        if self._n_of_a_kind(5, card_counts, num_wilds):
            return 7
        elif self._n_of_a_kind(4, card_counts, num_wilds):
            return 6
        elif self._full_house(card_counts, num_wilds):
            return 5
        elif self._n_of_a_kind(3, card_counts, num_wilds):
            return 4
        elif self._two_pair(card_counts, num_wilds):
            return 3
        elif self._n_of_a_kind(2, card_counts, num_wilds):
            return 2
        else:
            return 1


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, val, bet, joker_wild=False):
        if not self.root:
            self.root = Node(val, bet, joker_wild)
        else:
            self._insert((val, bet, joker_wild), self.root)

    def _insert(self, val, node):
        if val[0] < node:
            if node.l:
                self._insert(val, node.l)
            else:
                node.l = Node(*val)
        else:
            if node.r:
                self._insert(val, node.r)
            else:
                node.r = Node(*val)

    def __iter__(self):
        if self.root is None:
            return None
        for x in iter(self.root):
            yield x


def part_one(data):
    hands = BinaryTree()
    for hand, bet in data:
        hands.insert(hand, bet)
    ordered_bets = [bet for _, bet in hands]
    winnings_by_bet = [
        bet * (rank + 1) for bet, rank in zip(ordered_bets, range(len(ordered_bets)))
    ]
    total_winnings = sum(winnings_by_bet)
    print(f"{total_winnings=}")


def part_two(data):
    hands = BinaryTree()
    for hand, bet in data:
        hands.insert(hand, bet, joker_wild=True)
    ordered_bets = [bet for _, bet in hands]
    winnings_by_bet = [
        bet * (rank + 1) for bet, rank in zip(ordered_bets, range(len(ordered_bets)))
    ]
    total_winnings = sum(winnings_by_bet)
    print(f"{total_winnings=}")


def parse_input(data):
    parsed_data = []
    for line in data.splitlines():
        cards, bet = line.split()
        parsed_data.append((cards, int(bet)))
    return parsed_data


if __name__ == "__main__":
    input_filepath = "data/day07_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()
    d = parse_input(input_data)
    part_one(d)
    part_two(d)
