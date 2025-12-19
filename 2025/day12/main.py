import numpy as np
from dataclasses import dataclass

def load_input(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]

    # Separate the shape descriptions from grid descriptions
    separators = [i for i in range(len(input)) if input[i] == ""]
    shape_separators = separators[:-1]

    # Parse each shape
    shapes = {}
    for i, sep in enumerate(shape_separators):
        prev = -1 if i ==0 else shape_separators[i-1]

        shape_idx = input[prev+1].split(":")[0]
        shape = input[prev+2:sep]
        shapes[shape_idx] = shape

    # Parse grids
    grids = []
    for l in input[separators[-1]+1:]:
        w, h = [int(x) for x in l.split(":")[0].split("x")]
        
        

@dataclass
class Grid:
    height: int
    width: int
    requirements: dict[int, int]


    

if __name__ == "__main__":
    input = load_input("./test_input.txt")