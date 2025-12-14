
def update_state_part1(current_state, instruction):
    if len(instruction) < 1:
        return current_state, False
    direction = instruction[0]
    amount = int(instruction[1:])

    amount = -amount if direction == "L" else amount

    new_state = (current_state + amount) % 100

    # Catch error
    if new_state < 0 or new_state >= 100:
        raise ValueError(
            f"Initial state {current_state} was updated with"\
            f"instruction {instruction} and gave result {new_state}")
    
    # Return new state and bool if zero
    return new_state, new_state == 0

def update_state_part2(initial, instruction):
    if len(instruction) < 1:
        return initial, False
    direction = instruction[0]
    amount = int(instruction[1:])

    # Get if we ended at zero from existing tested method
    new_state, end_at_0 = update_state_part1(initial, instruction)
    
    # Count full rotations
    full_rotations = amount // 100

    # Check if we passed through zero on the way (and did not start there!)
    amount_within_rotation = amount % 100
    if direction == "L":
        passed_zero = int(initial - amount_within_rotation < 0 and initial > 0)
    if direction == "R":
        passed_zero = int(initial + amount_within_rotation > 100)

    # Compute result
    result = int(end_at_0) + full_rotations + passed_zero

    # # Print
    # if True:
    #     print(f"Initial {initial}, instr. {instruction}, end {new_state}")
    #     print(f"End at zero: {end_at_0}, {full_rotations} full rotations, passed zero: {passed_zero}")
    #     print(f"Result:", result)
    #     print('-----')

    # Return new state and bool if zero
    return new_state, result


def load_file(path):
    with open(path, "r") as f:
        content = f.read()
    
    instructions = content.split("\n")
    return instructions


if __name__ == "__main__":
    instructions = load_file("./input.txt")
    # instructions = instructions[:100]
    print("Total number of instructions:", len(instructions))

    current_state = 50

    results = []
    for count, i in enumerate(instructions):
        # print(count)
        current_state, countszero = update_state_part2(current_state, i)
        results.append(countszero)

    print(f"Final count: {sum(results)}")