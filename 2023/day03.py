import operator
import re

import numpy as np
from scipy.signal import convolve2d


def is_symbol(s):
    return re.match(f"[^\d.]", s) is not None


def is_adjacent_to_symbol(row, start_position, end_position, symbol_adjacency):
    return np.any(symbol_adjacency[row, start_position:end_position])


def part_one(data):
    schematic = np.array([list(s.strip()) for s in data])
    symbols = np.vectorize(is_symbol)(schematic)
    kernel = np.ones((3, 3))
    adjacent_to_symbols = convolve2d(symbols, kernel, mode="same").astype("bool")

    number_locations = []
    for row_num, row in enumerate(data):
        numbers = re.finditer(r"\d+", row)
        number_locations.extend(
            [(row_num, number.span(), int(number.group())) for number in numbers]
        )

    numbers_adjacent_to_symbols = filter(
        lambda x: is_adjacent_to_symbol(x[0], *x[1], adjacent_to_symbols),
        number_locations,
    )
    total = sum([n[-1] for n in numbers_adjacent_to_symbols])
    print(f"{total=}")


def part_two(data):
    schematic = np.array([list(s.strip()) for s in data])
    part_number_matches = np.empty_like(schematic, dtype="object")
    for row_num, row in enumerate(data):
        for number in re.finditer(r"\d+", row):
            part_number_matches[row_num, number.start() : number.end()] = number

    adjacent_kernel = np.ones((3, 3))
    total_gear_ratio = 0
    for idx, is_gear_symbol in np.ndenumerate(schematic == "*"):
        if is_gear_symbol:
            gear_location = np.zeros_like(schematic, dtype="bool")
            gear_location[idx] = True
            gear_location = convolve2d(
                gear_location, adjacent_kernel, mode="same"
            ).astype("bool")
            adjacent_part_numbers = set(
                filter(
                    lambda x: isinstance(x, re.Match),
                    set(part_number_matches[gear_location]),
                )
            )
            if len(adjacent_part_numbers) == 2:
                part_numbers = [int(pn.group()) for pn in adjacent_part_numbers]
                total_gear_ratio += operator.mul(*part_numbers)
    print(f"{total_gear_ratio=}")


if __name__ == "__main__":
    with open("data/day03_input.txt") as input_file:
        input_data = input_file.readlines()
    part_one(input_data)
    part_two(input_data)
