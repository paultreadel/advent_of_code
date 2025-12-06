import numpy as np

# filename = "sample.txt"
filename = "data.txt"


DEBUG = True

symbol_to_operation_map = {
    "+": np.sum,
    "*": np.prod,
}

if __name__ == "__main__":
    total_part1 = 0
    total_part2 = 0

    with open(filename, "r") as f:
        lines = f.read()

    parsed_values = []
    for line in lines.split("\n"):
        parsed_line = [text for text in line.split()]
        parsed_values.append(parsed_line)

    operations = parsed_values.pop()
    numbers = np.asarray(parsed_values, dtype=int)

    for idx, column in enumerate(numbers.T):
        op = operations[idx]
        total_part1 += symbol_to_operation_map[op](column)

    # part 2
    lines_list = lines.split("\n")
    # remove last row containing operations
    lines_list.pop()
    longest_line_length = max(len(line) for line in lines_list)
    lines_padded = [line.ljust(longest_line_length) for line in lines_list]
    char_list = [list(line) for line in lines_padded]

    char_array = np.asarray(char_list, dtype=str)

    # transpose so columns become first array dimension
    problem_idx = 0
    problem_values = []
    for col in char_array.T:
        try:
            value = int("".join(col).strip())
            problem_values.append(value)
        except ValueError:
            # ValueError raises when column of all spaces is encountered, all spaces
            # indicates problem break, perform op on accumulated values and update
            # for next problem
            op = operations[problem_idx]
            total = symbol_to_operation_map[op](problem_values)
            total_part2 += total
            problem_idx += 1
            problem_values = []

    op = operations[problem_idx]
    total = symbol_to_operation_map[op](problem_values)
    total_part2 += total

    pass

    print(f"Part 1: {total_part1}")
    print(f"Part 1: {total_part2}")
