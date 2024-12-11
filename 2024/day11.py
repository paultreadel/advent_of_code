from functools import lru_cache
from pprint import pprint  # noqa: F401

if __name__ == "__main__":
    with open("data/day11.txt") as input_file:
        input_data = input_file.read()

    # input_data = """125 17"""

    stones = list(map(int, input_data.split()))

    @lru_cache(maxsize=None)
    def count_stone_after_blinks(stone, blinks):
        if blinks == 0:
            return 1
        if stone == 0:
            stone_count = count_stone_after_blinks(1, blinks - 1)
        elif len(str(stone)) % 2 == 0:
            chars = str(stone)
            midpoint = len(chars) // 2
            stone_count = count_stone_after_blinks(
                int(chars[:midpoint]),
                blinks - 1,
            ) + count_stone_after_blinks(
                int(chars[midpoint:]),
                blinks - 1,
            )
        else:
            stone_count = count_stone_after_blinks(stone * 2024, blinks - 1)
        return stone_count

    num_stones = sum(count_stone_after_blinks(stone, 25) for stone in stones)
    print(f"Part 1: {num_stones}")

    num_stones = sum(count_stone_after_blinks(stone, 75) for stone in stones)
    print(f"Part 2: {num_stones}")
