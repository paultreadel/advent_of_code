from pprint import pprint  # noqa: F401

if __name__ == "__main__":
    with open("data/day10.txt") as input_file:
        input_data = input_file.read()

    #         input_data = """89010123
    # 78121874
    # 87430965
    # 96549874
    # 45678903
    # 32019012
    # 01329801
    # 10456732"""

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

    def unique_trails(elevation, cell, scores, visited):
        if elevation == 9:
            scores[cell[0]][cell[1]].add(tuple((cell,)))
            return scores[cell[0]][cell[1]]
        for direction in DIRECTIONS:
            next_cell = (cell[0] + direction[0], cell[1] + direction[1])
            if not in_bounds(next_cell):
                continue
            try:
                next_elevation = int(grid[next_cell[0]][next_cell[1]])
            except ValueError:
                next_elevation = -1
            if next_elevation == elevation + 1:
                if unique_trails(next_elevation, next_cell, scores, visited):
                    paths = []
                    for path in scores[next_cell[0]][next_cell[1]]:
                        paths.append((cell,) + path)
                    scores[cell[0]][cell[1]].update(paths)
        visited.add(cell)
        return scores[cell[0]][cell[1]]

    # array of all zeros same shape as grid
    trailhead_count = 0
    scores = [[set() for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "0":
                trailhead_count += cell_score(0, (i, j), scores, set())
    print(f"Part 1 {trailhead_count}")

    # array of all zeros same shape as grid
    trailhead_count = 0
    scores = [[set() for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "0":
                trails = unique_trails(0, (i, j), scores, set())
                num_trails = len(set(tuple(l) for l in trails))
                trailhead_count += num_trails
    print(f"Part 2 {trailhead_count}")
