import re
from itertools import groupby


def part_one(data):
    total_points = 0
    for game in data:
        winning_numbers, card_numbers = game
        num_winning_numbers = len(set(winning_numbers).intersection(card_numbers))
        if num_winning_numbers:
            game_points = 2 ** (num_winning_numbers - 1)
            total_points += game_points
    print(f"{total_points=}")


def part_two(data):
    num_cards = [1] * len(data)
    for idx, game in enumerate(data):
        winning_numbers, card_numbers = game
        num_winning_numbers = len(set(winning_numbers).intersection(card_numbers))
        slice_wins = slice(idx + 1, idx + 1 + num_winning_numbers)
        num_cards[slice_wins] = [v + num_cards[idx] for v in num_cards[slice_wins]]
    total_cards = sum(num_cards)
    print(f"{total_cards=}")


def parse_input(data):
    numbers_by_game = []
    for game_data in data:
        numbers = [n for n in re.findall(r"(\b\d+\b(?!:)|\|)", game_data)]
        number_lists = [
            list(group) for k, group in groupby(numbers, lambda x: x == "|") if not k
        ]
        number_lists = [[int(x) for x in _list] for _list in number_lists]
        numbers_by_game.append(number_lists)
    return numbers_by_game


if __name__ == "__main__":
    # input_filepath = "data/input_sample.txt"
    input_filepath = "data/day04_input.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.readlines()
    parsed_input = parse_input(input_data)
    part_one(parsed_input)
    part_two(parsed_input)
