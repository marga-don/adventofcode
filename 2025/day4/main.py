# Using zero-based indexing throughout!
from copy import deepcopy

def parse_grid(file):
    with open(file) as f:
        gridlines = f.readlines()

    # Remove newlines and make list
    gridlines = [list(g.replace("\n", "")) for g in gridlines]
    
    return gridlines

def print_grid(g):
    for r in g:
        print("".join(r))

def get_around(grid, row, col):
    if row >= len(grid) or col >= len(grid[0]) or row < 0 or col < 0:
        raise ValueError(f"Queried position {row}, {col} which is out of bounds")

    neighbors = []
    for r in [row-1, row, row+1]:
        # Check only if in bounds
        if r < 0 or r >= len(grid):
            continue
        
        for c in [col-1, col, col+1]:
            # Check only if in bounds
            if c < 0 or c >= len(grid[0]):
                continue

            # Don't consider yourself
            if r == row and c == col:
                continue

            # Otherwise, get value at index
            neighbors.append(grid[r][c])

    return neighbors


def main(original_grid):
    grid_result = deepcopy(original_grid)
    result_counter = 0

    for r in range(len(original_grid)):
        for c in range(len(original_grid[0])):
            # Only count if current index is a paper roll
            if original_grid[r][c] == "@":
                neighbors = get_around(original_grid, r, c)
                n_rolls = sum([n == "@" for n in neighbors])

                # print(r, c, neighbors, n_rolls)

                if n_rolls < 4:
                    grid_result[r][c] = "x"
                    result_counter += 1
    
    print(f"Removing {result_counter} rolls of paper")
    return grid_result, result_counter

def remove_x_from_grid(g):
    for i in range(len(g)):
        g[i] = [x.replace("x", ".") for x in g[i]]
    return g

if __name__ == "__main__":
    grid = parse_grid("./input.txt")

    can_be_removed, total_removed = 1, 0
    while can_be_removed > 0:
        grid, can_be_removed = main(remove_x_from_grid(grid))
        total_removed += can_be_removed
        # print_grid(remove_x_from_grid(grid))
    
    print(total_removed)
    