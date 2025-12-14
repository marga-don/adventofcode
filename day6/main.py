import re
import itertools

def load_input_part1(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]
    
    problems, operations = input[:-1], input[-1]

    # Make into list of numbers
    problems = [re.split(' +', p) for p in problems]
    problems = [list(filter(lambda x: x != "", p)) for p in problems]
    problems = [list(map(int, p))for p in problems]

    # Split into operations
    operations = re.split(' +', operations)

    return problems, operations


def load_input_part2(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]
    
    problem_rows, operations = input[:-1], input[-1]

    # Find all ranges of digits
    match_idx = [re.finditer("\d+", p) for p in problem_rows]
    spans = [[list(m.span()) for m in match_p] for match_p in match_idx]

    # Each row should have an equal number of digit sets
    assert all([len(s) == len(spans[0]) for s in spans])

    # For each problem, save the longest span
    longest_spans = []
    for i in range(len(spans[0])):
        current_spans = [s[i] for s in spans]
        min_start = min([s[0] for s in current_spans])
        max_end = max([s[1] for s in current_spans])
        longest_spans.append((min_start, max_end))

    # Get problem columns from spans
    problem_str = []
    for begin, end in longest_spans:
        problem_str.append([list(reversed(p[begin:end])) for p in problem_rows])

    # (for readability only) read problems right to left
    problem_str = reversed(problem_str)

    # Change into ints
    problems = []
    for problem in problem_str:
        problem_numbers = []
        for i in range(len(problem[0])):
            numbers = [col[i] for col in problem]       
            problem_numbers.append(int("".join(numbers).replace(" ", "")))

        problems.append(problem_numbers)
        
    # Parse operations
    operations = list(reversed(re.split(' +', operations)))
    operations = operations[1:]

    # Check n_problems matches n_operations
    assert len(operations) == len(problems)

    return problems, operations

def part1(problems, operations):
    n_problems = len(problems[0])

    results = []
    for i in range(n_problems):
        numbers = [p[i] for p in problems]
        current_op = operations[i]

        results.append(compute_problem(numbers, current_op))

    print("Final:", sum(results))


def part2(problems, operations):
    results = []
    for i, numbers in enumerate(problems):
        current_op = operations[i]
        results.append(compute_problem(numbers, current_op))

    print("Final:", sum(results))

def compute_problem(numbers, operation):
    match operation:
        case "+":
            f = lambda x, y: x + y
        case "*":
            f = lambda x, y: x * y
        case _:
            raise ValueError("Invalid operation", operation)
        
    res = list(itertools.accumulate(numbers, f))
    return res[-1]

if __name__ == "__main__":
    problems, operations = load_input_part2("./input.txt")
    part2(problems, operations)
