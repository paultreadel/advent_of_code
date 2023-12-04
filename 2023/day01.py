import re
from itertools import chain


def part_one():
    line_digits = [re.findall(r"\d", line) for line in input_data]
    first_last_digits = [int(line[0] + line[-1]) for line in line_digits]
    total = sum(first_last_digits)
    print(f"{total=}")


numbers_by_word = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part_two():

    total = 0
    for line in input_data:
        number_candidates = chain(
            re.finditer(r"\d", line),
            *[re.finditer(key, line) for key in numbers_by_word.keys()],
        )
        sorted_number_candidates = sorted(number_candidates, key=lambda x: x.start())
        first_last_numbers = [
            sorted_number_candidates[0].group(),
            sorted_number_candidates[-1].group(),
        ]
        as_digits = [numbers_by_word.get(x, x) for x in first_last_numbers]
        value = int("".join(as_digits))
        total += value
    print(f"{total=}")


if __name__ == "__main__":
    with open("data/day01_input.txt") as input_file:
        input_data = input_file.readlines()
    part_one()
    part_two()
