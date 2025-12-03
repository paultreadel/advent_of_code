import string

filename = "sample.txt"
filename = "data.txt"

DEBUG = False


def max_joltage_search(joltages, total_joltage_value, max_joltage_value=9):
    # build max joltage from right to left, strategy is to find the largest number
    # searching from right to left, repeating until a string of 12 characters is
    # completed, if length of the remaining joltages ever drops below the number of
    # characters required to reach 12 then backtracking is required by searching the
    # next lowest digit
    if not joltages:
        return False, total_joltage_value
    if len(total_joltage_value) == 12:
        return True, total_joltage_value
    if len(joltages) + len(total_joltage_value) < 12:
        return False, total_joltage_value
    joltage_idx = None
    descending_digits_capped = string.digits[max_joltage_value:0:-1]
    for digit in descending_digits_capped:
        joltage = str(digit)
        if joltage not in joltages:
            continue
        joltage_idx = joltages.index(joltage)
        total_joltage_value += joltage
        break

    if joltage_idx is None:
        raise ValueError(
            "No valid joltage found. A check before the descending search is "
            "executed should be added to handle this case."
        )
    search_status, total_joltage_value = max_joltage_search(
        joltages[joltage_idx + 1 :], total_joltage_value
    )
    if search_status or len(total_joltage_value) == 12:
        return True, total_joltage_value

    # search failed backtrack, but cap search for joltage one less than the value
    # that failed
    total_joltage_value = total_joltage_value[:-1]
    search_status, total_joltage_value = max_joltage_search(
        joltages, total_joltage_value, int(joltage) - 1
    )
    return search_status, total_joltage_value


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
            if DEBUG:
                print(joltages, bank_max_joltage_candidates)
        total_part1 += max(bank_max_joltage_candidates)

        _, total_joltage_value = max_joltage_search(joltage_bank, "")
        if DEBUG:
            print(total_joltage_value)
        total_part2 += int(total_joltage_value)
    print(f"Part 1: {total_part1}")
    print(f"Part 1: {total_part2}")
