from enum import Enum
from typing import Sequence

import numpy as np

# filename = "sample.txt"
filename = "data.txt"


DEBUG = True


class LineType(Enum):
    GRID = "grid"
    TILE = "tile"


def line_type(line):
    """
    Check if a line is a grid or tile data.

    "Uses presence of `x` to determine if line is grid data.
    """
    if "x" in line:
        return LineType.GRID
    return LineType.TILE


def parse_tile(lines) -> np.ndarray:
    """
    Example Input:
        0:
        ###
        ##.
        .##

    """
    # discard first line, it contains ID
    lines.pop(0)

    # consume lines until an empty row is found
    tile = []
    while lines[0]:
        tile.append(list(lines.pop(0)))

    # remove empty line from lines
    lines.pop(0)

    # convert tile to bool array to indicate grid cells it covers
    return np.array(tile) == "#"


def test_grid(grid_size, tile_counts, tiles: Sequence[np.ndarray]):
    """
    Fail fast if grid does not contain enough area to fit total area of required tiles.

    Pass immediately if grid contains enough area to naively add tiles without any
    specialized packing. Each tile is placed naively in cell
    """
    col, row = grid_size
    tile_areas = [int(np.sum(tile)) for tile in tiles]

    total_tile_area = sum(
        tile_area * tile_counts[idx] for idx, tile_area in enumerate(tile_areas)
    )
    grid_area = col * row
    if total_tile_area > grid_area:
        return False

    # if all tiles have identical grid cell shapes then test each rotation of the tile
    # to check if the required tiles will fit in the grid without any specialized
    # packing
    tile_shapes_equal = len(set(tile.shape for tile in tiles)) == 1
    if tile_shapes_equal:
        tile = tiles[0]
        tile_rot = np.rot90(tile)
        for tile_row, tile_col in [tile.shape, tile_rot.shape]:
            tiles_per_col = col // tile_row
            tiles_per_row = row // tile_row
            grid_size_in_tiles = tiles_per_col * tiles_per_row
            required_tile_count = sum(tile_counts)
            if grid_size_in_tiles >= required_tile_count:
                return True
    raise ValueError("Need to test fancy tile packings.")


if __name__ == "__main__":
    total_part1 = 0
    total_part2 = 0

    if filename == "sample.txt":
        raise NotImplementedError(
            "Solution does not work for example input. Example input requires testing "
            "of packed tiles while full puzzle input only requires naive tests to "
            "find answer."
        )

    with open(filename, "r") as f:
        lines = f.read()

    lines = lines.split("\n")

    # parse tiles out of lines input until grid configuration data found,
    # tile information assumed to always occur at start of input, followed by grid info
    tiles = []
    while lines:
        if line_type(lines[0]) == LineType.TILE:
            tile = parse_tile(lines)
            tiles.append(tile)
            continue
        break

    # parse each grid configuration from remaining lines input, grid configuration
    # consists of grid size COLUMNSxROWS and counts of each tile that must be included
    for line in lines:
        grid_size, tile_counts = line.split(":")
        grid_size = list(map(int, grid_size.split("x")))
        tile_counts = list(map(int, tile_counts.split()))
        if test_grid(grid_size, tile_counts, tiles):
            total_part1 += 1

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")
