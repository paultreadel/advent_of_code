if __name__ == "__main__":
    # parse input
    with open("data/day05.txt") as input_file:
        input_data = input_file.read()

    rules, updates = input_data.split("\n\n")
    rules = [list(map(int, line.split("|"))) for line in rules.splitlines()]
    updates = [list(map(int, line.split(","))) for line in updates.splitlines()]

    def update_follows_rules(update):
        for lh_page, rh_page in rules:
            if lh_page not in update or rh_page not in update:
                continue
            if update.index(lh_page) > update.index(rh_page):
                return False
        # only return True after checking all rules and finding no violations
        return True

    part_one_total = 0
    part_two_total = 0
    for update in updates:
        if update_follows_rules(update):
            middle_page_idx = len(update) // 2
            part_one_total += update[middle_page_idx]
        else:
            # keep checking rules and swapping pages if a violation is found until the
            # order is valid
            while not update_follows_rules(update):
                for lh, rh in rules:
                    if lh not in update or rh not in update:
                        # if update doesn't contain both pages skip this rule
                        continue
                    idx_lh = update.index(lh)
                    idx_rh = update.index(rh)
                    if idx_lh > idx_rh:
                        # swap lh and rh if they are in the wrong order
                        update[idx_lh], update[idx_rh] = rh, lh
            middle_page_idx = len(update) // 2
            part_two_total += update[middle_page_idx]

    print(f"Part 1: {part_one_total}")
    print(f"Part 2: {part_two_total}")
