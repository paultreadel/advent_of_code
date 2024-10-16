def roll_rock(idx, col):
    if idx == len(col):
        return col

    if col[idx] == "O":
        move_idx = idx - 1
        while (move_idx > -1) and (col[move_idx] == "."):
            move_idx -= 1
        move_idx += 1  # increment back to last free location
        if idx != move_idx:
            # move rock to next free location (if not already at it)
            col[idx], col[move_idx] = col[move_idx], col[idx]
        return roll_rock(idx + 1, col)
    elif col[idx] in ".#":
        return roll_rock(idx + 1, col)

    pass


def part_one(input):
    cols = []
    for col in zip(*input):
        cols.append(roll_rock(0, list(col)))
        pass
    grid = list(zip(*cols))  # pivot back to original shape
    rocks_per_row = [len(list(filter(lambda x: x == "O", row))) for row in grid]
    weight_per_row = [
        rocks * wt for rocks, wt in zip(rocks_per_row, range(len(rocks_per_row), 0, -1))
    ]
    total_weight = sum(weight_per_row)
    print(f"{total_weight=}")


def part_two(input):
    pass


def parse_input(data):
    return [list(l) for l in data.splitlines()]


if __name__ == "__main__":
    input_filepath = "data/day14_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()

    data = parse_input(input_data)
    part_one(data)
    # part_two(data)
