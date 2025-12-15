import math
import itertools
from copy import deepcopy

def load_input(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]
    
    # Split everything
    coords = [[int(c) for c in coord.split(',')] for coord in input]

    # Make into boxes
    boxes = [JunctionBox(x, y, z) for x, y, z in coords]
    return boxes

class JunctionBox:
    def __init__(self, x, y, z):
        self.xyz = (x, y, z)
        self.circuit = None


class Circuit:
    def __init__(self, boxes):
        self.boxes = boxes

    def add_box(self, boxes):
        self.boxes += [boxes]
        for b in boxes:
            b.circuit = self


def compute_distance(node1: JunctionBox, node2: JunctionBox):
    xyz = list(zip(node1.xyz, node2.xyz))
    squares = [(c1-c2)**2 for c1, c2 in xyz]
    return math.sqrt(sum(squares))


def part1(boxes):
    
    # Compute distances between all boxes
    distances = [[math.inf]*len(boxes)] * len(boxes)

    for i, b1 in enumerate(boxes):
        for j, b2 in enumerate(boxes):
            # Do only below diagonal of triangle
            if j >= i:
                continue
            dist = compute_distance(b1, b2)
            
            cur_dists = deepcopy(distances[i])
            cur_dists[j] = dist
            distances[i] = cur_dists

    # Get the indices of the n lowest distances
    n = 10
    n_boxes = len(boxes)
    flat_distances = list(itertools.chain(*distances))
    shortest_dists_idx = sorted(range(len(flat_distances)), key=lambda k: flat_distances[k])[:n]
    
    # Make list of boxes to connect
    to_connect = []
    for idx in shortest_dists_idx:
        b1_idx = idx // n_boxes
        b2_idx = idx % n_boxes
        to_connect.append([boxes[b1_idx], boxes[b2_idx]])

    # Make each box into a circuit
    circuits = [Circuit([b]) for b in boxes]

    # Connect circuits
    for b1, b2 in to_connect:
        pass
        # Case 1: both entirely separate and of size 1
        # merge the circuits
        # if len(b1.circuit.boxes) == 1 and len(b2.circuit.boxes) == 1:


if __name__ == "__main__":
    boxes = load_input("./test_input.txt")
    part1(boxes)