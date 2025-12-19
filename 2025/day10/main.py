from dataclasses import dataclass
from itertools import chain
from collections import deque

def load_input(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]

    machines = []
    for i in input:
        # Find end of goal and parse
        goal_state = i[1:i.index("]")]
        goal_state = [x == "#" for x in goal_state]
        
        # Find buttons and parse
        buttons = i[i.index("("):i.index("{")].replace("(", "").replace(")", "")
        buttons = [[int(x) for x in b.split(",")] for b in buttons.split(" ")[:-1]]
        
        # Find joltages and parse
        joltage_reqs = [int(x) for x in i[i.index("{")+1:-1].split(",")]
        
        # Create machine
        machines.append([goal_state, buttons, joltage_reqs])
    
    return machines

@dataclass
class State:
    state: list[bool]
    operations: list[list[int]]
    child_states: list["State"]

    def apply_button(self, button):
        # Invert state if its index is in the button, else keep the same
        return [not s if i in button else s for i, s in enumerate(self.state)]

    def return_all_children(self):
        rec_children = [x.return_all_children() for x in self.child_states]
        return [self] + list(chain(*rec_children))

class StateCollection:
    def __init__(self, init_state, goal_state):
        self.init_state = State(init_state, [], [])
        self.goal_state = goal_state

    @property
    def all_states(self):
        return self.init_state.return_all_children()
    
    def get_leaves(self):
        states = self.all_states
        max_ops = max([len(x.operations) for x in states])
        return list(filter(lambda x: len(x.operations) == max_ops, states))
    
    def add_state(self, old_state: State, button):
        new = old_state.apply_button(button)

        # If this is the goal, stop
        if new == self.goal_state:
            return len(old_state.operations) + 1
        
        # Otherwise, add state if we haven't seen it before
        if new not in [x.state for x in self.all_states]:
            old_state.child_states.append(
                State(new, operations=old_state.operations + [button], 
                      child_states=[]))


@dataclass
class JoltageState:
    state: list[int]
    operations: list[list[int]]

    def apply_button(self, button):
        new_state = [s+1 if i in button else s for i, s in enumerate(self.state)]
        return JoltageState(new_state, self.operations + [button])


@dataclass
class JoltageSearch:
    to_visit: deque[JoltageState]
    goal: list[int]
    buttons: list[list[int]]
    
    def bfs(self):
        while len(self.to_visit) > 0:
            # Pop first node
            current = self.to_visit.popleft()

            # Check if reached goal
            if current.state == self.goal:
                return len(current.operations)
            
            # Check if invalid, then move on to next
            if any([current.state[i] > self.goal[i] for i in range(len(self.goal))]):
                continue

            # Apply each button to the state
            # Prepend to to_visit
            new_states = [current.apply_button(b) for b in self.buttons]
            for s in new_states:
                self.to_visit.append(s)


def bfs_pt2(goal, buttons):
    init_state = JoltageState([0]*len(goal), [])
    init_queue = deque()
    init_queue.appendleft(init_state)
    search = JoltageSearch(init_queue, goal, buttons)
    res = search.bfs()
    print("Result:", res)

def breadth_first_search(goal, buttons):
    init_state = [False]*len(goal)

    # Keep track using pairs of (state, operations)
    collection = StateCollection(init_state, goal)

    while True:
        # Apply each possible button to each leaf in the tree
        for leaf in collection.get_leaves():
            for b in buttons:
                res = collection.add_state(leaf, b)

                if res is not None:
                    return res


def part1(machines):
    shortest = [breadth_first_search(goal, buttons) for goal, buttons, _ in machines]
    print("Result:", sum(shortest))


def part2(machines):
    shortest = [bfs_pt2(goal_joltages, buttons) for _, buttons, goal_joltages in machines]
    print("Result", sum(shortest))
    
if __name__ == "__main__":
    machines = load_input("./test_input.txt")

    part2(machines)
