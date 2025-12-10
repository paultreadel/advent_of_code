import itertools
from typing import List, Sequence

from tqdm import tqdm

# filename = "sample.txt"
filename = "data.txt"


DEBUG = True


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Line:
    def __init__(self, vertex1: Point, vertex2: Point):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def is_horizontal(self) -> bool:
        return self.vertex1.y == self.vertex2.y

    def __repr__(self):
        return f"({self.vertex1}, {self.vertex2})"

    def intersects(self: "Line", other: "Line") -> bool:
        # due to axis aligned edges, parallel edges don't intersect
        if self.is_horizontal() == other.is_horizontal():
            return False
        if self.is_horizontal():
            horizontal_edge, vertical_edge = self, other
        else:
            horizontal_edge, vertical_edge = other, self
        # For vertical edge, y varies, x is constant
        # For horizontal edge, x varies, y is constant
        hx1, hx2 = horizontal_edge.vertex1.x, horizontal_edge.vertex2.x
        hy = horizontal_edge.vertex1.y
        vx = vertical_edge.vertex1.x
        vy1, vy2 = vertical_edge.vertex1.y, vertical_edge.vertex2.y
        # ensure point 1 is the minimum point
        if vy1 > vy2:
            vy1, vy2 = vy2, vy1
        if hx1 > hx2:
            hx1, hx2 = hx2, hx1
        # The intersection occurs if:
        # - The vertical edge's x is between the horizontal edge's x1 and x2
        # - The horizontal edge's y is between the vertical edge's y1 and y2
        return (hx1 < vx < hx2) and (vy1 < hy < vy2)

    def contains(self, other: Point) -> bool:
        if self.is_horizontal():
            if other.y != self.vertex1.y:
                return False
            x1, x2 = (self.vertex1.x, self.vertex2.x)
            if x1 > x2:
                x1, x2 = x2, x1
            return x1 <= other.x <= x2
        else:
            if other.x != self.vertex1.x:
                return False
            y1, y2 = (self.vertex1.y, self.vertex2.y)
            if y1 > y2:
                y1, y2 = y2, y1
            return y1 <= other.y <= y2


class AxisAlignedBoundingBox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.min_vertex = Point(xmin, ymin)
        self.max_vertex = Point(xmax, ymax)

    def contains(self, other: "AxisAlignedBoundingBox|Point") -> bool:
        if isinstance(other, AxisAlignedBoundingBox):
            return self.contains(other.min_vertex) and self.contains(other.max_vertex)
        if isinstance(other, Point):
            return (
                self.min_vertex.x <= other.x <= self.max_vertex.x
                and self.min_vertex.y <= other.y <= self.max_vertex.y
            )
        raise ValueError("Invalid type")


class Polygon:
    def __init__(self, coordinates: Sequence[Sequence[int]]):
        self.coordinates: List[Point] = [
            Point(coord[0], coord[1]) for coord in coordinates
        ]
        xs, ys = zip(*coordinates)
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        self.aabb = AxisAlignedBoundingBox(xmin, ymin, xmax, ymax)

    @property
    def edges(self) -> List[Line]:
        # an edge is the line between each adjacent vertex in coordinates, an edge
        # between the last & first coordinates is also included to create a full loop
        return [
            Line(self.coordinates[i], self.coordinates[(i + 1) % len(self.coordinates)])
            for i in range(len(self.coordinates))
        ]

    def contains(self, other: "Point|Polygon") -> bool:
        """
        Returns True if this polygon contains the other geometry.

        Incident geometry is considered containment. E.g. point on polygon edge,
        polygon's identical, polygon sharing an edge, etc...
        """
        if isinstance(other, Polygon):
            return self._contains_polygon(other)
        elif isinstance(other, Point):
            return self._contains_point(other)
        raise ValueError("Invalid type")

    def _contains_point(self, vertex: Point) -> bool:
        """
        Returns True if vertex is within polygon.

        Uses axis-aligned bounding box to determine if vertex is outside polygon as an
        optimization.

        If any vertex is same as polygon coordinate, consider inside.

        If point is on polygon edge consider inside.

        If point is inside axis-aligned bounding box, not shared vertex and not on an
        edge, then uses even-odd ray-casting algorithm to determine if point is
        inside polygon.
        """
        if not self.aabb.contains(vertex):
            return False
        for polygon_vertex in self.coordinates:
            if polygon_vertex == vertex:
                return True
        edge_crossing_count = 0
        for edge in self.edges:
            if edge.contains(vertex):
                return True
            if _ray_intersects_edge(vertex, edge):
                edge_crossing_count += 1
        # if odd number of edge crossings point is inside
        return edge_crossing_count % 2 == 1

    def _contains_polygon(self, other: "Polygon") -> bool:
        """
        Returns True if other polygon vertex is within this polygon.

        Check for axis-aligned bounding box containment as optimization.

        Polygon does not contain other polygon if any one vertex of the other is not
        contained. Short-circuit as soon as a vertex is found outside the polygon as
        an optimization.

         If all vertexes are contained, then check edges of polygon to be contained
         against each edge of polygon. Any intersecting edges indicate that the
         polygon edges cross and thus do not intersect. Short-circuit as soon as this
         test fails.  A polygon containing all vertices of another but still having
         edge intersections occurs when the containing polygon is concave.

         Polygon only contains the other if the following criteria are met:
         - axis-aligned bounding box contains other axis-aligned bounding box
         - polygon contains all vertices of other polygon
         - no edges of either polygon intersect
        """
        # aabb containment
        if not self.aabb.contains(other.aabb):
            return False
        # all vertex containment
        for vertex in other.coordinates:
            if not self.contains(vertex):
                return False
        # no edge intersections
        for edge1 in other.edges:
            for edge2 in self.edges:
                if edge1.intersects(edge2):
                    return False
        return True


class Box(Polygon):
    def __init__(self, corner1: Point | Sequence[int], corner2: Point | Sequence[int]):
        if not isinstance(corner1, Point):
            corner1, corner2 = Point(*corner1), Point(*corner2)
        xmin, xmax = min(corner1.x, corner2.x), max(corner1.x, corner2.x)
        ymin, ymax = min(corner1.y, corner2.y), max(corner1.y, corner2.y)
        bottom_left = xmin, ymin
        bottom_right = xmax, ymin
        top_right = xmax, ymax
        top_left = xmin, ymax
        super().__init__([bottom_left, bottom_right, top_right, top_left])

    @property
    def area(self) -> int:
        # increase by one, rectangles of a single row should still have area, likewise
        # when two corners are identical area should be 1 not zero
        xdiff = self.aabb.max_vertex.x - self.aabb.min_vertex.x + 1
        ydiff = self.aabb.max_vertex.y - self.aabb.min_vertex.y + 1
        return xdiff * ydiff


def _ray_intersects_edge(ray: Point, edge: Line):
    """
    Returns True if ray intersects edge.

    https://rosettacode.org/wiki/Ray-casting_algorithm#
    """
    a, b = edge.vertex1, edge.vertex2
    if a.y > b.y:
        a, b = b, a
    p = ray
    # degenerate case: ray on vertex - handle by shifting ray vertex y value up,
    # this causes only intersections on the "lower" vertex to count, this also
    # handles the case where the ray is on or collinear to the segment which is also
    # considered a non-intersection
    if p.y == a.y or p.y == b.y:
        p = Point(p.x, p.y + 1)

    # short-circuit checks
    if p.y < a.y or p.y > b.y:
        # ray y value is entirely above or below edge, no chance at intersection
        return False
    elif p.x >= max(a.x, b.x):
        # ray x value is right of edge, no intersection
        return False
    elif p.x < min(a.x, b.x):
        # ray x value is left of edge and y is between y extents, guaranteed to
        # intersect, y between extents is implied because it fails the first short
        # circuit check of y entirely above or below edge
        return True

    m_red = m_blue = float("inf")
    if a.x != b.x:
        m_red = (b.y - a.y) / (b.x - a.x)
    if a.x != p.x:
        m_blue = (p.y - a.y) / (p.x - a.x)
    return m_blue >= m_red


if __name__ == "__main__":
    total_part1 = 0
    total_part2 = 0

    with open(filename, "r") as f:
        lines = f.read()

    corners = [
        [int(value) for value in line.split(",")] for line in lines.split("\n") if line
    ]

    areas = [Box(c1, c2).area for c1, c2 in itertools.combinations(corners, 2)]
    max_area = max(areas)
    total_part1 = max_area

    # create a list of points with first point repeated at end to create a full loop
    red_green_tiles = Polygon(corners)
    max_area_part2 = 0
    for c1, c2 in tqdm(list(itertools.combinations(corners, 2))):
        rectangle = Box(c1, c2)
        area = rectangle.area
        if area < max_area_part2:
            continue
        if red_green_tiles.contains(rectangle):
            max_area_part2 = max(max_area_part2, area)
    total_part2 = max_area_part2

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")
