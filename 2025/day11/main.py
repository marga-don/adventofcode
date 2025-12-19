from dataclasses import dataclass
from collections import deque

def load_input(path):
    with open(path) as f:
        input = f.readlines()
        input = [i.replace("\n", "") for i in input]

    devices = [i.split(":")[0] for i in input]
    connections = [i.split(": ")[1].split(" ") for i in input]
    dev_conn = {d: c for d, c in zip(devices, connections)}
    return dev_conn


@dataclass
class Device:
    name: str
    outputs: list["Device"]

    def __str__(self):
        if len(self.outputs) == 0:
            return self.name
        
        out = self.name + ": "
        for o in self.outputs:
            out += o.name + ", "
        return out[:-2]


@dataclass
class Path:
    visited_last: Device
    len_path: int
    visited_dac: bool
    visited_fft: bool

    def is_valid(self):
        return self.visited_dac and self.visited_fft


class FindPath:
    def __init__(self, start_node: Device, part2=False):
        self.to_visit = deque()
        self.part2 = part2

        if part2:
            self.to_visit.append(Path(
                visited_last=start_node,
                len_path=1,
                visited_dac=start_node.name == "dac",
                visited_fft=start_node.name == "fft",
            ))
        else:
            self.to_visit.append(start_node)

        self.n_paths = 0

    def dfs(self):
        if self.part2:
            return self.dfs2()
        return self.dfs1()

    def dfs1(self):
        while len(self.to_visit) > 0:
            current = self.to_visit.popleft()
            # print("Popped", current.name, "queue", [x.name for x in list(self.to_visit)])

            # Found valid path, increment counter and continue
            if current.name == "out":
                self.n_paths += 1
                continue

            # Add connections to queue
            for c in current.outputs:
                self.to_visit.appendleft(c)

        return self.n_paths
    
    def dfs2(self):
        while len(self.to_visit) > 0:
            current = self.to_visit.popleft()
            print(f"Current path length: {current.len_path}    ", end="\r")

            if current.len_path > 30:
                print()

            # If path ends at out and its a valid path, increment counter
            if current.visited_last.name == "out" and current.is_valid():
                self.n_paths += 1
                continue

            # Add new paths to queue with new connections
            dac, fft = current.visited_dac, current.visited_fft
            for c in current.visited_last.outputs:
                self.to_visit.appendleft(
                    Path(c,
                         current.len_path + 1,
                         dac or c.name == "dac", 
                         fft or c.name == "fft")
                )

        return self.n_paths


def create_and_connect(dev_conn):
    # Connect and create devices
    devices = [Device(d, []) for d in dev_conn.keys()] + [Device("out", [])]
    for d in devices[:-1]:
        connections = list(filter(lambda x: x.name in dev_conn[d.name], devices))
        d.outputs = connections
    
    print(f"Created and connected {len(devices)} devices")
    return devices

def part1(dev_conn):
    devices = create_and_connect(dev_conn)
    
    # Find start node
    you = list(filter(lambda x: x.name == "you", devices))
    assert len(you) == 1

    # Do dfs
    find = FindPath(you[0])
    res = find.dfs()
    print("Result:", res)


def part2(dev_conn):
    devices = create_and_connect(dev_conn)
    
    # Find start node
    svr = list(filter(lambda x: x.name == "svr", devices))
    assert len(svr) == 1

    # Do dfs
    find = FindPath(svr[0], part2=True)
    res = find.dfs()
    print("Result:", res)


                
if __name__ == "__main__":
    devices_connections = load_input("./input.txt")

    part2(devices_connections)
