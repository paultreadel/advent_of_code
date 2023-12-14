import numpy as np


def vertical_reflection(grid, with_smudge=False):
    h, w = grid.shape
    for i in range(1, w):  # start on first column, need at least two columns to compare
        sz = min(i, w - i)
        l, r = grid[:, i - sz : i], grid[:, i : i + sz]
        r = np.flip(r, axis=1)  # mirror vertically
        if with_smudge:
            if np.sum(~np.equal(l, r)) == 1:
                return i
        else:
            if np.array_equal(l, r):
                return i


def horizontal_reflection(grid, with_smudge=False):
    return vertical_reflection(grid.T, with_smudge)  # transpose so vertical reflection


def part_one(input, with_smudge):
    total = 0
    for grid in input:
        value = vertical_reflection(grid, with_smudge)
        if not value:
            value = horizontal_reflection(grid, with_smudge) * 100
        total += value
    print(f"{total=}")


def parse_input(data):
    grids = [
        np.array([list(l) for l in grid.splitlines()]) for grid in data.split("\n\n")
    ]
    return grids


if __name__ == "__main__":
    input_filepath = "data/day13_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()

    data = parse_input(input_data)
    part_one(data, False)
    part_one(data, True)
