from collections import deque
from copy import deepcopy

from tqdm import tqdm

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

    def next_contiguous_space_of_size(lst: deque, size: int):
        data = deepcopy(lst)
        idx_start = 0
        while idx_start < len(data):
            is_free = True
            for idx in range(size):
                if data[idx] != ".":
                    is_free = False
                    idx_start += 1
                    data.rotate(-1)
                    break
            if is_free:
                return idx_start
        return -1

    def sort_data_part_two(lst: deque, file_size_by_id: dict):
        checked_sizes = set()
        for _id, size in tqdm(
            reversed(file_size_by_id.items()), total=len(file_size_by_id)
        ):
            if size in checked_sizes:
                continue
            idx_start = next_contiguous_space_of_size(lst, size)
            if idx_start == 0:
                idx_id_unsorted = lst.index(_id)
                for idx in range(size):
                    lst[idx_start + idx] = _id
                    lst[idx_id_unsorted + idx] = "."
            elif idx_start < 0:
                checked_sizes.add(size)
                continue
            else:
                idx_id_unsorted = lst.index(_id)
                if idx_start > idx_id_unsorted:
                    continue
                for idx in range(size):
                    lst[idx_start + idx] = _id
                    lst[idx_id_unsorted + idx] = "."
        return lst

    sorted_files = sort_data(deque(file_list))
    total_part_one = 0
    for idx, file_id in enumerate(sorted_files):
        total_part_one += file_id * idx

    sorted_files = sort_data_part_two(deque(file_list), deepcopy(file_size_by_id))
    total_part_two = 0
    for idx, file_id in enumerate(sorted_files):
        if isinstance(file_id, int):
            total_part_two += file_id * idx

    print(f"Part 1: {total_part_one}")
    print(f"Part 2: {total_part_two}")
