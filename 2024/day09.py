from collections import deque
from copy import deepcopy

from tqdm import tqdm

if __name__ == "__main__":
    with open("data/day09.txt") as input_file:
        input_data = input_file.read()

    input_data = """2333133121414131402"""
    # input_data = """12345"""

    file_size_by_id = {}
    free_space_by_idx = {}

    idx_start = 0
    file_id = 0
    # (id, size, start_idx)
    file_system = deque()
    for idx, char in enumerate(input_data):
        if idx % 2 == 0:
            file_size_by_id[file_id] = int(char)
            file_system.append((file_id, int(char), idx_start))
            file_id += 1
        else:
            free_space_by_idx[idx_start] = int(char)
            file_system.append((".", int(char), idx_start))
        idx_start += int(char)

    def sort_data(file_system: deque, file_size_by_id: dict, free_space_by_idx: dict):
        file_system = deepcopy(file_system)
        file_size_by_id = deepcopy(file_size_by_id)
        file_ids = list(file_size_by_id)

        sorted_file_system = []
        file_id = None
        last_file_size = 0
        while file_system:
            if last_file_size == 0:
                file_id, last_file_size, file_idx_start = file_system.popleft()
            if file_id == ".":
                next_file_id = file_ids.pop()
                next_file_size = file_size_by_id.pop(next_file_id)
                file_system.remove()
                _, _, next_file_idx_start = file_system.pop()
                size_to_write = 0
                while last_file_size > 0:
                    size_to_write += 1
                    last_file_size -= 1
                    next_file_size -= 1
                    if next_file_size == 0:
                        break

                sorted_file_system.append((next_file_id, size_to_write))
                if next_file_size > 0:
                    file_ids.append(next_file_id)
                    file_size_by_id[next_file_id] = next_file_size
                    file_system.append(
                        (
                            next_file_id,
                            next_file_size,
                            next_file_idx_start,
                        )
                    )
            else:
                sorted_file_system.append((file_id, last_file_size))
                file_size_by_id.pop(file_id)
                last_file_size = 0
        return sorted_file_system

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

    sorted_files = sort_data(file_system, file_size_by_id, free_space_by_idx)
    total_part_one = 0
    idx = 0
    for file_id, file_size in sorted_files:
        for _ in range(file_size):
            total_part_one += file_id * idx
            idx += 1

    # sorted_files = sort_data_part_two(deque(file_list), deepcopy(file_size_by_id))
    # total_part_two = 0
    # for idx, file_id in enumerate(sorted_files):
    #     if isinstance(file_id, int):
    #         total_part_two += file_id * idx

    print(f"Part 1: {total_part_one}")
    # print(f"Part 2: {total_part_two}")
