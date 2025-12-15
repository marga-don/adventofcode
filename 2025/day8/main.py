import math
import itertools
from copy import deepcopy

def load_input(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]
    
    # Split everything
    coords = [[int(c) for c in coord.split(',')] for coord in input]

    # Make into boxes and circuits
    boxes = [JunctionBox(x, y, z) for x, y, z in coords]
    for b in boxes:
        b.circuit = Circuit([b])

    return boxes

class JunctionBox:
    def __init__(self, x, y, z):
        self.xyz = (x, y, z)
        self.circuit = None


class Circuit:
    def __init__(self, boxes):
        self.boxes = boxes

    def add_box(self, boxes: list[JunctionBox]):
        self.boxes += boxes
        for b in boxes:
            b.circuit = self

    
    def __str__(self):
        return f"{[b.xyz for b in self.boxes]}"


def compute_distance(node1: JunctionBox, node2: JunctionBox):
    xyz = list(zip(node1.xyz, node2.xyz))
    squares = [(c1-c2)**2 for c1, c2 in xyz]
    return math.sqrt(sum(squares))


def compute_distances(combined_boxes):
    # Compute distances between all boxes
    distances = list([compute_distance(b1, b2) for b1, b2 in combined_boxes])
    return distances


def get_n_shortest_distances(distances, n):
    # Get the indices of the n lowest distances
    n = 1000
    shortest_dists_idx = sorted(range(len(distances)), key=lambda k: distances[k])[:n]
    return shortest_dists_idx


def connect_boxes(b1, b2):
    # print(f"Connecting {b1.xyz} and {b2.xyz}\nCircuits before:", b1.circuit, b2.circuit)

    # Case 1: already connected, no action
    if b1.circuit == b2.circuit:
        # print("Already connected, no action\n----")
        return

    # Case 2: add boxes
    b1.circuit.add_box(b2.circuit.boxes)

    # print("Circuits after:", b1.circuit, "\n----")

def part1(boxes, n):
    combinations = list(itertools.combinations(boxes, 2))
    distances = compute_distances(combinations)
    shortest_dists_idx = get_n_shortest_distances(distances, n=n)

    # Connect boxes
    to_connect = [combinations[i] for i in shortest_dists_idx]
    for b1, b2 in to_connect:
        connect_boxes(b1, b2)
    
    # Find which circuits are the largest
    circuits = []
    for b in boxes:
        if b.circuit not in circuits:
            circuits.append(b.circuit)

    # Sort on length, take the size of largest three and multiply
    circuit_lengths = [len(c.boxes) for c in circuits]
    chosen_circuits = sorted(circuit_lengths, reverse=True)[:3]
    print(f"Result:", chosen_circuits[0]*chosen_circuits[1]*chosen_circuits[2])


def part2(boxes):
    combinations = list(itertools.combinations(boxes, 2))
    distances = compute_distances(combinations)

    sorted_distances_idx = sorted(range(len(distances)), key=lambda k: distances[k])
    for idx in sorted_distances_idx:
        b1, b2 = combinations[idx]
        connect_boxes(b1, b2)

        # Check if all one circuit --> every box has the same circuit
        if all([b.circuit == boxes[0].circuit for b in boxes]):
            break
    
    print("Result:", b1.xyz[0]*b2.xyz[0])


if __name__ == "__main__":
    boxes = load_input("./input.txt")
    part2(boxes)