from enum import Enum

filename = "sample.txt"
filename = "data.txt"

DEBUG = True


class Direction8Way(Enum):
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SW = (1, -1)
    W = (0, -1)
    NW = (-1, -1)


def is_neighbor_occupied(grid, i, j, direction: Direction8Way):
    offset = direction.value
    i_n = i + offset[0]
    j_n = j + offset[1]
    if 0 <= i_n < len(grid) and 0 <= j_n < len(grid[0]):
        return grid[i_n][j_n]
    # out-of-grid - consider unoccupied
    return False


def rolls_in_grid(grid):
    return sum(sum(row) for row in grid)


if __name__ == "__main__":
    with open(filename, "r") as f:
        lines = f.read()
    total_part1 = 0
    total_part2 = 0
    occupancy_grid = []
    for row in lines.split("\n"):
        occupancy_grid.append([value == "@" for value in row])

    num_rows = len(occupancy_grid)
    num_cols = len(occupancy_grid[0])

    prev_rolls_in_grid = 0
    iteration_count = 0
    # must run at least two iterations because rolls are not removed on the first
    # iteration to ensure part 1 total is calculated correctly, first iteration
    # solves part 1 then second iteration is the start of part2 and all subsequent
    # iterations
    while (prev_rolls_in_grid != rolls_in_grid(occupancy_grid)) or iteration_count < 2:
        iteration_count += 1
        prev_rolls_in_grid = rolls_in_grid(occupancy_grid)
        for row_idx in range(num_rows):
            for col_idx in range(num_cols):
                if not occupancy_grid[row_idx][col_idx]:
                    continue
                neighbor_count = 0
                for direction in Direction8Way:
                    neighbor_count += int(
                        is_neighbor_occupied(
                            occupancy_grid, row_idx, col_idx, direction
                        )
                    )
                if neighbor_count < 4:
                    # can't remove rolls on first iteration or the part 1 total is
                    # miscounted
                    if iteration_count == 1:
                        total_part1 += 1
                    else:
                        total_part2 += 1
                        occupancy_grid[row_idx][col_idx] = False

    print(f"Part 1: {total_part1}")
    print(f"Part 1: {total_part2}")
