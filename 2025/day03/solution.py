import string

filename = "sample.txt"
# filename = "data.txt"

DEBUG = False


def max_joltage_search(joltages, joltage_idx, total_joltage_value, joltage_cap="9"):
    # exit if joltage index is at end of joltages
    if joltage_idx >= len(joltages) - 1:
        return False, total_joltage_value
    original_joltage_idx = joltage_idx
    for joltage in reversed(string.digits[1 : int(joltage_cap) + 1]):
        if joltage not in joltages[joltage_idx:]:
            continue
        joltage_idx = original_joltage_idx
        joltage_idx = joltages[joltage_idx:].index(joltage) + joltage_idx
        total_joltage_value += joltages[joltage_idx]
        joltage_idx += 1
        if len(total_joltage_value) == 12:
            return True, total_joltage_value
        search_status, total_joltage_value = max_joltage_search(
            joltages, joltage_idx, total_joltage_value
        )
        if search_status:
            break
        # search failed, reset back to original index, pop failed digit off list and
        # continue to next lowest number
        joltage_idx = original_joltage_idx
        total_joltage_value = total_joltage_value[:-1]
    while len(total_joltage_value) != 12:
        joltage_cap = str(int(total_joltage_value[-1]) - 1)
        original_joltage_idx -= 1
        joltage_idx = original_joltage_idx
        total_joltage_value = total_joltage_value[:-1]
        search_status, total_joltage_value = max_joltage_search(
            joltages, joltage_idx, total_joltage_value, joltage_cap
        )
        if search_status:
            break
    return True, total_joltage_value


if __name__ == "__main__":
    with open(filename, "r") as f:
        lines = f.read()
    total_part1 = 0
    total_part2 = 0
    # invalid_id_total_part2 = 0
    for joltage_bank in lines.split("\n"):
        joltages = [int(char) for char in joltage_bank]
        bank_max_joltage_candidates = []
        for joltage in range(1, 10):
            if joltage not in joltages:
                continue
            joltage_idx = joltages.index(joltage)
            if joltage_idx >= len(joltages) - 1:
                continue
            max_val = max(joltages[joltage_idx + 1 :])
            bank_max_joltage_candidates.append(int(str(joltage) + str(max_val)))
            print(joltages, bank_max_joltage_candidates)
        total_part1 += max(bank_max_joltage_candidates)

        _, total_joltage_value = max_joltage_search(joltage_bank, 0, "")
        print(total_joltage_value)
        total_part2 += int(total_joltage_value)
    print(f"Part 1: {total_part1}")
    print(f"Part 1: {total_part2}")
