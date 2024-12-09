if __name__ == "__main__":
    with open("data/day09.txt") as input_file:
        input_data = input_file.read()

    input_data = """2333133121414131402"""
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
        disk_as_chars = [str(file_id) if file_id >= 0 else "." for file_id in disk]
        print("".join(disk_as_chars))

    def defrag(disk):
        idx_head = 0
        for idx_tail in reversed(range(len(disk))):
            if idx_head >= idx_tail:
                break
            print_disk(disk)
            for idx_head in range(idx_head, idx_tail):
                id_tail = disk[idx_tail]
                id_head = disk[idx_head]
                if id_head >= 0:
                    # space not free
                    continue
                disk[idx_head], disk[idx_tail] = id_tail, id_head
                break

    def disk_size(disk):
        size = 0
        for idx, file_id in enumerate(disk):
            if file_id >= 0:
                size += file_id * idx
        return size

    disk_unit_blocks = []
    for file_id, size in disk:
        disk_unit_blocks.extend([file_id] * size)

    disk_defrag_part_one = defrag(disk_unit_blocks)
    print(f"Part 1: {disk_size(disk_unit_blocks)}")

    pass
