from typing import List, Tuple


class ValueMaps:
    def __init__(self, map_string):
        lines_no_title = map_string.split("\n")[1:]

        self.maps: List[Tuple[int, int, int]] = []
        for line in lines_no_title:
            dst, src, size = [int(x) for x in line.split()]
            src_end = src + size
            offset = dst - src
            self.maps.append((src, src_end, offset))

    def next_value(self, x):
        for src_start, src_end, offset in self.maps:
            if src_start <= x < src_end:
                return x + offset
        return x

    def next_ranges(self, ranges):
        next_ranges = []
        for src_start, src_end, offset in self.maps:
            not_in_source = []
            while ranges:
                r_start, r_end = ranges.pop()

                # range entirely before or after source interval
                if (r_end < src_start) | (r_start > src_end):
                    not_in_source.append((r_start, r_end))
                    continue

                # find any interval that may occur before source start
                interval_before = (min(r_start, src_start), src_start)

                # find the interval contained by source, squeezing to the smallest size
                # if entirely contained
                interval_within = (max(r_start, src_start), min(r_end, src_end))

                # find any interval that may occur after source end
                interval_after = (src_end, max(r_end, src_end))

                # if valid intervals found before and after source start/end
                # respectively add to list that will check these partial intervals
                # against the other maps
                if interval_before[1] > interval_before[0]:
                    not_in_source.append(interval_before)
                if interval_after[1] > interval_after[0]:
                    not_in_source.append(interval_after)

                # for the interval contained by this range adjust by offset value
                # defined by the src->dst mapping
                next_ranges.append(tuple(x + offset for x in interval_within))

            # set ranges to the list of ranges not found in this mapping and prepare
            # to check for these values in the other mappings
            ranges = not_in_source

        # all mappings checked any intervals remaining in ranges now are returned
        # with no offset, combine these with the next ranges which contains any
        # ranges found that needed an offset applied
        return ranges + next_ranges


def part_one(seeds, value_mappings):
    locations = []
    for seed in seeds:
        for _map in value_mappings:
            seed = _map.next_value(seed)
        locations.append(seed)
    min_location = min(locations)
    print(f"{min_location=}")


def part_two(seeds, mappings):
    seeds_iter = iter(seeds)
    seed_ranges = [(start, start + _len) for start, _len in zip(seeds_iter, seeds_iter)]

    locations = []
    for seed_range in seed_ranges:
        ranges = [seed_range]
        for _map in mappings:
            ranges = _map.next_ranges(ranges)
            # ranges = _map.apply_range(ranges)
        locations.append(min(start for start, _ in ranges))
    min_location = min(locations)
    print(f"{min_location=}")


def parse_input(data):
    seeds, *mapping_groups = data.split("\n\n")
    seeds = [int(s) for s in seeds.split(":")[1].split()]

    value_mappings = [ValueMaps(s) for s in mapping_groups]
    return seeds, value_mappings


if __name__ == "__main__":
    input_filepath = "data/day05_input.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()
    parsed_seeds, parsed_maps = parse_input(input_data)
    part_one(parsed_seeds, parsed_maps)
    part_two(parsed_seeds, parsed_maps)
