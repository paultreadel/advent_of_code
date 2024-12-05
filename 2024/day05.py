from collections import defaultdict
from graphlib import TopologicalSorter

if __name__ == "__main__":
    # parse input
    with open("data/day05.txt") as input_file:
        input_data = input_file.read()

    # input_data = """47|53
    # 97|13
    # 97|61
    # 97|47
    # 75|29
    # 61|13
    # 75|53
    # 29|13
    # 97|29
    # 53|29
    # 61|53
    # 97|53
    # 61|29
    # 47|13
    # 75|47
    # 97|75
    # 47|61
    # 75|61
    # 47|29
    # 75|13
    # 53|13
    #
    # 75,47,61,53,29
    # 97,61,53,29,13
    # 75,29,13
    # 75,97,47,61,53
    # 61,13,29
    # 97,13,75,29,47"""

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

    print("Topological sort approach")

    rules, updates = input_data.split("\n\n")
    rules = [list(map(int, line.split("|"))) for line in rules.splitlines()]
    updates = [list(map(int, line.split(","))) for line in updates.splitlines()]

    rules_as_graph = defaultdict(set)
    for lh, rh in rules:
        rules_as_graph[rh].add(lh)

    # Part 1
    pt_1_total = 0
    pt_2_total = 0
    for update in updates:
        # filter rules graph to only include pages from this update
        updates_rule_graph = {
            page: rules_as_graph[page].intersection(update) for page in update
        }
        topo_sorted_update = list(TopologicalSorter(updates_rule_graph).static_order())
        idx_mid = len(update) // 2
        if topo_sorted_update == update:
            pt_1_total += update[idx_mid]
        else:
            pt_2_total += topo_sorted_update[idx_mid]

    print(pt_1_total)
    print(pt_2_total)
