if __name__ == "__main__":
    with open("data/day09.txt") as input_file:
        input_data = input_file.read()

    # input_data = """2333133121414131402"""
    # input_data = """12345"""

    file_size_by_id = {}
    free_spaces = []

    file_id = 0
    file_list = []
    for idx, char in enumerate(input_data):
        if idx % 2 == 0:
            file_size_by_id[file_id] = int(char)
            file_list.extend([file_id] * int(char))
            file_id += 1
        else:
            free_spaces.append(int(char))
            file_list.extend(["."] * int(char))

    def is_organized(lst: list):
        min_free_space = next(idx for idx, x in enumerate(lst) if x == ".")
        max_char_space = next(
            len(lst) - 1 - idx
            for idx, x in enumerate(reversed(lst))
            if isinstance(x, int)
        )
        return min_free_space > max_char_space, min_free_space, max_char_space

    list_is_organized, idx_min_free_space, idx_max_char_space = is_organized(file_list)
    while not list_is_organized:
        file_list[idx_min_free_space], file_list[idx_max_char_space] = (
            file_list[idx_max_char_space],
            file_list[idx_min_free_space],
        )
        list_is_organized, idx_min_free_space, idx_max_char_space = is_organized(
            file_list
        )
    total_part_one = 0
    for idx, file_id in enumerate(file_list):
        if isinstance(file_id, int):
            total_part_one += file_id * idx
        else:
            break

    print(f"Part 1: {total_part_one}")
    # print(f"Part 2: {len(unique_antinodes_part_two)}")
