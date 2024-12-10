import matplotlib.pyplot as plt  # noqa: I001
import moviepy
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.ticker import MultipleLocator
from tqdm import tqdm

MultipleLocator(base=0.5, offset=1.0)


if __name__ == "__main__":
    # parse input
    # with open("data/day06.txt") as input_file:
    #     input_data = input_file.read()

    input_data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    input_data = """....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#..."""

    def draw_grid_figure(grid, characters):
        size_x = len(grid) - 1
        size_y = len(grid[0]) - 1

        Y_OFFSET = 0.6

        fig, ax = plt.subplots(figsize=(8, 8))
        # ax.axis("off")
        # set axis limits
        ax.set_xlim(-0.5, size_x + 0.5)
        ax.set_ylim(Y_OFFSET - 1, size_y + (1 - Y_OFFSET))
        # turn on minor grid at 1 unit intervals starting at 0.5
        grid_ticker = MultipleLocator(base=1.0, offset=0.5)
        # ax.set_xticks(range(11), minor=True)
        # ax.set_yticks(range(11), minor=True)
        ax.grid(which="major", color="black", linestyle="-", linewidth=2)
        # ax.grid(which="minor", color="black", linestyle="-", linewidth=1)
        # turn off major ticks
        # ax.minorticks_on()
        ax.xaxis.set_major_formatter(plt.NullFormatter())
        ax.yaxis.set_major_formatter(plt.NullFormatter())
        ax.xaxis.set_minor_formatter(plt.FormatStrFormatter("%d"))
        ax.yaxis.set_minor_formatter(plt.FormatStrFormatter("%d"))
        ax.xaxis.set_minor_locator(MultipleLocator(base=1.0))
        ax.yaxis.set_minor_locator(MultipleLocator(base=1.0))

        # ax.tick_params(which="major", axis="x", labeltop=True, labelbottom=True)
        ax.tick_params(which="major", length=0)
        ax.xaxis.tick_top()
        ax.spines["bottom"].set_position(("data", Y_OFFSET - 1))
        # turn off minor tick labels
        # ax.tick_params(which="minor", length=0, labelsize=0)
        ax.xaxis.set_major_locator(MultipleLocator(base=1.0, offset=0.5))
        ax.yaxis.set_major_locator(MultipleLocator(base=1.0, offset=(1 - Y_OFFSET)))
        ax.invert_yaxis()

        for char in characters:
            (i, j), char, color = char
            ax.text(j, i, char, ha="center", va="center", fontsize=20, color=color)
        return fig

    grid = [list(row) for row in input_data.split("\n")]

    def get_chars(grid):
        chars = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != ".":
                    char = grid[i][j]
                    match char:
                        case "^":
                            color = "green"
                        case "#":
                            color = "black"
                        case "O":
                            color = "blue"
                        case _:
                            color = "red"
                    chars.append(((i, j), char, color))
        return chars

    input_data = """....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#..."""

    grid = [list(row) for row in input_data.split("\n")]
    chars = get_chars(grid)
    fig = draw_grid_figure(grid, chars)
    fig.show()

    input_data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    grid = [list(row) for row in input_data.split("\n")]
    chars = get_chars(grid)
    fig = draw_grid_figure(grid, chars)
    fig.show()

    # up, right, down, left, ordered so each increment of 1 in the index will rotate
    # the direction 90 degrees clockwise
    DIRECTIONS = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]
    guard_chars_to_directions = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }

    def find_guard_start_cell_and_direction(grid):
        guard_chars = "^v<>"
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] in guard_chars:
                    start_direction = guard_chars_to_directions[grid[i][j]]
                    grid[i][j] = "."
                    return (i, j), start_direction
        return None

    def is_cell_in_bounds(cell, grid):
        i, j = cell
        return 0 <= i < len(grid) and 0 <= j < len(grid[0])

    def is_cell_traversable(cell, grid):
        i, j = cell
        return grid[i][j] == "."

    def find_guard_path(grid, start, direction):
        current_cell = start

        # function returns an ordered path to allow part 2 to optimize checking for
        # loops on simulated obstacle position by starting the guard at position `n-1`
        # if an obstacle is placed at position `n`
        ordered_path = [(start, direction)]

        # use set to improve performance when checking if a cell/dir has been visited
        # indicating a loop has been found
        _visited_path = {(start, direction)}

        while True:
            i, j = current_cell
            di, dj = direction
            next_cell = (i + di, j + dj)
            if not is_cell_in_bounds(next_cell, grid):
                return ordered_path, False
            if is_cell_traversable(next_cell, grid):
                current_cell = next_cell
                if (current_cell, direction) in _visited_path:
                    return ordered_path, True
                ordered_path.append((current_cell, direction))
                _visited_path.add((current_cell, direction))
            else:
                direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

    start_cell, start_direction = find_guard_start_cell_and_direction(grid)

    # part 1
    guard_path, _ = find_guard_path(grid, start_cell, start_direction)
    unique_cells = set(cell for cell, _ in guard_path)
    print(f"Part 1: {len(unique_cells)}")

    # part 2
    checked_cells = set()
    num_looping_obstructions = 0
    for idx, (cell, dir) in tqdm(enumerate(guard_path), total=len(guard_path)):
        if cell in checked_cells or idx == 0:
            continue
        # place an obstacle at the current cell, don't create a copy of the grid to
        # reduce runtime, instead update individual elements of the grid in place and
        # reset them after each loop check
        i, j = cell
        grid[i][j] = "#"

        # check for loop in guard path with new obstacle present but start check at
        # the previous cell & direction to speed up loop detection
        prev_cell, prev_dir = guard_path[idx - 1]
        _, is_loop = find_guard_path(grid, prev_cell, prev_dir)
        if is_loop:
            num_looping_obstructions += 1

        # remove the obstacle after checking for loops
        grid[i][j] = "."

        # add cell to list of checked cells, this prevents the same cell from being
        # double counted if it is visited multiple times by the guard
        checked_cells.add(cell)
    print(f"Part 2: {num_looping_obstructions}")

    def get_obstacles(grid, color="black"):
        obstacles = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "#":
                    obstacles.append(((i, j), "#", color))
        return obstacles

    obstacles = get_obstacles(grid)

    guard_directions_to_chars = {
        dir_val: char for char, dir_val in guard_chars_to_directions.items()
    }

    def mplfig_to_npimage(fig):
        """Converts a matplotlib figure to a RGB frame after updating the canvas"""
        #  only the Agg backend now supports the tostring_rgb function
        canvas = FigureCanvasAgg(fig)
        canvas.draw()  # update/draw the elements

        # get the width and the height to resize the matrix
        l, b, w, h = canvas.figure.bbox.bounds
        w, h = int(w), int(h)

        #  exports the canvas to a string buffer and then to a numpy nd.array
        buf = canvas.tostring_rgb()
        image = np.frombuffer(buf, dtype=np.uint8)
        return image.reshape(h, w, 3)

    def create_frame(grid, obstacles, guard_state, path):
        chars = []
        chars.extend(obstacles)
        chars.extend(path)
        if guard_state:
            guard_pos, guard_direction = guard_state
            guard_char = guard_directions_to_chars[guard_direction]
            chars += ((guard_pos, guard_char, "green"),)
        fig = draw_grid_figure(grid, chars)
        frame = mplfig_to_npimage(fig)
        plt.close(fig)
        return frame

    visited_cells = set()
    frames = []
    for guard_state in tqdm(guard_path):
        frame = create_frame(grid, obstacles, guard_state, visited_cells)
        frames.append(frame)
        visited_cells.add((guard_state[0], "X", "red"))
    frames.append(create_frame(grid, obstacles, None, visited_cells))

    clip = moviepy.ImageSequenceClip(frames, fps=2)
    clip.write_videofile("guard_path.mp4", codec="libx264")

    pass
