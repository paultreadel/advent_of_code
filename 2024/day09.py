from collections import deque
from copy import deepcopy

if __name__ == "__main__":
    with open("data/day09.txt") as input_file:
        input_data = input_file.read()

    input_data = """2333133121414131402"""
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

    def sort_data(lst: deque):
        sorted_files = []
        while lst:
            file_id = lst.popleft()
            if isinstance(file_id, int):
                sorted_files.append(file_id)
            else:
                while lst:
                    next_file_id = lst.pop()
                    if isinstance(next_file_id, int):
                        sorted_files.append(next_file_id)
                        break
        return sorted_files

    def sort_data_part_two(lst: deque, file_size_by_id: dict):
        sorted_files = []
        while lst:
            file_id = lst.popleft()
            if isinstance(file_id, int):
                if file_id in file_size_by_id:
                    for _ in range(file_size_by_id.pop(file_id)):
                        sorted_files.append(file_id)
                else:
                    continue
            else:
                free_space_size = 0
                while lst:
                    free_space_size += 1
                    if isinstance(lst[0], int):
                        break
                    lst.popleft()
                while (
                    free_space_size > 0
                    and min(file_size_by_id.values()) <= free_space_size
                ):
                    for _id, size in dict(reversed(file_size_by_id.items())).items():
                        if size <= free_space_size:
                            for _ in range(size):
                                sorted_files.append(_id)
                            del file_size_by_id[_id]
                            while _id in lst:
                                lst.remove(_id)
                            free_space_size -= size
                            if free_space_size == 0:
                                break
                    else:
                        break

                pass
        return sorted_files

    # sorted_files = sort_data(deque(file_list))
    # total_part_one = 0
    # for idx, file_id in enumerate(sorted_files):
    #     total_part_one += file_id * idx

    sorted_files = sort_data_part_two(deque(file_list), deepcopy(file_size_by_id))
    pass

    # print(f"Part 1: {total_part_one}")
    # print(f"Part 2: {len(unique_antinodes_part_two)}")
