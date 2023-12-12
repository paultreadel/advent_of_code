import time
from functools import lru_cache
from typing import List


@lru_cache(maxsize=256)
def layout_permutations(layout, runs):
    if not runs:
        # valid if no non-working springs remain
        return 1 if "#" not in layout else 0
    elif not layout:
        # layout is empty and runs remain (invalid)
        return 0

    next_char = layout[0]
    sz = runs[0]

    if next_char == ".":
        # drop working spring and get remaining permutations
        valid_perm = layout_permutations(layout[1:], runs)
        return valid_perm

    elif next_char == "#":  # next run start
        # check if chars of next run have no working springs (invalid run)
        next_run = layout[:sz]
        if "." not in next_run:
            # valid only if char after run is a working/unknown spring
            if layout[sz] in ".?":
                # force char after valid run to be working even if unknown
                remaining_layout = "." + layout[(sz + 1) :]
                valid_perm = layout_permutations(remaining_layout, runs[1:])
                return valid_perm
            else:
                return 0
        else:
            return 0  # invalid permutation

    elif next_char in "?":  # need to test both working/non conditions of "?"
        # need to test both working/non-working spring conditions
        layout_working = layout.replace("?", ".", 1)
        layout_nonworking = layout.replace("?", "#", 1)
        valid_perm_working = layout_permutations(layout_working, runs)
        valid_perm_nonworking = layout_permutations(layout_nonworking, runs)
        return valid_perm_working + valid_perm_nonworking
    else:
        assert False, "Should not happen"


def part_one(input):
    runs: List
    total_perms = 0
    for layout, runs in input:
        layout = layout + "."  # add working spring to end to simplify validity checks
        perms = layout_permutations(layout, runs)
        total_perms += perms
    print(f"{total_perms=}")
    print(layout_permutations.cache_info())


def part_two(input):
    runs: List
    total_perms = 0
    for layout, runs in input:
        layout = "?".join([layout] * 5)
        runs = runs * 5
        layout = layout + "."  # add working spring to end to simplify validity checks
        perms = layout_permutations(layout, runs)
        total_perms += perms
    print(f"{total_perms=}")
    print(layout_permutations.cache_info())
    pass


def parse_input(data):
    layouts, run_lengths = zip(*(line.split() for line in data.splitlines()))
    run_lengths = [tuple(int(x) for x in s.split(",")) for s in run_lengths]
    return list(zip(layouts, run_lengths))


if __name__ == "__main__":
    input_filepath = "data/day12_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()

    data = parse_input(input_data)
    part_one(data)
    start_time = time.time()
    part_two(data)
    elapsed_time = time.time() - start_time
    print(f"{elapsed_time=}")
