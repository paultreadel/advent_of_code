import itertools
from typing import List, Sequence

from tqdm import tqdm

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


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Edge:
    def __init__(self, vertex1: Vertex, vertex2: Vertex):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def is_horizontal(self) -> bool:
        return self.vertex1.y == self.vertex2.y

    def __repr__(self):
        return f"({self.vertex1}, {self.vertex2})"

    def intersects(self: "Edge", other: "Edge") -> bool:
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
        if vy1 > vy2:
            vy1, vy2 = vy2, vy1
        if hx1 > hx2:
            hx1, hx2 = hx2, hx1
        # The intersection occurs if:
        # - The vertical edge's x is between the horizontal edge's x1 and x2
        # - The horizontal edge's y is between the vertical edge's y1 and y2
        return (hx1 < vx < hx2) and (vy1 < hy < vy2)

    def contains(self, other: Vertex) -> bool:
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
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.min_vertex = Vertex(xmin, ymin)
        self.max_vertex = Vertex(xmax, ymax)

    def contains(self, other: "AxisAlignedBoundingBox") -> bool:
        if isinstance(other, AxisAlignedBoundingBox):
            return self.contains(other.min_vertex) and self.contains(other.max_vertex)
        if isinstance(other, Vertex):
            return (
                self.xmin <= other.x <= self.xmax and self.ymin <= other.y <= self.ymax
            )
        raise ValueError("Invalid type")


class Polygon:
    def __init__(self, coordinates: Sequence[Sequence[int]]):
        self.coordinates: List[Vertex] = [
            Vertex(coord[0], coord[1]) for coord in coordinates
        ]
        xs, ys = zip(*coordinates)
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        self.aabb = AxisAlignedBoundingBox(xmin, ymin, xmax, ymax)

    @property
    def edges(self) -> List[Edge]:
        # an edge is the line between each adjacent vertex in coordinates, an edge
        # between the last & first coordinates is also included to create a full loop
        return [
            Edge(self.coordinates[i], self.coordinates[(i + 1) % len(self.coordinates)])
            for i in range(len(self.coordinates))
        ]

    @classmethod
    def from_rectangle(cls, vertex1: Vertex, vertex2: Vertex):
        xmin, xmax = min(vertex1.x, vertex2.x), max(vertex1.x, vertex2.x)
        ymin, ymax = min(vertex1.y, vertex2.y), max(vertex1.y, vertex2.y)
        bottom_left = xmin, ymin
        bottom_right = xmax, ymin
        top_right = xmax, ymax
        top_left = xmin, ymax
        return cls([bottom_left, bottom_right, top_right, top_left])

    def contains(self, other: "Vertex|Polygon") -> bool:
        if isinstance(other, Polygon):
            return self._contains_polygon(other)
        elif isinstance(other, Vertex):
            return self._contains_point(other)
        raise ValueError("Invalid type")

    def _contains_point(self, vertex: Vertex) -> bool:
        """
        Returns True if vertex is within polygon.

        Uses axis-aligned bounding box to determine if vertex is outside polygon as an
        optimization.

        If any vertex is same as polygon coordinate, consider inside.

        If point is on polygon edge consider inside.

        If not outside polygon, then uses even-odd ray-casting algorithm to determine if
        point is inside polygon.  Points exactly aligned with polygon edges require
        """
        if not self.aabb.contains(vertex):
            return False
        for polygon_vertex in self.coordinates:
            if polygon_vertex == vertex:
                return True
        count = 0
        for edge in self.edges:
            if edge.contains(vertex):
                return True
            if _ray_intersects_edge(vertex, edge):
                count += 1
        # if odd point is inside
        return count % 2 == 1

    def _contains_polygon(self, other: "Polygon") -> bool:
        if not self.aabb.contains(other.aabb):
            return False
        for vertex in other.coordinates:
            if not self.contains(vertex):
                return False
        for edge1 in other.edges:
            for edge2 in self.edges:
                if edge1.intersects(edge2):
                    return False
        return True


def _ray_intersects_edge(ray: Vertex, edge: Edge):
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
        p = Vertex(p.x, p.y + 1)

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
    # b.y >= a.y required to cover case where ray intersects the vertex in this case,
    # a crossing on only the minimum vertex is considered an intersection, when the
    # two y-s are equal then the ray is on the edge and parallel
    # return m_blue >= m_red
    return m_blue >= m_red


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
    red_green_tiles = Polygon(corners)
    areas_part2 = []
    for c1, c2 in tqdm(list(itertools.combinations(corners, 2))):
        x1, y1 = c1
        x2, y2 = c2
        square_geom = Polygon.from_rectangle(Vertex(*c1), Vertex(*c2))
        if red_green_tiles.contains(square_geom):
            areas_part2.append(rectangle_area(c1, c2))
    total_part2 = max(areas_part2)

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")
