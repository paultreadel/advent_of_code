from collections import deque
from pprint import pprint  # noqa: F401
from typing import List

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

    def in_bounds(cell):
        return 0 <= cell[0] < len(grid) and 0 <= cell[1] < len(grid[0])

    def find_unique_trails(elevation, cell):
        if elevation == 9:
            return [deque((cell,))]
        new_trails: List[deque] = []
        for direction in DIRECTIONS:
            next_cell = (cell[0] + direction[0], cell[1] + direction[1])
            if not in_bounds(next_cell):
                continue
            next_elevation = int(grid[next_cell[0]][next_cell[1]])
            if next_elevation == elevation + 1:
                for trail in find_unique_trails(next_elevation, next_cell):
                    trail.appendleft((cell,))
                    new_trails.append(trail)
        return new_trails

    total_trail_score = 0
    total_trail_rating = 0
    scores = [[set() for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "0":
                unique_trails = find_unique_trails(0, (i, j))
                trail_end_cells = set(trail[-1] for trail in unique_trails)
                total_trail_score += len(trail_end_cells)
                total_trail_rating += len(unique_trails)
    print(f"Part 1: {total_trail_score}")
    print(f"Part 2: {total_trail_rating}")
