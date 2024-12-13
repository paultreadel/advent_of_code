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

    a_token_cost = 3
    b_token_cost = 1

    total_tokens_part_one = 0
    for offset in [0, 10000000000000]:
        for machine in input_data.split("\n\n"):
            match_pattern = r"X[=+](\d+), Y[=+](\d+)"
            numbers = []
            for match in re.finditer(match_pattern, machine):
                numbers.append(tuple(map(int, match.groups())))
            *buttons, prize = numbers

            # I don't know why this works and the cvxpy solution doesn't for part 2,
            # they should both be solving a system of lineara equations
            buttons = np.array(buttons).T
            prize = np.array(prize) + offset
            presses = np.linalg.solve(buttons, prize).round()
            if np.all(buttons @ presses == prize):
                num_tokens = presses[0] * a_token_cost + presses[1] * b_token_cost
                total_tokens_part_one += int(num_tokens)

            # (a_x, a_y), (b_x, b_y) = np.array(buttons)
            # prize_x, prize_y = np.array(prize) + offset
            #
            # a_presses = cp.Variable(integer=True)
            # b_presses = cp.Variable(integer=True)
            # minimize_tokens = cp.Minimize(
            #     a_presses * a_token_cost + b_presses * b_token_cost
            # )
            # constraints = [
            #     a_x * a_presses + b_x * b_presses == prize_x,
            #     a_y * a_presses + b_y * b_presses == prize_y,
            #     0.0 <= a_presses,
            #     0.0 <= b_presses,
            # ]
            #
            # problem = cp.Problem(
            #     minimize_tokens,
            #     constraints,
            # )
            # num_tokens = problem.solve()
            # if problem.status == "optimal":
            #     total_tokens_part_one += int(num_tokens)
        print(total_tokens_part_one)
