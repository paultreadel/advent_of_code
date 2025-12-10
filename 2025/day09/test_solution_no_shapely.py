import pytest
from solution_no_shapely import (
    Edge,
    Polygon,
    Vertex,
    _ray_intersects_edge,
)


@pytest.mark.parametrize(
    "ray, edge, expected",
    [
        pytest.param(
            Vertex(2, 2),
            Edge(Vertex(1, 1), Vertex(3, 3)),
            True,
            id="inside edge segment",
        ),
        pytest.param(
            Vertex(0, 0),
            Edge(Vertex(1, 1), Vertex(3, 3)),
            False,
            id="outside edge segment",
        ),
        pytest.param(
            Vertex(0, 0), Edge(Vertex(0, 0), Vertex(3, 3)), True, id="at edge start"
        ),
        pytest.param(
            Vertex(3, 3), Edge(Vertex(0, 0), Vertex(3, 3)), False, id="at edge end"
        ),
        pytest.param(
            Vertex(1, 3), Edge(Vertex(0, 0), Vertex(3, 3)), False, id="crosses edge end"
        ),
        pytest.param(
            Vertex(2, 0),
            Edge(Vertex(3, 0), Vertex(0, 3)),
            True,
            id="crosses diagonal edge",
        ),
        pytest.param(
            Vertex(-1, 0),
            Edge(Vertex(0, 0), Vertex(3, 0)),
            False,
            id="crosses edge & collinear",
        ),
        pytest.param(
            Vertex(-1, 0),
            Edge(Vertex(1, -1), Vertex(1, 0)),
            False,
            id="crosses edge end, edge vertices swapped",
        ),
        pytest.param(
            Vertex(0, 0),
            Edge(Vertex(0, 0), Vertex(4, 0)),
            False,
            id="on edge start - horizontal",
        ),
        pytest.param(
            Vertex(4, 0),
            Edge(Vertex(0, 0), Vertex(4, 0)),
            False,
            id="on edge end - horizontal",
        ),
        pytest.param(
            Vertex(4, 0),
            Edge(Vertex(4, 4), Vertex(4, 0)),
            False,
            id="on edge start - vertical",
        ),
        pytest.param(
            Vertex(4, 4),
            Edge(Vertex(4, 4), Vertex(4, 0)),
            False,
            id="on edge start - vertical",
        ),
        pytest.param(
            Vertex(0, 0),
            Edge(Vertex(4, 4), Vertex(4, 0)),
            True,
            id="crosses edge start - vertical",
        ),
        pytest.param(
            Vertex(4, 4),
            Edge(Vertex(4, 4), Vertex(4, 0)),
            False,
            id="crosses edge end - vertical",
        ),
        pytest.param(
            Vertex(-1, 0),
            Edge(Vertex(0, 0), Vertex(4, 0)),
            False,
            id="crosses edge start - horizontal",
        ),
        pytest.param(
            Vertex(-1, 0),
            Edge(Vertex(0, 0), Vertex(4, 0)),
            False,
            id="crosses edge end - horizontal",
        ),
    ],
)
def test_ray_intersects_edge(ray, edge, expected):
    intersects = _ray_intersects_edge(ray, edge)
    assert expected == intersects


def test_point_in_polygon():
    polygon = Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)])
    # points on bottom edge
    assert polygon.contains(Vertex(-1, -2)) is True
    assert polygon.contains(Vertex(1, -2)) is True
    # points on right edge
    assert polygon.contains(Vertex(2, -1)) is True
    assert polygon.contains(Vertex(2, 1)) is True
    # points on top edge
    assert polygon.contains(Vertex(-1, 2)) is True
    assert polygon.contains(Vertex(1, 2)) is True
    # points on left edge
    assert polygon.contains(Vertex(-2, 1)) is True
    assert polygon.contains(Vertex(-2, -1)) is True


def test_edge_intersects_edge():
    edge_1 = Edge(Vertex(0, -2), Vertex(0, 2))
    edge_2 = Edge(Vertex(-2, 0), Vertex(2, 0))
    assert edge_1.intersects(edge_2) is True
    # corners match, 90 degree
    edge_1 = Edge(Vertex(0, 0), Vertex(0, 2))
    edge_2 = Edge(Vertex(0, 2), Vertex(2, 2))
    assert edge_1.intersects(edge_2) is False
    # corners match, in-line
    edge_1 = Edge(Vertex(0, 0), Vertex(0, 2))
    edge_2 = Edge(Vertex(0, 2), Vertex(0, 4))
    assert edge_1.intersects(edge_2) is False


def test_polygon_in_polygon_polygon_entirely_inside():
    polygon1 = Polygon([(1, 1), (1, 1), (1, 1), (1, 1)])
    polygon2 = Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)])
    assert polygon2.contains(polygon1) is True


def test_polygon_in_polygon_polygon_entirely_outside():
    polygon1 = Polygon([(3, 3), (4, 3), (4, 4), (3, 4)])
    polygon2 = Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)])
    assert polygon2.contains(polygon1) is False


def test_polygon_in_polygon_polygon_same_as_polygon():
    polygon1 = Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)])
    polygon2 = Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)])
    assert polygon2.contains(polygon1) is True


def test_polygon_in_polygon_polygon_on_polygon_edges():
    polygon1 = Polygon([(-2, -1), (2, -1), (2, 1), (-2, 1)])
    polygon2 = Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)])
    assert polygon2.contains(polygon1) is True

    polygon1 = Polygon([(-1, -2), (1, -2), (1, 2), (-1, 2)])
    polygon2 = Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)])
    assert polygon2.contains(polygon1) is True
