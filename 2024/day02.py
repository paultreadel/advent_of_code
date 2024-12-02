from itertools import pairwise
from math import copysign

MIN_LEVEL_CHANGE_ALLOWED = 1
MAX_LEVEL_CHANGE_ALLOWED = 3

if __name__ == "__main__":
    # parse input
    with open("data/day02.txt") as input_file:
        input_data = input_file.read()
        input_data = """7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9"""
    reports = [
        [int(level) for level in line.split()] for line in input_data.splitlines()
    ]
    consecutive_differences = [
        [a - b for a, b in pairwise(report)] for report in reports
    ]
    safe_reports = []
    for differences in consecutive_differences:
        directions = [copysign(1, d) for d in differences]
        is_direction_same = all((d == directions[0] for d in directions))
        if not is_direction_same:
            safe_reports.append(False)
            continue
        magnitudes = [abs(d) for d in differences]
        is_level_change_tolerable = (
            min(magnitudes) >= MIN_LEVEL_CHANGE_ALLOWED
            and max(magnitudes) <= MAX_LEVEL_CHANGE_ALLOWED
        )
        safe_reports.append(is_direction_same and is_level_change_tolerable)

    print(f"Part 1: {sum(safe_reports)}")
    pass
