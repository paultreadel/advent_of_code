import re


def parse_game_data(input_data):
    parsed_data = []
    for game_data in input_data:
        matches = re.search(r"Game (?P<game_number>\d+): (?P<draw_data>.*)", game_data)
        draws = matches["draw_data"].split("; ")
        parsed_draw_data = [draw_to_cube_count(draw) for draw in draws]
        parsed_data.append((int(matches["game_number"]), parsed_draw_data))
    return parsed_data


def is_valid_game(game_draws, red=12, green=13, blue=14):
    for draw in game_draws:
        if (
            (draw.get("red", 0) > red)
            | (draw.get("green", 0) > green)
            | (draw.get("blue", 0) > blue)
        ):
            return False
    return True


def draw_to_cube_count(draw):
    count_with_color = [s.split(" ") for s in draw.split(", ")]
    return {color: int(count) for count, color in count_with_color}


def part_one(parsed_data):
    valid_games = filter(lambda x: is_valid_game(x[1]), parsed_data)
    game_sum = sum(game_number for game_number, _ in valid_games)
    print(f"{game_sum=}")
    return valid_games


def min_cube_count_by_color(game_data):
    reds = [x.get("red", 0) for x in game_data]
    greens = [x.get("green", 0) for x in game_data]
    blues = [x.get("blue", 0) for x in game_data]
    return max(reds) * max(greens) * max(blues)


def part_two(parsed_data):
    game_power = sum(
        [min_cube_count_by_color(game_data[1]) for game_data in parsed_data]
    )
    print(f"{game_power=}")


if __name__ == "__main__":
    with open("data/day02_input.txt") as input_file:
        input_data = input_file.readlines()
    parsed_game_data = parse_game_data(input_data)
    part_one(parsed_game_data)
    part_two(parsed_game_data)
