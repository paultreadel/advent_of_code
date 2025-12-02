# filename = "sample.txt"
filename = "data.txt"

DEBUG = False


if __name__ == "__main__":
    with open(filename, "r") as f:
        lines = f.read()
    invalid_id_total_part1 = 0
    invalid_id_total_part2 = 0
    for value in lines.split(","):
        first_id, last_id = value.split("-")
        invalid_ids = []
        invalid_ids_part2 = []
        for _id in range(int(first_id), int(last_id) + 1):
            _id = str(_id)
            middle_index = len(_id) // 2
            first_half = _id[:middle_index]
            second_half = _id[middle_index:]
            if first_half == second_half:
                invalid_ids.append(_id)
                invalid_id_total_part1 += int(_id)
                continue

            # offset by one for indexing
            for offset in range(1, len(first_half) + 1):
                base_pattern = _id[:offset]
                remaining_chunk = _id[offset:]
                pattern = base_pattern * ((len(_id) - offset) // offset)
                if pattern == remaining_chunk:
                    invalid_ids.append(_id)
                    invalid_id_total_part2 += int(_id)

        if DEBUG:
            print(invalid_ids)
    print(f"Part 1: {invalid_id_total_part1}")
    print(f"Part 2: {invalid_id_total_part1 + invalid_id_total_part2}")
