from collections import defaultdict
from itertools import combinations

if __name__ == "__main__":
    with open("data/day08.txt") as input_file:
        input_data = input_file.read()

    grid = [list(row) for row in input_data.split("\n")]

    def get_offset(a, b):
        return a[0] - b[0], a[1] - b[1]

    def apply_offset(cell, offset):
        return cell[0] + offset[0], cell[1] + offset[1]

    def in_bounds(cell):
        return 0 <= cell[0] < len(grid) and 0 <= cell[1] < len(grid[0])

    def find_nodes(cell, offset, harmonic: float = 1) -> set:
        # harmonic = 0 -> node on antennas
        # harmonic = 1 -> node on antennas and one offset step away
        # ...
        # harmonic = "inf" -> node on antennas and every multiple step away on grid
        original_cell = cell
        nodes = set()
        for offset in [offset, (-offset[0], -offset[1])]:
            cell = original_cell
            harmonic_count = 0
            while in_bounds(cell) and harmonic_count <= harmonic:
                nodes.add(cell)
                cell = apply_offset(cell, offset)
                harmonic_count += 1
        return nodes

    antenna_positions = defaultdict(set)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ".":
                continue
            antenna_positions[grid[i][j]].add((i, j))

    unique_antinodes_part_one = set()
    unique_antinodes_part_two = set()
    for antenna_type in antenna_positions:
        for antenna_pair in combinations(antenna_positions[antenna_type], 2):
            a1, a2 = antenna_pair
            offset_step = get_offset(a1, a2)

            # part 1 - find nodes on antennas and one offset step away
            nodes = find_nodes(a1, offset_step, harmonic=1) | find_nodes(
                a2, offset_step, harmonic=1
            )
            # remove antenna locations from nodes
            unique_antinodes_part_one.update(nodes.difference(antenna_pair))

            # part 2 - find nodes on antennas and every multiple step away on grid
            unique_antinodes_part_two.update(
                find_nodes(a1, offset_step, harmonic=float("inf"))
            )

    print(f"Part 1: {len(unique_antinodes_part_one)}")
    print(f"Part 2: {len(unique_antinodes_part_two)}")
