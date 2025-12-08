import heapq
import itertools
import math
from dataclasses import dataclass, field
from typing import List, Set

# filename, total_connections = "sample.txt", 10
filename, total_connections = "data.txt", 1000


DEBUG = False


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        # euclidean distance
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"


class JunctionBox(Vector):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.circuit = Circuit(self)

    def connect_circuits(self, other):
        # add junction boxes of other circuit to this circuit
        self.circuit.junction_boxes.update(other.circuit.junction_boxes)

        # update each junction box in the circuit to indicate it is connected to the
        # new merged circuit
        for j_box in self.circuit.junction_boxes:
            j_box.circuit = self.circuit


class Circuit:
    def __init__(self, junction_box):
        self.junction_boxes = {junction_box}


@dataclass(order=True)
class Connection:
    distance: float
    junctions: Set = field(compare=False)

    def __repr__(self):
        return f"({self.distance:.2f}, {self.junctions})"


if __name__ == "__main__":
    total_part1 = 0
    total_part2 = 0

    with open(filename, "r") as f:
        lines = f.read()

    junction_boxes: List[JunctionBox] = []
    for line in lines.split("\n"):
        junction_boxes.append(JunctionBox(*map(float, line.split(","))))

    # calculate distance of all pairwise permutations of junction boxes as a
    # connection, order does not matter in a connection, ignore checks against self
    junction_pairs = itertools.combinations(junction_boxes, 2)
    connections = []
    for j1, j2 in junction_pairs:
        distance = j1.distance(j2)
        connections.append(Connection(distance, {j1, j2}))

    # use min-heap to prioritize connections by shortest distance
    heapq.heapify(connections)

    # make the necessary connections for part 1
    for _ in range(total_connections):
        connection = heapq.heappop(connections)
        j1, j2 = connection.junctions
        j1.connect_circuits(j2)

    circuits = set(j.circuit for j in junction_boxes)
    circuits_by_length = sorted(
        circuits, key=lambda x: len(x.junction_boxes), reverse=True
    )
    total_part1 = math.prod(len(c.junction_boxes) for c in circuits_by_length[:3])

    # part 2 - use part 1 outcome and continue making connections until no junction
    # box is on an isolated circuit
    while connections:
        connection = heapq.heappop(connections)
        j1, j2 = connection.junctions
        j1.connect_circuits(j2)
        smallest_circuit = min(
            len(j_box.circuit.junction_boxes) for j_box in junction_boxes
        )
        if smallest_circuit != 1:
            # all junction boxes have been connected to at least one other
            total_part2 += int(j1.x * j2.x)
            break

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")
