import operator
import re
from itertools import product

if __name__ == "__main__":
    with open("data/day07.txt") as input_file:
        input_data = input_file.read()

    lines = input_data.splitlines()
    _EQUATIONS = [
        [int(s) for s in re.split(":? ", line)] for line in (input_data.splitlines())
    ]

    def process_equations_with_operators(operator_choices):
        total = 0
        for equation in _EQUATIONS:
            solution = equation[0]
            parameters = equation[1:]
            for operators in product(operator_choices, repeat=len(parameters) - 1):
                result = parameters[0]
                for op, param in zip(operators, parameters[1:]):
                    if op == "||":
                        result = int(str(result) + str(param))
                    else:
                        result = op(result, param)
                if result == solution:
                    total += solution
                    break
        return total

    total_part_one = process_equations_with_operators(
        [operator.add, operator.mul],
    )
    print(f"Part 1: {total_part_one}")

    total_part_two = process_equations_with_operators(
        [operator.add, operator.mul, "||"],
    )
    print(f"Part 2: {total_part_two}")
