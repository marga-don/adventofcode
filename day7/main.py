
def load_input(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]
    
    # Replace S with beam
    input[0] = input[0].replace("S", "|")
    
    # Split everything
    input = [list(i) for i in input]
    return input


def print_manifold(man):
    print("")
    for m in man:
        print("".join(m))


def part1(full_manifold):
    split_counter = 0
    for i, line in enumerate(full_manifold[:-1]):
        for j, character in enumerate(line):
            if character == "|":
                # Beam can continue down without issue
                if full_manifold[i+1][j] == ".":
                    full_manifold[i+1][j] = "|"
            
                # Beam splits
                elif full_manifold[i+1][j] == "^":
                    split_counter += 1
                    full_manifold[i+1][j-1] = "|"
                    full_manifold[i+1][j+1] = "|"
    
    return full_manifold, split_counter
 

def part2(manifold):
    world_counter = 0
    # Base case -- bottom
    if len(manifold) == 1:
        print("Reached bottom")
        return world_counter
    
    # Otherwise, check the first row for splitters
    for j, character in enumerate(manifold[0]):
        if character == "|":
            # Beam can continue down without issue
            if manifold[1][j] == ".":
                manifold[1][j] = "|"
                print_manifold(manifold)
            
            # Beam splits
            elif manifold[1][j] == "^":
                world_counter += 1
                # Create worlds and update counter
                print("Going into left world..")
                world_counter += create_and_process_world(manifold[1:].copy(), j, left=True)
                print("Popped from left, going into right..")
                print_manifold(manifold[1:])
                world_counter += create_and_process_world(manifold[1:].copy(), j, left=False)
                return world_counter

            # In this case, we have only one beam per row per world, so we can break
            # once we've found it
            break

    # If no splits have been found, move on to next line
    print("Moving to next line")
    return part2(manifold[1:])


def create_and_process_world(manifold, idx_in_line, left):
    # Create world
    change_idx = idx_in_line -1 if left else idx_in_line + 1
    manifold[0][change_idx] = "|"
    return part2(manifold)

if __name__ == "__main__":
    manifold = load_input("./test_input.txt")

    # Debug
    manifold = manifold[:6]
    print_manifold(manifold)

    n_worlds = part2(manifold=manifold)
    # print_manifold(manifold)
    print("Result:", n_worlds)