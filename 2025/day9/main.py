import itertools
import re
from operator import itemgetter

import numpy as np
from tqdm import tqdm

def load_input(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]

    coords = [x.split(',') for x in input]
    coords = [(int(x), int(y)) for x, y in coords]
    return coords


def compute_area(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return abs(y1-y2+1)*abs(x1-x2+1)


def part1(grid_coords):
    combinations = itertools.combinations(grid_coords, 2)
    areas = [compute_area(c1, c2) for c1, c2 in combinations]
    largest_area = max(areas)
    print("Result:", largest_area)


def get_corners(cs):
    xs = [c[0] for c in cs]
    ys = [c[1] for c in cs]
    return min(xs), max(xs), min(ys), max(ys)


def print_grid(grid):
    for g in grid:
        print("".join(g))


def fill_between_spans(row: np.array, span_pairs) -> np.array:
    (start1, end1), (start2, end2) = span_pairs

    span_start, span_end = min(start1, start2), max(end1, end2)
    row[span_start:span_end] = np.ones((span_end - span_start))
    return row


def all_length_1(spans):
    return all([length_1(s) for s in spans])

def length_1(span):
    return span[1]-span[0] == 1


def is_valid_slice(slice:np.array):
    return not 0 in slice
    

def fill_grid(grid_coords):
    # Use numpy for this only because lists of lists are so inefficient
    _, xmax, _, ymax = get_corners(grid_coords)
    grid = np.zeros((ymax+1, xmax+1), dtype=np.int8)

    # Get all pairs of coordinates
    coord_pairs = list(zip(grid_coords[:-1], grid_coords[1:])) 
    coord_pairs += [[grid_coords[0], grid_coords[-1]]]

    ## Fill in shape edges
    for i, ((x1, y1), (x2, y2)) in enumerate(coord_pairs):
        print(f"Processing coord. pair {i+1} out of {len(coord_pairs)}   ", end="\r")
        # Case 1: same row
        if y1 == y2:
            xmin, xmax = min(x1, x2), max(x1, x2)
            grid[y1][xmin:xmax+1] = np.ones(xmax-xmin+1)
        
        # Case 2: same column
        if x1 == x2:
            ymin, ymax = min(y1, y2), max(y1, y2)
            grid[ymin:ymax+1, x1] = np.ones((ymax-ymin+1))
        
    print("\nFilled edges")

    ## Fill in shape fully

    # Search all ranges of Xs
    filled_grid = np.apply_along_axis(fill_row, 1, grid)
    # for row_idx in tqdm(range(len(grid))):
    #     grid[row_idx] = fill_row(grid[row_idx])

    return filled_grid


def fill_row(current):
    # Separate into sets of 0s and 1s
    groups = itertools.groupby(current)

    # Get begin and end of spans
    keys_lengths = [(k.item(), len(list(g))) for k, g in groups]
    keys, lengths = list(zip(*keys_lengths))

    first_span = 0, lengths[0]
    spans = [first_span]
    for i, length in enumerate(lengths[1:]):
        prev_end = spans[i][1]
        spans.append((prev_end, length+prev_end))   

    # Filter for the spans containing ones
    row_spans = [s for i, s in enumerate(spans) if keys[i] == 1]

    # Case 1: no ones or only ones
    if len(row_spans) <= 1:
        return current
    
    # Case 2: an even number of 'X's fully separated
    # Fill the space between each following pair
    if len(row_spans) % 2 == 0 and all_length_1(row_spans):
        span_pairs = [row_spans[i:i+2] for i in range(0, len(row_spans), 2)]

        for pair in span_pairs:
            return fill_between_spans(current, pair)

    # Case 3:
    # Two sets --> Fill between them
    if len(row_spans) == 2:
        return fill_between_spans(current, row_spans)

    # Case 4:
    # Single - long - single --> Fill from begin to end
    if len(row_spans) == 3 and all_length_1([row_spans[0], row_spans[-1]]):
        return fill_between_spans(current, 
                                            [row_spans[0], row_spans[-1]])

    # Case 5:
    # Single - single - long --> Fill only the first two
    if len(row_spans) == 3 and all_length_1(row_spans[:-1]):
        return fill_between_spans(current, row_spans[:-1])

    # Case 6:
    # Long - single - single --> Fill only the last two
    if len(row_spans) == 3 and all_length_1(row_spans[1:]):
        return fill_between_spans(current, row_spans[1:])
    
    # Catch other edge cases
    raise ValueError("Unhandled case:", current)


def is_filled_rectangle(grid: list[str], corners: list[int]):
    xmin, xmax, ymin, ymax = corners

    # Row case
    if ymin == ymax:
        return is_valid_slice(grid[ymin][xmin:xmax+1])
    
    # Column case
    if xmin == xmax:
        return is_valid_slice([row[xmin] for row in grid[ymin:ymax+1]])

    # If the rectangle contains a period, it isn't completely filled
    for y in range(ymin, ymax+1):
        slice = grid[y][xmin:xmax+1]
        if not is_valid_slice(slice):
            return False
    return True

def part2(grid_coords):
    # Fill areas within grids
    print("Filling grid..")
    grid = fill_grid(grid_coords)

    combinations = itertools.combinations(grid_coords, 2)
    valid_combinations = list(filter(
        lambda c: is_filled_rectangle(grid, get_corners(c)),
        combinations
    ))

    areas = [compute_area(c1, c2) for c1, c2 in valid_combinations]
    largest_area = max(areas)
    
    print("Result:", largest_area)

if __name__ == "__main__":
    coords = load_input("./input.txt")

    # Check if each row and column contains max 2 coords

    part2(coords)
    