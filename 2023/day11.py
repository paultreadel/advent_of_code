from itertools import combinations

import numpy as np


def is_empty(arr):
    return not np.any(arr)


def expand_universe(input):
    is_galaxy = (input == "#").astype("int")

    empty_cols = np.apply_along_axis(is_empty, axis=0, arr=is_galaxy)
    empty_rows = np.apply_along_axis(is_empty, axis=1, arr=is_galaxy)

    is_galaxy = np.insert(is_galaxy, np.flatnonzero(empty_cols), 0, axis=1)
    is_galaxy = np.insert(is_galaxy, np.flatnonzero(empty_rows), 0, axis=0)
    return is_galaxy


def distance(point1, point2):
    """Calculate manhatten distance between points"""
    return np.abs(np.subtract(point1, point2)).sum()


def part_one(input):
    universe = expand_universe(input)

    # find galaxies dict(id: loc)  loc: (x, y)
    galaxy_indices = zip(*np.where(universe))
    galaxies = dict(enumerate(galaxy_indices))

    # measure manhatten distance between each combination of galaxies
    dists = []
    for n0, n1 in combinations(galaxies.keys(), 2):
        g0, g1 = galaxies[n0], galaxies[n1]
        dists.append(distance(g0, g1))
    total_dist = sum(dists)
    print(f"{total_dist=}")


def distance_w_expansion(point1, point2, empty_rows, empty_cols, factor=2):
    coord_ranges = [sorted(coords) for coords in zip(point1, point2)]
    x_rows, y_rows = [range(*coord_range) for coord_range in coord_ranges]

    x_empty = set(x_rows).intersection(empty_rows)
    x_galaxies = set(x_rows).difference(empty_rows)

    y_empty = set(y_rows).intersection(empty_cols)
    y_galaxies = set(y_rows).difference(empty_cols)

    dist = len(x_galaxies) + len(y_galaxies) + (len(x_empty) + len(y_empty)) * factor

    return dist


def part_two(input):
    universe = (input == "#").astype("int")
    empty_cols = np.flatnonzero(np.apply_along_axis(is_empty, axis=0, arr=universe))
    empty_rows = np.flatnonzero(np.apply_along_axis(is_empty, axis=1, arr=universe))

    # find galaxies dict(id: loc)  loc: (x, y)
    galaxy_indices = zip(*np.where(universe))
    galaxies = dict(enumerate(galaxy_indices))

    # measure manhatten distance between each combination of galaxies
    dists = []
    for n0, n1 in combinations(galaxies.keys(), 2):
        g0, g1 = galaxies[n0], galaxies[n1]
        dists.append(
            distance_w_expansion(g0, g1, empty_rows, empty_cols, factor=1_000_000)
        )
    total_dist = sum(dists)
    print(f"{total_dist=}")


def parse_input(data):
    parsed = [list(line) for line in data.splitlines()]
    return np.array(parsed)


if __name__ == "__main__":
    input_filepath = "data/day11_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()

    data = parse_input(input_data)
    part_one(data)
    part_two(data)
