import re

import cvxpy as cp
import numpy as np

if __name__ == "__main__":
    with open("data/day13.txt") as input_file:
        input_data = input_file.read()

    #     input_data = """Button A: X+94, Y+34
    # Button B: X+22, Y+67
    # Prize: X=8400, Y=5400
    #
    # Button A: X+26, Y+66
    # Button B: X+67, Y+21
    # Prize: X=12748, Y=12176
    #
    # Button A: X+17, Y+86
    # Button B: X+84, Y+37
    # Prize: X=7870, Y=6450
    #
    # Button A: X+69, Y+23
    # Button B: X+27, Y+71
    # Prize: X=18641, Y=10279"""

    machines = input_data.split("\n\n")

    total_tokens_part_one = 0
    total_tokens_part_two = 0
    for machine in machines:
        match_pattern = r"X[=+](\d+), Y[=+](\d+)"
        numbers = []
        for match in re.finditer(match_pattern, machine):
            numbers.append(tuple(map(int, match.groups())))
        *buttons, prize = numbers

        buttons = np.array(buttons)
        prize = np.array(prize) + 0

        x = cp.Variable(2, integer=True)
        a_token_cost = 3
        b_token_cost = 1
        minimize_tokens = cp.Minimize(x @ [a_token_cost, b_token_cost])
        constraints = [
            # position x (row 0), y (row 1)
            buttons.T @ x == prize,
            # num presses, scaler broadcasts so applies individually to each button
            0 <= x,
            x <= 100,
        ]

        problem = cp.Problem(
            minimize_tokens,
            constraints,
        )
        num_tokens = problem.solve()
        if problem.status == "optimal":
            total_tokens_part_one += int(num_tokens)
            total_tokens_part_two += int(x.value @ [a_token_cost, b_token_cost])
    print(total_tokens_part_one)
    print(total_tokens_part_two)
    # 56828585825849
    pass
