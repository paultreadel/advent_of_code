from copy import deepcopy
from typing import Dict, Tuple, List

import numpy as np

valid_directions = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(0, -1), (-1, 0)],
    "7": [(0, -1), (1, 0)],
    "F": [(0, 1), (1, 0)],
    ".": [],
    "S": [(-1, 0), (1, 0), (0, -1), (0, 1)],
}


class Index:
    def __init__(self, idx):
        self.r, self.c = idx
        self.idx = idx

    def __add__(self, other):
        return self.r + other[0], self.c + other[1]

    def __sub__(self, other):
        return self.r - other[0], self.c - other[1]

    def __repr__(self):
        return f"({self.r}, {self.c})"


class Pipe:
    def __init__(self, idx, type):
        self.idx = Index(idx)
        self.type = type

    def __repr__(self):
        return f"{self.idx}: {self.type}"

    @property
    def connections(self):
        return [self.idx + _dir for _dir in valid_directions[self.type]]

    def connected(self, other):
        return self.idx.idx in other.connections and other.idx.idx in self.connections

    def valid_connections(self, layout):
        return [
            connection
            for connection in self.connections
            if self.connected(Pipe(connection, layout[connection]))
        ]


def valid_start_directions(start, layout):
    start_pipe = Pipe(start, layout[start])
    return start_pipe.valid_connections(layout)


def find_start(input):
    loc = np.where(input == "S")
    loc = tuple(int(x[0]) for x in loc)
    return loc


def part_one(input):
    prev_loc = find_start(input)
    start_dirs = valid_start_directions(prev_loc, input)
    next_loc = start_dirs
    pipe_chain = [prev_loc]
    while next_loc:
        next_loc = next_loc.pop()
        pipe_chain.append(next_loc)
        next_loc = set(
            Pipe(next_loc, input[next_loc]).valid_connections(input)
        ).difference(pipe_chain)
    chain_length = len(pipe_chain)
    length_far = chain_length // 2
    print(f"{length_far=}")
    return pipe_chain


def is_sum_odd(arr):
    return sum(arr) % 2


def replace_s_pipe(input):
    loc = find_start(input)
    s_pipe = Pipe(loc, input[loc])
    start_directions = [Index(conn) - loc for conn in (s_pipe.valid_connections(input))]
    for pipe, _dirs in valid_directions.items():
        pipe_matches_dirs = all(s_dir in _dirs for s_dir in start_directions)
        if pipe_matches_dirs:
            input[loc] = pipe
            return input
    assert "Valid start pipe not found"


def part_two(input):
    pipe_chain = part_one(input)
    input = replace_s_pipe(input)

    main_loop_only = np.full_like(input, ".")
    idx_chain = tuple(np.array(pipe_chain).T)
    main_loop_only[idx_chain] = input[idx_chain]

    is_main_loop = main_loop_only != "."

    vertical_pipes = list("|LJ")
    is_vertical = np.isin(main_loop_only, vertical_pipes)

    # ray cast at each tile not in main loop, find vertical crossing number, odd is
    # enclosed, elbows require caution, cannot consider both sets of  `LJ` and `F7` as
    # vertical pipes, must choose one or the other
    is_enclosed = np.zeros_like(is_main_loop, dtype="uint8")
    for idx, v in np.ndenumerate(is_main_loop):
        if v:
            continue
        row, col = idx
        is_enclosed[idx] = is_sum_odd(is_vertical[row, col:])
    num_enclosed = np.sum(is_enclosed)
    print(f"{num_enclosed=}")


def parse_input(data):
    parsed = [list(line) for line in data.splitlines()]
    return np.array(parsed)


if __name__ == "__main__":
    input_filepath = "data/day10_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()

    data = parse_input(input_data)
    # part_one(data)
    part_two(data)
