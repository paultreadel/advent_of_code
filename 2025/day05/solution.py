import bisect
from typing import List

# filename = "sample.txt"
filename = "data.txt"


def coalesce_intervals(intervals: List[List[int]]) -> List[List[int]]:
    merged_intervals = []
    for start, end in sorted(intervals):
        # base case - first interval is appended directly
        if not merged_intervals:
            merged_intervals.append([start, end])
            continue

        # check if start outside end of previous interval
        if start >= merged_intervals[-1][1]:
            # append interval, no overlap
            merged_intervals.append([start, end])
        else:
            # extend interval to the max of this end or the previous interval end,
            # after sorting (by start then end) some intervals may be entirely
            # contained by the previous interval
            merged_intervals[-1][1] = max(merged_intervals[-1][1], end)
    return merged_intervals


def is_fresh(intervals, ingredient_id):
    # note: decrement by one as bisect returns index of next element position where
    # value should be inserted to keep list sorted
    idx = bisect.bisect_right(intervals, ingredient_id, key=lambda i: i[0]) - 1
    # ensure index is valid, if ingredient is smaller than any interval index is -1,
    # and likewise if larger will be the length of the intervals list
    if idx == len(intervals) or idx < 0:
        return False
    # check if value is within the interval, required because the value could fall in
    # the interval or in the empty period between the interval that may contain this
    # ingredient and the next
    return intervals[idx][0] <= ingredient_id <= intervals[idx][1]


DEBUG = True

if __name__ == "__main__":
    with open(filename, "r") as f:
        lines = f.read()
    (fresh_id_ranges_text, ingredient_id_text) = lines.split("\n\n")

    id_ranges = []
    for s in fresh_id_ranges_text.split("\n"):
        start, end = s.split("-")
        id_ranges.append([int(start), int(end) + 1])

    merged_id_ranges = coalesce_intervals(id_ranges)

    total_part1 = 0
    total_part2 = 0
    for ingredient_id in ingredient_id_text.split("\n"):
        if is_fresh(merged_id_ranges, int(ingredient_id)):
            total_part1 += 1

    for start, end in merged_id_ranges:
        total_part2 += end - start

    print(f"Part 1: {total_part1}")
    print(f"Part 1: {total_part2}")
