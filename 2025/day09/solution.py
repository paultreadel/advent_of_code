import itertools

import shapely

# filename = "sample.txt"
filename = "data.txt"


DEBUG = True


def rectangle_area(corner1, corner2):
    x1, y1 = corner1
    x2, y2 = corner2
    # increase by one, rectangles of a single row should still have area, likewise
    # when two corners are identical area should be 1 not zero
    xdiff = abs(x1 - x2) + 1
    ydiff = abs(y1 - y2) + 1
    return xdiff * ydiff


if __name__ == "__main__":
    total_part1 = 0
    total_part2 = 0

    with open(filename, "r") as f:
        lines = f.read()

    corners = [
        [int(value) for value in line.split(",")] for line in lines.split("\n") if line
    ]

    areas = [rectangle_area(c1, c2) for c1, c2 in itertools.combinations(corners, 2)]
    max_area = max(areas)
    total_part1 = max_area

    # create a list of points with first point repeated at end to create a full loop
    points_ring = corners.copy()
    points_ring.append(corners[0])
    red_green_tiles = shapely.geometry.Polygon(corners)
    areas_part2 = []
    for c1, c2 in itertools.combinations(corners, 2):
        x1, y1 = c1
        x2, y2 = c2
        square_geom = shapely.geometry.box(
            min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        )
        if not red_green_tiles.contains(square_geom):
            continue
        areas_part2.append(rectangle_area(c1, c2))
    total_part2 = max(areas_part2)

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")
