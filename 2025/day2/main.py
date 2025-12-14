import math

def parse_input(str):
    return [x.split("-") for x in str.split(",")]


def is_invalid_id(number: str) -> bool:
    # Smallest pattern has length 1
    chunk_length = 1

    # Chunk length can be max half of the number
    while chunk_length <= len(number) // 2:
        # Compute number of chunks - round up to account for uneven division
        n_chunks = math.ceil(len(number) / chunk_length)

        # Divide into chunks of length chunk_length
        chunks = [number[0+(chunk_length*i):(i+1)*chunk_length] \
                  for i in range(n_chunks)]
                
        # Check if each chunk is equal
        equal = [c == chunks[0] for c in chunks[1:]]
        if all(equal):
            return True, chunks

        chunk_length += 1
    
    # If we get here, it's a valid id
    return False, None


def find_invalid_ids(bottom: str, top: str) -> list:
    invalid_ids = []

    # Make sure to include the top in the range
    for number in range(int(bottom), int(top) + 1):
        is_inval, selected_chunks = is_invalid_id(str(number))
        if is_inval:
            invalid_ids.append(number)
            # print(number, selected_chunks)
    
    return invalid_ids


if __name__ == "__main__":
    with open("./input.txt") as f:
        input = parse_input(f.read())
    
    result = []
    for bottom, top in input:
        result += find_invalid_ids(bottom, top)
    
    # print("All selected numbers:", result)
    print("Final:", sum(result))