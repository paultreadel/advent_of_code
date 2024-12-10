from pprint import pprint  # noqa: F401

if __name__ == "__main__":
    with open("data/day10.txt") as input_file:
        input_data = input_file.read()

    #         input_data = """.....0.
    # ..4321.
    # ..5..2.
    # ..6543.
    # ..7..4.
    # ..8765.
    # ..9...."""

    DIRECTIONS = [
        (0, 1),  # right
        (1, 0),  # down
        (0, -1),  # left
        (-1, 0),  # up
    ]

    grid = [list(row) for row in input_data.split("\n")]
    pprint(grid)

    # for all zeros

    def in_bounds(cell):
        return 0 <= cell[0] < len(grid) and 0 <= cell[1] < len(grid[0])

    def print_scores(scores):
        copy = scores.copy()
        for i in range(len(scores)):
            for j in range(len(scores[0])):
                copy[i][j] = len(copy[i][j])
        pprint(copy)

    def cell_score(elevation, cell, scores, visited):
        if cell in visited:
            return scores[cell[0]][cell[1]]
        if elevation == 9:
            if cell in visited:
                return 0
            visited.add(cell)
            scores[cell[0]][cell[1]] |= {cell}
            return len(scores[cell[0]][cell[1]])
        for direction in DIRECTIONS:
            next_cell = (cell[0] + direction[0], cell[1] + direction[1])
            if not in_bounds(next_cell):
                continue
            try:
                next_elevation = int(grid[next_cell[0]][next_cell[1]])
            except ValueError:
                next_elevation = -1
            if next_elevation == elevation + 1:
                if cell_score(next_elevation, next_cell, scores, visited):
                    scores[cell[0]][cell[1]] |= scores[next_cell[0]][next_cell[1]]
        visited.add(cell)
        return len(scores[cell[0]][cell[1]])

    # array of all zeros same shape as grid
    trailhead_count = 0
    scores = [[set() for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "0":
                trailhead_count += cell_score(0, (i, j), scores, set())
    print(trailhead_count)

    # visited_cells = set()
    # print(cell_score(0, (0, 1), scores, visited_cells))
    # print(cell_score(0, (6, 5), scores, visited_cells))
    # # print(cell_score(0, (0, 3), scores, visited_cells))
    # print_scores(scores)

    pass
