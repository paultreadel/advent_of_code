from functools import lru_cache

# filename = "sample.txt"
filename = "data.txt"


DEBUG = True


def propagate_beam_downward(grid, idx, explored):
    # index uses ij index i=rows, j=columns
    # if beam off bottom or split left/right out of bounds or beam merges with
    # another already explored beam
    if idx[0] >= len(grid) or idx[1] < 0 or idx[1] >= len(grid[0]) or idx in explored:
        return 0
    explored.add(idx)
    if grid[idx[0]][idx[1]] in "S.":
        # empty cell, move down on index and propagate again
        idx_down = (idx[0] + 1, idx[1])
        return propagate_beam_downward(grid, idx_down, explored)
    split_count = 1
    idx_left = (idx[0], idx[1] - 1)
    idx_right = (idx[0], idx[1] + 1)
    if idx_left not in explored:
        split_count += propagate_beam_downward(grid, idx_left, explored)
    if idx_right not in explored:
        split_count += propagate_beam_downward(grid, idx_right, explored)
    return split_count


if __name__ == "__main__":
    # total_part1 = 0
    # total_part2 = 0

    with open(filename, "r") as f:
        lines = f.read()

    grid = [list(line) for line in lines.split("\n")]
    explored = set()

    @lru_cache
    def propagate_beam_downward_quantum_part2(idx):
        # index uses ij index i=rows, j=columns
        # if beam off bottom or split left/right out of bounds or beam merges with
        # another already explored beam
        if idx[0] >= len(grid) or idx[1] < 0 or idx[1] >= len(grid[0]):
            return 0
        explored.add(idx)
        if grid[idx[0]][idx[1]] in "S.":
            # empty cell, move down on index and propagate again
            idx_down = (idx[0] + 1, idx[1])
            return propagate_beam_downward_quantum_part2(idx_down)
        split_count = 1
        idx_left = (idx[0], idx[1] - 1)
        idx_right = (idx[0], idx[1] + 1)
        split_count += propagate_beam_downward_quantum_part2(idx_left)
        split_count += propagate_beam_downward_quantum_part2(idx_right)
        return split_count

    idx_start = (0, grid[0].index("S"))
    total_part1 = propagate_beam_downward(grid, idx_start, explored=set())
    total_part2 = propagate_beam_downward_quantum_part2(idx_start)
    # need to add one to account for the initial beam (from start to first splitter),
    # this also covers the case where beam is never split, resulting in one timeline
    total_part2 += 1

    print(f"Part 1: {total_part1}")
    print(f"Part 1: {total_part2}")
