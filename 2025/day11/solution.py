from functools import cache
from pprint import pprint

# filename = "sample.txt"
# filename = "sample_part2.txt"
filename = "data.txt"


DEBUG = False


if __name__ == "__main__":
    total_part1 = 0
    total_part2 = 0

    with open(filename, "r") as f:
        lines = f.read()

    # input lines contains the device and its downstream connections
    server_network = dict()
    for line in lines.split("\n"):
        device, remaining_line = line.split(": ")
        server_network[device] = remaining_line.split()

    if DEBUG:
        pprint(server_network, sort_dicts=False)

    @cache
    def count_paths(source, target):
        if source == target:
            return 1
        down_stream_paths = 0
        for next_device in server_network.get(source, []):
            down_stream_paths += count_paths(next_device, target)
        return down_stream_paths

    total_part1 += count_paths("you", "out")

    total_part2 += 1
    total_part2 *= count_paths(source="svr", target="fft")
    total_part2 *= count_paths(source="fft", target="dac")
    total_part2 *= count_paths(source="dac", target="out")

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")
