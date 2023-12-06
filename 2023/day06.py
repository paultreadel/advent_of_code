from math import ceil, floor

import numpy as np


def part_one(times, distances):
    margins = 1
    for t, d in zip(times, distances):
        # solve: -x^2 + t*x - d = 0
        # any value of x that falls between the roots will beat the record
        coef = [-1, t, -(d + 0.001)]  # add small offset to d to force tie breaking
        _min, _max = np.sort(np.roots(coef))

        # button allowed to be pressed in integer increments only
        margin = floor(_max) - ceil(_min) + 1
        margins *= margin

    print(f"{margins=}")


def part_two(times, distances):
    times = int("".join(map(str, times)))
    distances = int("".join(map(str, distances)))
    part_one([times], [distances])


def parse_input(data):
    times, distances = [
        [int(x) for x in line.split()[1:]] for line in data.splitlines()
    ]
    return times, distances


if __name__ == "__main__":
    input_filepath = "data/day06_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()
    t, d = parse_input(input_data)
    part_one(t, d)
    part_two(t, d)
