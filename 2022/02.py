day_num = __file__[-5:-3]
filepath = f"./data/{day_num}.txt"
# filepath = r"./data/input_sample.txt"

with open(filepath) as fp:
    input = fp.read()

input_as_strategy = input.translate(str.maketrans("ABCXYZ", "RPSRPS"))
rounds = [l.split() for l in input_as_strategy.splitlines()]

winning_move = {"R": "P", "P": "S", "S": "R"}
score_by_move = {"R": 1, "P": 2, "S": 3}

total_score = 0
for opponent, player in rounds:
    move_score = score_by_move[player]
    if opponent == player:
        winner_score = 3
    else:
        winner_score = (winning_move[opponent] == player) * 6
    round_score = move_score + winner_score
    total_score += round_score
print(f"{total_score=}")

input_as_outcome = input.translate(str.maketrans("ABC", "RPS"))
rounds = [l.split() for l in input_as_outcome.splitlines()]

# X = lose, Y = draw, Z = win
move_to_achieve_outcome = {
    "R": {"X": "S", "Y": "R", "Z": "P"},
    "P": {"X": "R", "Y": "P", "Z": "S"},
    "S": {"X": "P", "Y": "S", "Z": "R"},
}

total_score = 0
for opponent, outcome in rounds:
    player = move_to_achieve_outcome[opponent][outcome]
    move_score = score_by_move[player]
    if opponent == player:
        winner_score = 3
    else:
        winner_score = (winning_move[opponent] == player) * 6
    round_score = move_score + winner_score
    total_score += round_score
print(f"{total_score=}")
