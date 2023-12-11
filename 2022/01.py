day_num = __file__[-5:-3]
filepath = f"./data/{day_num}.txt"
# filepath = r"./data/input_sample.txt"

with open(filepath) as fp:
    input = fp.read()

calories = [[int(x) for x in l.splitlines()] for l in input.split("\n\n")]

total_calories_by_elf = [sum(l) for l in calories]

max_calories = max(total_calories_by_elf)
print(f"{max_calories=}")

top_three_calories = sorted(total_calories_by_elf, reverse=True)[:3]

total_top_three = sum(top_three_calories)

print(f"{total_top_three=}")