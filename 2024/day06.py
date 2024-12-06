from tqdm import tqdm

if __name__ == "__main__":
    # parse input
    with open("data/day06.txt") as input_file:
        input_data = input_file.read()

    pass

    #     input_data = """....#.....
    # .........#
    # ..........
    # ..#.......
    # .......#..
    # ..........
    # .#..^.....
    # ........#.
    # #.........
    # ......#..."""

    grid = [list(row) for row in input_data.split("\n")]
    # up, right, down, left, ordered so each increment of 1 in the index will rotate
    # the direction 90 degrees clockwise
    DIRECTIONS = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]
    guard_chars_to_directions = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }

    def find_guard_start_cell_and_direction(grid):
        guard_chars = "^v<>"
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] in guard_chars:
                    start_direction = guard_chars_to_directions[grid[i][j]]
                    grid[i][j] = "."
                    return (i, j), start_direction
        return None

    def is_cell_in_bounds(cell, grid):
        i, j = cell
        return 0 <= i < len(grid) and 0 <= j < len(grid[0])

    def is_cell_traversable(cell, grid):
        i, j = cell
        return grid[i][j] == "."

    def find_guard_path(grid, start, direction):
        current_cell = start

        # function returns an ordered path to allow part 2 to optimize checking for
        # loops on simulated obstacle position by starting the guard at position `n-1`
        # if an obstacle is placed at position `n`
        ordered_path = [(start, direction)]

        # use set to improve performance when checking if a cell/dir has been visited
        # indicating a loop has been found
        _visited_path = {(start, direction)}

        while True:
            i, j = current_cell
            di, dj = direction
            next_cell = (i + di, j + dj)
            if not is_cell_in_bounds(next_cell, grid):
                return ordered_path, False
            if is_cell_traversable(next_cell, grid):
                current_cell = next_cell
                if (current_cell, direction) in _visited_path:
                    return ordered_path, True
                ordered_path.append((current_cell, direction))
                _visited_path.add((current_cell, direction))
            else:
                direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

    start_cell, start_direction = find_guard_start_cell_and_direction(grid)

    # part 1
    guard_path, _ = find_guard_path(grid, start_cell, start_direction)
    unique_cells = set(cell for cell, _ in guard_path)
    print(f"Part 1: {len(unique_cells)}")

    # part 2
    checked_cells = set()
    num_looping_obstructions = 0
    for idx, (cell, dir) in tqdm(enumerate(guard_path), total=len(guard_path)):
        if cell in checked_cells or cell is start_cell or idx == 0:
            continue
        i, j = cell
        grid[i][j] = "#"
        # start at previous cell & direction to speed up loop detection
        prev_cell, prev_dir = guard_path[idx - 1]
        _, is_loop = find_guard_path(grid, prev_cell, dir)
        if is_loop:
            num_looping_obstructions += 1
        checked_cells.add(cell)
        grid[i][j] = "."
    print(f"Part 2: {num_looping_obstructions}")
