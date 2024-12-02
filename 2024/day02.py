from itertools import pairwise
from math import copysign

MIN_LEVEL_CHANGE_ALLOWED = 1
MAX_LEVEL_CHANGE_ALLOWED = 3

if __name__ == "__main__":
    # parse input
    with open("data/day02.txt") as input_file:
        input_data = input_file.read()
    reports = [
        [int(level) for level in line.split()] for line in input_data.splitlines()
    ]

    def is_safe_report(report):
        changes = [a - b for a, b in pairwise(report)]
        change_direction = copysign(1, changes[0])
        for idx, change in enumerate(changes):
            level_change_within_tolerance = (
                MIN_LEVEL_CHANGE_ALLOWED <= abs(change) <= MAX_LEVEL_CHANGE_ALLOWED
            )
            change_directionally_consistent = copysign(1, change) == change_direction
            if not level_change_within_tolerance or not change_directionally_consistent:
                return False, idx
        return True, None

    num_safe_reports_part1 = 0
    for report in reports:
        safe_report, unsafe_idx = is_safe_report(report)
        if safe_report:
            num_safe_reports_part1 += 1
    print(f"Part 1: {num_safe_reports_part1}")

    num_safe_reports_part2 = 0
    for report in reports:
        safe_report, unsafe_idx = is_safe_report(report)
        if safe_report:
            num_safe_reports_part2 += 1
        else:
            # special case: if second transition found unsafe, check if removing the
            # first level makes the remainder of the report safe
            if unsafe_idx == 1:
                report_level_removed = report.copy()
                report_level_removed.pop(0)
                safe_report, _ = is_safe_report(report_level_removed)
                if safe_report:
                    num_safe_reports_part2 += 1
                    continue

            # check if removing one transition from either side of the unsafe
            # transition makes the entire report safe
            for offset in [0, 1]:
                report_level_removed = report.copy()
                report_level_removed.pop(unsafe_idx + offset)
                safe_report, _ = is_safe_report(report_level_removed)
                if safe_report:
                    num_safe_reports_part2 += 1
                    break
    print(f"Part 2: {num_safe_reports_part2}")
