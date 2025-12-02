day_num = __file__[-5:-3]
filepath = f"./data/{day_num}.txt"
# filepath = r"./data/input_sample.txt"

with open(filepath) as fp:
    input = fp.read()


def item_priority(item):
    if item.islower():
        priority = ord(item) - 96  # "a" is at 97, priority starts at 1
    else:
        priority = ord(item) - 64 + 26  # "A" at 65, but add 26 too it follow
    return priority


total_priority = 0
total_group_priority = 0
group_items = []
for idx, contents in enumerate(input.splitlines()):
    sz = len(contents)
    comp1, comp2 = set(contents[: sz // 2]), set(contents[sz // 2 :])
    shared_item = comp1.intersection(comp2).pop()
    priority = item_priority(shared_item)
    total_priority += priority

    group_items.append(set(contents))
    if (idx % 3) == 2:  # every 3rd bag
        group_item = set.intersection(*group_items).pop()
        group_priority = item_priority(group_item)
        total_group_priority += group_priority
        group_items = []


print(f"{total_priority=}")
print(f"{total_group_priority=}")
