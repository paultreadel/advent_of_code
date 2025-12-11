import itertools
import re
from typing import List

import numpy as np
from scipy.optimize import LinearConstraint, milp

# filename = "sample.txt"
filename = "data.txt"


DEBUG = False


def button_wiring_to_output(wiring: List[int]) -> int:
    light_bit_array = 0
    for light in wiring:
        light_bit_array |= 1 << light
    return light_bit_array


def powerset(iterable):
    """
    Subsequences of the iterable from shortest to longest.

    Copied from python docs: https://docs.python.org/3/library/itertools.html#:~:text=counts))%0A%0Adef-,powerset,-(iterable)%3A
    """
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


class Machine:
    def __init__(self, instruction_text):
        num_lights, indicator_lights, button_wirings, joltages = (
            self._parse_instructions(instruction_text)
        )
        self.num_lights: int = num_lights
        self.indicator_lights: int = indicator_lights
        self.button_wirings: List[List[int]] = button_wirings
        # an integer that represents the binary changes that will occur when the
        # button is pressed
        self.button_outputs: List[int] = [
            button_wiring_to_output(lights) for lights in self.button_wirings
        ]
        self.joltages: List[int] = joltages
        if DEBUG:
            print(f"Number of Lights: {self.num_lights}")
            print(
                f"Indicator Lights: {self.indicator_lights}, "
                f"{self.indicator_lights:0{self.num_lights}b}"
            )
            print(f"Button Wirings: {self.button_wirings}")
            print(
                f"Button Outputs: {[(output, bin(output)) for output in self.button_outputs]}"
            )
            print(f"Joltages: {self.joltages}")

    @staticmethod
    def _parse_instructions(instruction_text):
        if DEBUG:
            print(f"Instructions: {instruction_text}")
        chunks = instruction_text.split()
        indicator_lights = re.sub(r"[\[\]]", "", chunks[0])
        num_lights = len(indicator_lights)
        # reverse pattern so first light is least significant bit, then replace
        # characters with 0s & 1s for conversion to integer representing the button
        # to light wiring binary array
        indicator_lights = int(
            indicator_lights[::-1].replace(".", "0").replace("#", "1"), 2
        )
        button_wirings = [
            list(map(int, re.findall(r"\d+", wiring))) for wiring in chunks[1:-1]
        ]
        joltages = list(map(int, chunks[-1][1:-1].split(",")))
        return num_lights, indicator_lights, button_wirings, joltages

    def start_machine(self) -> int:
        """
        Returns minimum number of presses for machine to match the indicator lights.

        Pressing a button twice is equivalent to doing nothing. Never test scenarios
        where two presses are completed.

        Like-wise pressing the same button three times is equivalent to pressing a
        button once. There-fore only need to test combinations of single button pushes.

        Button push order should not matter.

        Each tested combination either decides to push or not push each button.
        A combination is a list of button indices to push. An empty list means push
        no buttons. List [1,4] means push buttons at indices 1 and 4 but push no
        other buttons, and so on.
        """
        num_buttons = len(self.button_wirings)
        for button_index_pattern in powerset(range(num_buttons)):
            if self.test_button_pattern(button_index_pattern):
                return len(button_index_pattern)
        raise ValueError(
            "Machine should be possible to start with at least one button combination."
        )

    def test_button_pattern(self, button_indices: List[int]) -> bool:
        """
        Given a list of button indices returns True if pressing each of those buttons
        results in a matching indicator light pattern.

        Assumes lights all start at off.

        A button push is equivalent to an XOR between the button output and the
        current light state.  The button output is the integer representation of
        binary array of lights that will change when the button is pushed,
        it is derived from the button wiring details.

        If the current light state matches the indicator light
        value after all pushes in the pattern return True.
        """
        light_state = 0
        for idx in button_indices:
            button_output = self.button_outputs[idx]
            light_state ^= button_output
        return light_state == self.indicator_lights

    def set_joltage(self) -> int:
        """
        Formulate as linear integer programming problem.


        """
        # transform button outputs into a wiring matrix where each column is the
        # wiring pattern for that button, left-most column is first button (however
        # column ordering has no impact because button presses are summed), top row
        # is wiring for last joltage counter, this order is important needs to align
        # with corresponding joltages
        wiring_matrix = []
        for wiring in self.button_outputs:
            wiring_matrix.append(list(f"{wiring:0{self.num_lights}b}"))
        wiring_matrix = np.array(wiring_matrix).T.astype(int)
        # wiring_matrix = np.array(wiring_matrix).T.astype(int)
        joltages = np.flip(self.joltages)

        # formulated following example of https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html#:~:text=017%2D0130%2D5-,Examples,-Try%20it%20in

        # strict equality, upper and lower bounds must equal the joltages
        constraints = LinearConstraint(wiring_matrix, lb=joltages, ub=joltages)

        # all buttons have impact on minimization problem (one is this array),
        # don't use negative like example problem because we want to minimize which
        # is what milp does by default
        c = np.ones(wiring_matrix.shape[1])
        # enforce that number of button pushes must be integers
        integrality = np.ones_like(c)
        res = milp(c=c, constraints=constraints, integrality=integrality)
        if DEBUG:
            print("Wiring Matrix:\n", wiring_matrix)
            print("Joltages:\n", joltages)
            print("Optimization Result:\n", res.x, res.fun, sum(res.x))
            print(res)
        if not res.success:
            raise ValueError(
                "Optimization to find minimum number of button presses failed."
            )
        return int(res.fun)


if __name__ == "__main__":
    total_part1 = 0
    total_part2 = 0

    with open(filename, "r") as f:
        lines = f.read()

    for line in lines.split("\n"):
        machine = Machine(line)
        pushes = machine.start_machine()
        joltage_pushes = machine.set_joltage()
        if DEBUG:
            print(f"Pushes: {pushes}\n")
            print(f"Joltage Pushes: {joltage_pushes}\n")
        total_part1 += pushes
        total_part2 += joltage_pushes

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")
