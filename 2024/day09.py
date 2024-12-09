from itertools import chain

if __name__ == "__main__":
    with open("data/day09.txt") as input_file:
        input_data = input_file.read()

    # input_data = """2333133121414131402"""
    # input_data = """12345"""

    disk = []
    file_id = 0
    for idx, char in enumerate(input_data):
        if idx % 2:
            disk.append((-1, int(char)))
        else:
            disk.append((file_id, int(char)))
            file_id += 1

    def print_disk(disk):
        disk_as_chars = []
        for file_id, size in disk:
            if file_id >= 0:
                disk_as_chars.extend(str(file_id) * size)
            else:
                disk_as_chars.extend("." * size)
        print("".join(disk_as_chars))

    def defrag(disk, debug=False):
        is_idx_head_contiguous = True
        idx_head_contiguous = 0
        update_made = True
        for idx_tail in reversed(range(len(disk))):
            if debug and update_made:
                update_made = False
                print_disk(disk)
            if idx_head_contiguous >= idx_tail:
                break
            for idx_head in range(idx_head_contiguous, idx_tail):
                id_tail, size_tail = disk[idx_tail]
                id_head, size_head = disk[idx_head]
                if id_head >= 0:
                    # head space not free, next head idx
                    continue
                elif id_tail < 0:
                    # tail has free space, go to next tail idx
                    break

                if size_head >= size_tail:
                    update_made = True
                    disk[idx_head] = (id_head, size_head - size_tail)
                    disk[idx_tail] = (id_head, size_tail)
                    disk.insert(idx_head, (id_tail, size_tail))
                    if size_head == size_tail:
                        # remove zero size allocations, this significantly reduces
                        # the number of iterations
                        disk.pop(idx_head + 1)
                        pass
                else:
                    # file doesn't fit in head space, go to next head idx
                    # mark that idx_head is no longer in the starting contiguous block
                    is_idx_head_contiguous = False
                    continue
                if is_idx_head_contiguous:
                    idx_head_contiguous = idx_head
                if debug and update_made:
                    update_made = False
                    print_disk(disk)
        return disk

    def disk_size(disk):
        size = 0
        disk = chain.from_iterable([[file_id] * size for file_id, size in disk])
        for idx, file_id in enumerate(disk):
            if file_id >= 0:
                size += file_id * idx
        return size

    disk_unit_blocks = []
    for file_id, size in disk:
        disk_unit_blocks.extend([(file_id, 1)] * size)

    disk_defrag_part_one = defrag(disk_unit_blocks)
    print(f"Part 1: {disk_size(disk_unit_blocks)}")

    disk_defrag_part_two = defrag(disk, debug=False)
    print(f"Part 2: {disk_size(disk_defrag_part_two)}")
