import re

if __name__ == "__main__":
    # parse input
    with open("data/day03.txt") as input_file:
        input_data = input_file.read()
    # input_data = (
    #     """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    # )

    # part 1
    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pattern, input_data)
    matches_multiplied = [int(a) * int(b) for a, b in matches]
    total_part_1 = sum(matches_multiplied)
    print(f"Part 1: {total_part_1}")

    # part 2
    pattern = r"mul\((\d+),(\d+)\)|(do(?:n't)?\(\))"
    matches = re.findall(pattern, input_data)
    total_part_2 = 0
    multiply_flag = True
    for a, b, flag in matches:
        if flag:
            if flag == "do()":
                multiply_flag = True
            elif flag == "don't()":
                multiply_flag = False
            continue

        if multiply_flag:
            total_part_2 += int(a) * int(b)
    print(f"Part 2: {total_part_2}")

    # part 2 alternative
    pattern = r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))"
    total_part_2 = 0
    multiply_flag = True
    for a, b, do, dont in re.findall(pattern, input_data):
        if do or dont:
            multiply_flag = bool(do)
        else:
            if multiply_flag:
                total_part_2 += int(a) * int(b)
    print(f"Part 2 (alternative): {total_part_2}")
