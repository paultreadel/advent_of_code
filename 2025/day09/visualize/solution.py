import itertools
import multiprocessing
from enum import Enum
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import shapely
import shapely.plotting
from constants import (
    MEDIA_DIR,
    PART1_EXAMPLE_FRAMES,
    PART1_PUZZLE_FRAMES,
    PART2_EXAMPLE_FRAMES,
)
from tqdm import tqdm
from video import generate_video

DEBUG = True
GRID_W = 13
GRID_H = 8


class COLORS(str, Enum):
    WHITE = "#FFFFFF"
    VERY_LIGHT_GRAY = "#FAFAFA"
    GRAY = "#BDBDBD"
    RED = "#E53935"
    GREEN = "#43A047"
    BLACK = "#000000"
    LIGHT_BLUE = "#8BC0EF"
    BLUE = "#1E88E5"
    PURPLE = "#8E24AA"
    LIGHT_PURPLE = "#CE93D8"
    YELLOW = "#FFD600"
    FOREST_GREEN = "#228B22"
    LIGHT_GRAY = "#F0F0F0"


Coord = Tuple[int, int]
Rect = Tuple[Coord, Coord]


def rectangle_area(corner1, corner2):
    x1, y1 = corner1
    x2, y2 = corner2
    # increase by one, rectangles of a single row should still have area, likewise
    # when two corners are identical area should be 1 not zero
    xdiff = abs(x1 - x2) + 1
    ydiff = abs(y1 - y2) + 1
    return xdiff * ydiff


def draw_grid(ax):
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, GRID_W + 0.5)
    ax.set_ylim(-0.5, GRID_H + 0.5)
    ax.set_xticks(range(GRID_W + 1), minor=False)
    ax.set_yticks(range(GRID_H + 1), minor=False)
    ax.set_xticklabels([str(x) for x in range(GRID_W + 1)])
    ax.set_yticklabels([str(y) for y in range(GRID_H + 1)])
    ax.tick_params(axis="both", which="major", length=0)
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.invert_yaxis()  # origin top-left for slides
    # Set all spines to GRAY color
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS.GRAY)

    # Draw white tiles for the entire grid
    tiles = [(x, y) for x in range(GRID_W + 1) for y in range(GRID_H + 1)]
    plot_tiles(ax, tiles, color=COLORS.VERY_LIGHT_GRAY, edgecolor=COLORS.GRAY)


def plot_tiles(
    ax,
    tiles: List[Coord],
    color: COLORS = COLORS.RED,
    edgecolor: COLORS = COLORS.BLACK,
    alpha: float = 1.0,
):
    xs, ys = zip(*tiles) if tiles else ([], [])
    # draw each tile as a rectangle with a black edges and fill as specified color
    # draw each tile as a rectangle patch
    for x, y in tiles:
        rect = plt.Rectangle(
            (x - 0.5, y - 0.5),
            1,
            1,
            facecolor=color,
            edgecolor=edgecolor,
            linewidth=0.5,
            alpha=alpha,
        )
        ax.add_patch(rect)


def rectangle_to_tiles(rect: Rect) -> List[Coord]:
    ((x1, y1), (x2, y2)) = rect
    # x1, y1 = c1
    # x2, y2 = c2
    xs = range(min(x1, x2), max(x1, x2) + 1)
    ys = range(min(y1, y2), max(y1, y2) + 1)
    return [(x, y) for x in xs for y in ys]


def make_static_grid_png(
    coords: List[Coord],
    filename: str,
    rectangle: Optional[Rect] = None,
    current_area: Optional[str] = None,
    max_area: Optional[str] = None,
    green_tiles: List[Coord] = None,
):
    fig, ax = plt.subplots(figsize=(6, 6))
    draw_grid(ax)
    plot_tiles(ax, coords)
    # plot green tiles if available
    if green_tiles:
        plot_tiles(ax, green_tiles, color=COLORS.GREEN)
    if rectangle:
        c1, c2 = rectangle
        tiles = rectangle_to_tiles(rectangle)
        if green_tiles:
            # plot blue with alpha to allow green tiles to be seen
            plot_tiles(ax, tiles, color=COLORS.BLUE, alpha=0.5)
        else:
            # plot light blue with full alpha to overwrite any tiles covered by the
            # rectangle
            plot_tiles(ax, tiles, color=COLORS.LIGHT_BLUE, alpha=1.0)
        # highlight corner tiles by drawing darker blue
        plot_tiles(ax, [c1, c2], color=COLORS.BLUE)
        # Add area text annotation below plot area
        ax.annotate(
            f"Current Area: {current_area}\nMax Area: {max_area}",
            xy=(0, GRID_H + 1),
            xycoords="data",
            ha="left",
            va="top",
            xytext=(0, 0),
            textcoords="offset points",
            annotation_clip=False,
        )

    save_png(filename, fig)


def save_png(path, fig):
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def initialize_poly_axes(rect):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.grid(False)
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.invert_yaxis()  # origin top-left for slides

    return fig, ax


class Rectangle:
    def __init__(self, rect=shapely.Polygon(), area=0, c1=None, c2=None):
        self.polygon = rect
        self.area = area
        self.c1 = c1
        self.c2 = c2


def draw_polygon_points(
    tiles: shapely.Polygon,
    filename: str,
    rect: Optional[Rectangle] = None,
    max_rect: Optional[Rectangle] = None,
    draw_edges=False,
):
    fig, ax = initialize_poly_axes(rect)
    if draw_edges:
        shapely.plotting.plot_polygon(
            tiles,
            ax=ax,
            facecolor=COLORS.LIGHT_GRAY,
            edgecolor=COLORS.GREEN,
            add_points=False,
        )
        markersize = 0.5
    else:
        markersize = 1.0
    shapely.plotting.plot_points(tiles, ax=ax, color=COLORS.RED, markersize=markersize)
    if rect:
        # draw shaded rectangle
        shapely.plotting.plot_polygon(
            rect.polygon,
            ax=ax,
            edgecolor=COLORS.BLUE,
            facecolor=COLORS.LIGHT_BLUE,
            linewidth=1.5,
            add_points=False,
            alpha=0.5,
        )
        # Draw text in the ax_text axes instead of using fig.text
        ax.text(
            0.01,
            0.03,
            f"Area: {rect.area:d}",
            ha="left",
            va="bottom",
            fontsize=10,
            color=COLORS.BLUE,
            transform=ax.transAxes,
        )
        ax.text(
            0.01,
            0.0,
            f"Max Area: {max_rect.area:d}",
            ha="left",
            va="bottom",
            fontsize=10,
            color=COLORS.PURPLE,
            transform=ax.transAxes,
        )
        # draw colored points at rectangle corners
        ax.plot(
            rect.c1[0],
            rect.c1[1],
            marker="o",
            color=COLORS.YELLOW,
            markersize=3,
        )
        ax.plot(
            rect.c2[0],
            rect.c2[1],
            marker="o",
            color=COLORS.FOREST_GREEN,
            markersize=3,
        )

    if max_rect:
        # draw shaded max area rectangle
        shapely.plotting.plot_polygon(
            max_rect.polygon,
            ax=ax,
            edgecolor=COLORS.PURPLE,
            facecolor=COLORS.LIGHT_PURPLE,
            linewidth=1.5,
            add_points=False,
            alpha=0.2,
        )
        # draw colored points at rectangle corners
        ax.plot(
            max_rect.c1[0],
            max_rect.c1[1],
            marker="o",
            color=COLORS.YELLOW,
            markersize=3,
            alpha=0.7,
        )
        ax.plot(
            max_rect.c2[0],
            max_rect.c2[1],
            marker="o",
            color=COLORS.FOREST_GREEN,
            markersize=3,
            alpha=0.7,
        )
    save_png(filename, fig)
    return ax


def corners_to_rectangle(c1, c2) -> Rectangle:
    x1, y1 = c1
    x2, y2 = c2
    rect = shapely.geometry.box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    area = rectangle_area(c1, c2)
    return Rectangle(rect, area, c1, c2)


class Frame:
    def __init__(self, rect, max_rect):
        self.rect = rect
        self.max_rect = max_rect

    def draw_frame(self, tiles, idx):
        draw_polygon_points(
            tiles,
            filename=f"{PART1_PUZZLE_FRAMES}/{idx:06d}.png",
            rect=self.rect,
            max_rect=self.max_rect,
        )


def draw_frame_wrapper(args):
    idx, frame, tiles = args
    frame.draw_frame(tiles, idx)


def multiprocessing_draw(tiles, frame_data):
    with multiprocessing.Pool() as pool:
        for _ in tqdm(
            pool.imap_unordered(
                draw_frame_wrapper,
                [(idx, frame, tiles) for idx, frame in enumerate(frame_data)],
            ),
            total=len(frame_data),
        ):
            pass


if __name__ == "__main__":
    with open("sample.txt", "r") as f:
        lines = f.read()

    example_corners = []
    for line in lines.split("\n"):
        values = line.split(",")
        example_corners.append((int(values[0]), int(values[1])))

    with open("data.txt", "r") as f:
        lines = f.read()

    puzzle_corners: List[Coord] = []
    for line in lines.split("\n"):
        values = line.split(",")
        puzzle_corners.append((int(values[0]), int(values[1])))

    # visualize part 1 example input
    make_static_grid_png(
        example_corners, filename=f"{MEDIA_DIR}/part1_grid_example.png"
    )
    max_area = 0
    for idx, (c1, c2) in enumerate(itertools.combinations(example_corners, 2)):
        area = rectangle_area(c1, c2)
        if area > max_area:
            max_area = area
        make_static_grid_png(
            example_corners,
            filename=f"{PART1_EXAMPLE_FRAMES}/{idx:03d}.png",
            rectangle=(c1, c2),
            current_area=area,
            max_area=max_area,
        )

    # visualize part 1 full puzzle input
    red_green_tiles = shapely.geometry.Polygon(puzzle_corners)
    draw_polygon_points(red_green_tiles, filename=f"{MEDIA_DIR}/part1_grid_puzzle.png")

    # capture all frames from the first k iterations, then only the largest rectangle
    # tested rectangle in all remaining frames, largest tested is largest within that
    # that iteration and not necessarily the max total rectangle observed across all
    # iterations, an iteration is defined as c1 being constant
    NUM_FULL_FRAME_ITERATIONS = 2
    max_rect = Rectangle()
    frame_data = []
    full_frame_iteration_count = 0
    max_iteration_rect = Rectangle()
    prev_c1 = None
    for c1, c2 in itertools.combinations(puzzle_corners, 2):
        # detect new c1 iteration, when it occurs capture the max rectangle from that
        # iteration, but only if all full frame iterations have been completed
        if prev_c1 != c1:
            # check if max iteration frame should be captured otherwise discard as it
            # was captured by full frame capture logic
            if full_frame_iteration_count > NUM_FULL_FRAME_ITERATIONS:
                frame_data.append(Frame(max_iteration_rect, max_rect))
            # reset for next iteration
            full_frame_iteration_count += 1
            max_iteration_rect = Rectangle()
            prev_c1 = c1

        rect = corners_to_rectangle(c1, c2)
        # check if rectangle is maximum rectangle from all tests
        if rect.area > max_rect.area:
            max_rect = rect
        # check if rectangle is maximum for this c1 iteration
        if rect.area > max_iteration_rect.area:
            max_iteration_rect = rect

        if full_frame_iteration_count <= NUM_FULL_FRAME_ITERATIONS:
            frame_data.append(Frame(rect, max_rect))
    multiprocessing_draw(red_green_tiles, frame_data)

    generate_video(PART1_EXAMPLE_FRAMES, "part1_example.mp4", 2)
    generate_video(PART1_PUZZLE_FRAMES, "part1_puzzle.mp4", 50)

    #######
    # visualize part 2 example input
    #######

    # get set of all green tiles on perimeter of polygon defined by loop of polygon
    # corners
    example_polygon = shapely.geometry.Polygon(example_corners)
    example_green_tiles = set()
    for i in range(int(example_polygon.length)):
        point_at_dist_i = example_polygon.exterior.interpolate(i)
        example_green_tiles.add(
            (int(round(point_at_dist_i.x)), int(round(point_at_dist_i.y)))
        )
    example_green_tiles = list(example_green_tiles.difference(example_corners))

    # draw example input with green tiles between each red corner on the loop
    make_static_grid_png(
        example_corners,
        filename=f"{MEDIA_DIR}/part2_grid_example.png",
        green_tiles=example_green_tiles,
    )

    max_area = 0
    for idx, (c1, c2) in enumerate(itertools.combinations(example_corners, 2)):
        # draw all rectangles, even if they are not contained
        area = rectangle_area(c1, c2)
        make_static_grid_png(
            example_corners,
            filename=f"{PART2_EXAMPLE_FRAMES}/{idx:03d}.png",
            rectangle=(c1, c2),
            current_area=area,
            max_area=area,
            green_tiles=example_green_tiles,
        )

    # visualize part 2 full puzzle input
    draw_polygon_points(
        red_green_tiles,
        filename=f"{MEDIA_DIR}/part2_grid_puzzle.png",
        draw_edges=True,
    )
    exit()

    # # create a list of points with first point repeated at end to create a full loop
    # points_ring = example_corners.copy()
    # points_ring.append(example_corners[0])
    # red_green_tiles = shapely.geometry.Polygon(example_corners)
    # max_area_part2 = 0
    # max_rectangle = shapely.Polygon()
    #
    # for c1, c2 in itertools.combinations(example_corners, 2):
    #     x1, y1 = c1
    #     x2, y2 = c2
    #     square_geom = shapely.geometry.box(
    #         min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
    #     )
    #     area = rectangle_area(c1, c2)
    #     if area < max_area_part2:
    #         continue
    #     if not red_green_tiles.contains(square_geom):
    #         continue
    #     area = rectangle_area(c1, c2)
    #     if area > max_area_part2:
    #         max_area_part2 = area
    #         max_rectangle = square_geom
    # total_part2 = max_area_part2
    #
    # import matplotlib.pyplot as plt
    # from shapely.plotting import plot_polygon
    #
    # fig, ax = plt.subplots()
    # plot_polygon(
    #     red_green_tiles,
    #     ax=ax,
    #     add_points=False,
    #     facecolor="lightblue",
    #     edgecolor="blue",
    # )
    # plot_polygon(
    #     max_rectangle,
    #     ax=ax,
    #     add_points=False,
    #     facecolor="violet",
    #     edgecolor="purple",
    # )
    # ax.set_aspect("equal", adjustable="datalim")
    # plt.show()
