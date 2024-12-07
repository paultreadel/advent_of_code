import operator
import re
from itertools import product
from time import perf_counter

if __name__ == "__main__":
    with open("data/day07.txt") as input_file:
        input_data = input_file.read()

    lines = input_data.splitlines()
    _EQUATIONS = [
        [int(s) for s in re.split(":? ", line)] for line in (input_data.splitlines())
    ]

    ########################################
    print("Iterative implementation")
    ########################################

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

    tic = perf_counter()
    total_part_one = process_equations_with_operators(
        [operator.add, operator.mul],
    )
    print(f"Part 1: {total_part_one}")

    total_part_two = process_equations_with_operators(
        [operator.add, operator.mul, "||"],
    )
    print(f"Part 2: {total_part_two}")
    toc = perf_counter()
    print(f"Time: {toc - tic:0.4f} seconds")

    ########################################
    print("Recursive implementation")
    ########################################

    def process_operator(op, a, b):
        match op:
            case "+":
                return a + b
            case "*":
                return a * b
            case "||":
                return int(str(a) + str(b))
            case _:
                raise ValueError(f"Unknown operator: {op}")

    def process_params(result_input, params, ops, solution):
        if not params:
            return result_input == solution
        elif result_input > solution:
            return False
        for op in ops:
            result_op = process_operator(op, result_input, params[0])
            if process_params(result_op, params[1:], ops, solution):
                return True

    def process_equations_with_operators(with_concat):
        total = 0
        for equation in _EQUATIONS:
            solution = equation[0]
            parameters = equation[1:]
            if process_params(parameters[0], parameters[1:], with_concat, solution):
                total += solution
        return total

    tic = perf_counter()
    total_part_one = process_equations_with_operators(("+", "*"))
    print(f"Part 1: {total_part_one}")

    total_part_two = process_equations_with_operators(("||", "+", "*"))
    print(f"Part 2: {total_part_two}")
    toc = perf_counter()
    print(f"Time: {toc - tic:0.4f} seconds")
