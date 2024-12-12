from collections import defaultdict
from pprint import pprint  # noqa: F401

if __name__ == "__main__":
    with open("data/day12.txt") as input_file:
        input_data = input_file.read()

    input_data = """AAAA
BBCD
BBCC
EEEC"""

    grid = [list(row) for row in input_data.split("\n")]

    checked_cells = set()

    regions = defaultdict(dict)

    def find_matching_neighbors(cell, code):
        neighbors = set((cell,))
        if cell in checked_cells:
            return neighbors
        checked_cells.add(cell)
        for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (cell[0] + offset[0], cell[1] + offset[1])
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):
                if (
                    grid[neighbor[0]][neighbor[1]] == code
                    and neighbor not in checked_cells
                ):
                    neighbors.add(neighbor)
                    next_neighbors = find_matching_neighbors(neighbor, code)
                    neighbors.update(next_neighbors)
        return neighbors

    def l1_distance(cell, other_cell):
        return abs(cell[0] - other_cell[0]) + abs(cell[1] - other_cell[1])

    def is_neighbor(cell, other_cell):
        return l1_distance(cell, other_cell) == 1

    def region_adjacency_list(cells):
        adjacencies = defaultdict(set)
        for cell in cells:
            for other_cell in cells:
                if is_neighbor(cell, other_cell):
                    adjacencies[cell].add(other_cell)
        return adjacencies

    def adjacency_list_edges(adjacencies):
        edges = 0
        for cell in adjacencies:
            edges += len(adjacencies[cell])
        return edges

    def perimeter(num_cells, num_edges):
        perimeter = num_cells * 4 - num_edges
        return perimeter

    # area == num_cells

    total_price_part_one = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            cell = (i, j)
            if cell in checked_cells:
                continue
            region_code = grid[i][j]
            cells = find_matching_neighbors(cell, region_code)
            region_adjacencies = region_adjacency_list(cells)
            region_edges = adjacency_list_edges(region_adjacencies)
            region_area = len(cells)
            region_perimeter = perimeter(region_area, region_edges)
            total_price_part_one += region_area * region_perimeter

    print(f"Part 1: {total_price_part_one}")
    # print(f"Part 2: {num_stones}")
