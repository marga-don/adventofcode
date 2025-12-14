
def load_input(path, debug):
    with open(path) as f:
        input = f.readlines()

    # Remove newlines
    input = [i.replace("\n", "") for i in input]

    # Find split between fresh and available
    split = input.index("")

    fresh, available = input[:split], input[split+1:]

    # Debug
    if debug:
        print("Using debug!")
        fresh = fresh[:10]
        available = available[:100]

    # Convert available to ints
    available = [int(x) for x in available]

    return fresh, available

def build_fresh_list(fresh_list):
    result = []
    for l in fresh_list:
        begin, end = [int(x) for x in l.split("-")]
        result.append((begin, end))
    return result

def is_fresh(ingredient, fresh_list):
    for begin, end in fresh_list:
        if begin <= ingredient and ingredient <= end:
            return True
    return False

def part1(fresh, available):
    fresh_list = build_fresh_list(fresh)
    print("Built fresh set")

    result = []
    for ingredient in available:
        if is_fresh(ingredient, fresh_list):
            result.append(ingredient)

    print(len(result))

from dataclasses import dataclass

@dataclass
class FreshRange:
    begin: int
    end: int
    next: None

    def __str__(self):
        return f"[{self.begin}-{self.end}]"


class FreshCollection:
    def __init__(self, head: FreshRange):
        self.head = head

    def add_range(self, new: FreshRange):        
        # Find start range (where start.begin < new.begin < (start.next).begin)
        # Find end range (where (before end).end < new.end < end.end)
        start = self.find_start(new)
        end = self.find_end(new)

        # Case where start == end (add new as first or last, or overlap)
        if start == end:
            # Case already covered by existing range, no action
            if start.begin <= new.begin and start.end >= new.end:
                return
            
            # Case extend at the end
            if start.begin <= new.begin and start.end < new.end and new.begin <= start.end:
                start.end = new.end
                return

            # Case entirely new end
            if start.begin <= new.begin and start.end < new.end:
                start.next = new
                return
            
            # Case extend at beginning
            if start.begin > new.begin and start.end >= new.end and new.end >= start.begin:
                start.begin = new.begin
                return
            
            # Case entirely new beginning
            if start.begin > new.begin and start.end >= new.end:
                self.head = new
                new.next = start
                return

            raise ValueError("Shouldn't get here!")
                
        # Case overlap with both start and end
        #   Make start range go from start.begin-end.end
        if new.begin <= start.end and new.end >= end.begin:
            start.end = end.end
            start.next = end.next
            return

        # Case overlap with only start
        #   Extend start
        if new.begin <= start.end and new.begin < end.begin:
            start.end = new.end
            return

        # Case overlap with only end
        #   Extend end
        if new.begin > start.end and new.end >= end.begin:
            end.begin = new.begin
            return

        # Case no overlap
        #   Place between start and end
        if new.begin > start.end and new.end < end.begin:
            start.next = new
            new.next = end
            return

        # Catch errors
        raise ValueError("Shouldn't get here!")

    def find_start(self, new):
        current = self.head
        # Check if head is start
        if new.begin <= current.begin:
            return current

        while current.next is not None:
            if current.begin <= new.begin and new.begin <= current.next.begin:
                return current
            current = current.next
        return current
    
    def find_end(self, new):
        current = self.head
        # Check if head is end
        if new.end <= current.end:
            return current

        while current.next is not None:
            if current.end <= new.end and new.end <= current.next.end:
                return current.next
            current = current.next
        return current

    def show_ranges(self):
        to_print = ""
        current = self.head
        while current.next is not None:
            to_print += current.__str__()
            current = current.next
        to_print += current.__str__()
        return to_print
    
    def count_numbers(self):
        total = 0
        current = self.head
        while current.next is not None:
            total += (current.end - current.begin) + 1
            current = current.next
        total += (current.end - current.begin) + 1
        return total

def part2(fresh):
    start = fresh[0]
    result = FreshCollection(FreshRange(start[0], start[1], next=None))
    
    for begin, end in fresh[1:]:
        # print(result.show_ranges(), f"Adding: {begin}-{end}")
        result.add_range(FreshRange(begin, end, next=None))

    print("Result:")
    print(result.show_ranges())
    print(result.count_numbers())

if __name__ == "__main__":
    fresh, _ = load_input("./input.txt", debug=False)
    fresh = build_fresh_list(fresh)

    part2(fresh)



    