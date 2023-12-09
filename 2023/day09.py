import math
from itertools import cycle
from typing import Dict, List, Callable

import numpy as np


def part_one(data_streams):
    next_vals = []
    for data_stream in data_streams:
        diff = data_stream
        last_vals = [diff[-1]]
        while not np.all(diff == 0):
            diff = np.diff(diff)
            last_vals.append(diff[-1])
        next_vals.append(sum(last_vals))
    total = sum(next_vals)
    print(f"{total=}")


def part_two(data_streams):
    data_streams = [list(reversed(x)) for x in data_streams]
    part_one(data_streams)


def parse_input(data):
    data_streams = [[int(x) for x in line.split()] for line in data.splitlines()]
    return data_streams


if __name__ == "__main__":
    input_filepath = "data/day09_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()

    data = parse_input(input_data)
    part_one(data)
    part_two(data)
