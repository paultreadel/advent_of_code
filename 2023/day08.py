import math
from itertools import cycle
from typing import Dict, List, Callable


class Node:
    def __init__(self, l, r):
        self.l, self.r = l, r

    def step(self, direction):
        if direction == "L":
            return self.l
        elif direction == "R":
            return self.r
        else:
            raise ValueError(f"Input {direction=} not recognized.")


class Graph:
    def __init__(self, nodes, start, ending_rule):
        self.nodes: Dict[str:Node] = {
            name: Node(*neighbors) for name, neighbors in nodes
        }

        if not isinstance(start, list):
            start = [start]
        self.start: List[str] = start
        self.is_done: Callable = ending_rule

    def navigate(self, directions: List[str]):
        self._validate_directions(directions)

        directions = cycle(directions)
        steps_by_start = []
        for current_node_name in self.start:
            steps = 0
            while not self.is_done(current_node_name):
                dir = next(directions)
                current_node_name = self.nodes[current_node_name].step(dir)
                steps += 1
            steps_by_start.append(steps)
        steps = math.lcm(*steps_by_start)
        return steps

    @staticmethod
    def _validate_directions(directions):
        valid_directions = {"L", "R"}
        invalid_values = valid_directions.symmetric_difference(directions)
        if invalid_values:
            raise ValueError(
                f"Navigation direction input only allows: "
                f"{valid_directions}\n\t Found values: {invalid_values}"
            )


def part_one(directions, nodes):
    ending_rule = lambda node: node == "ZZZ"
    graph = Graph(nodes, "AAA", ending_rule)
    num_steps = graph.navigate(directions)
    print(f"{num_steps=}")


def part_two(directions, nodes):
    starting_nodes = [node for node, _ in nodes if node.endswith("A")]
    ending_rule = lambda node: node.endswith("Z")
    graph = Graph(nodes, starting_nodes, ending_rule)
    num_steps = graph.navigate(directions)
    print(f"{num_steps=}")


def parse_input(data):
    directions, node_text = data.split("\n\n")
    directions = list(directions)
    nodes = []
    for line in node_text.splitlines():
        node_name, others_text = line.split(" = ")
        neighbors = tuple(others_text.strip("()").split(", "))
        nodes.append((node_name, neighbors))
    return directions, nodes


if __name__ == "__main__":
    input_filepath = "data/day08_input.txt"
    # input_filepath = "data/input_sample.txt"
    with open(input_filepath) as input_file:
        input_data = input_file.read()

    directions, nodes = parse_input(input_data)
    part_one(directions, nodes)
    part_two(directions, nodes)
