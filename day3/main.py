import itertools

def parse_input(path):
    with open(path) as f:
        input = f.readlines()
    return [x.replace('\n', '') for x in input]

def find_largest_digit(lst):
    # Find largest number in list and its index
    largest_digit = max(lst)
    largest_digit_idx = lst.index(largest_digit)

    return largest_digit, largest_digit_idx

def find_max_joltage(bank):
    # Convert to list of ints
    bank_ints = [int(x) for x in bank]

    chosen_digits = []
    for idx in range(11, -1, -1):
        sublist = bank_ints[:-idx] if idx > 0 else bank_ints
        digit, digit_idx = find_largest_digit(sublist)
        chosen_digits.append(str(digit))
        bank_ints = bank_ints[digit_idx+1:]
    
    chosen_digits = int(''.join(chosen_digits))
    return chosen_digits

if __name__ == "__main__":
    banks = parse_input("./input.txt")
    
    max_joltages = [find_max_joltage(b) for b in banks]
    # print(max_joltages)
    print("Result:", sum(max_joltages))