from collections import defaultdict, deque
from functools import partial
from typing import Optional
from piper import p, pipe, Map, Filter
from Vec import Vec
from Term import Term
from typing import Optional, Union, Deque
import tty, sys

class Node:
    def __init__(self, label):
        self.outputs = set()
        self.inputs = set()
        self.label : str = label
        self.rank = None
        self.pos = Vec(0,0) # position on terminal
        self.coords = Vec(0,0) # coords in grid
        self.dims = Vec(len(label),1) + (2,2) # size in grid

    def print(self, term: Term, pos: Vec):
        term.write_here(self.pos+Vec(2,2), self.label)

class Conduit:
    def __init__(self):
        self.dims = Vec(1,1)

class Graph:
    def __init__(self):
        self.nodes : dict[str,Node] = {}
        self.grid = {}

    def __getitem__(self, key: str) -> Node:
        if key not in self.nodes:
            self.nodes[key] = Node(key)
        return self.nodes[key]

    def add_edge(self, label_a, label_b):
        graph[label_a].outputs.add(label_b)
        graph[label_b].inputs.add(label_a)

    def populate_from_file(self, filename):
        with open(filename, "r") as file:
            for line in file.readlines():
                line_tokens = list(line.strip().split())
                for i, token in enumerate(line_tokens):
                    if token == "->":
                        label_a = line_tokens[i-1]
                        label_b = line_tokens[i+1]
                        self.add_edge(label_a, label_b)
        self.set_node_dims()
        self.rank()
        self.populate_grid()

    def find_longest_path(self, cc_repr=None):
        if cc_repr == None:
            cc_sources = self.nodes.items()
        else:
            def find_sources(node: str,
                    sources: set, visited: set):
                if len(self[node].inputs) == 0:
                    sources.add(node)
                visited.add(node)
                for i in list(self[node].outputs) + list(self[node].inputs):
                    if i not in visited:
                        visited.add(i)
                        find_sources(i, sources, visited)
                return sources
            cc_sources = ((i, self[i]) for i in find_sources(cc_repr, set(), set()))
        return pipe(
            cc_sources,
            Filter(lambda x: x[1].inputs |p| len == 0),
            Map(lambda x: self.find_furthest_node(x[0])),
            max
        )

    def find_furthest_node(self, source):
        queue : Deque[tuple[int,str]] = deque([(0, source)])
        visited = set([source])
        farthest = (0, source)
        parent = {}
        while(queue):
            dist, x = queue.popleft()
            farthest = max(farthest, (dist, x))
            for i in self.nodes[x].outputs:
                if i not in visited:
                    visited.add(i)
                    parent[i] = x
                    queue.append((dist + 1, i))
        x = farthest[1]
        path = [x]
        while x != source:
            x = parent[x]
            path.append(x)
        return farthest + (path |p| reversed |p| list,)

    def set_node_dims(self):
        for node in self.nodes.values():
            node.dims.y = max(node.dims.y, len(node.inputs) + 2, len(node.outputs) + 2)
    def find_unranked_node(self):
        for k,v in self.nodes.items():
            if v.rank == None:
                return k
        return None

    def rank(self):

        while True:
            x = self.find_unranked_node()
            if x == None:
                break

            path = self.find_longest_path(cc_repr=x)[2]

            queue = deque()
            for i , x in (path |p| enumerate):
                self.nodes[x].rank = i
                queue.append(x)
            
            while(queue):
                x = queue.popleft()
                for i in self.nodes[x].outputs:
                    if self.nodes[i].rank == None:
                        self.nodes[i].rank = self.nodes[x].rank + 1
                        queue.append(i)
                for i in self.nodes[x].inputs:
                    if not self.nodes[i].rank:
                        self.nodes[i].rank = self.nodes[x].rank - 1
                        queue.append(i)

    def render(self):
        ranks = defaultdict(list)
        i = 0
        term.clear()
        for y in range(self.grid_dims.y):
            j = 0
            for x in range(self.grid_dims.x):
                label = ""
                if isinstance(self.grid[x,y], Node):
                    label = self.grid[x,y].label
                    term.draw_rectangle((j,i),(self.grid[x,y].dims), label=label)
                else:
                    pass
                    # term.draw_rectangle((j,i),(self.grid[x,y].dims))
                j += self.grid_col_widths[x]
            i += self.grid_row_heights[y]

        print("")

        for i in self.nodes:
            ranks[self.nodes[i].rank].append(i)
        for i, j in list(ranks.items()) |p| sorted:
            print(j)

    def populate_grid(self):
        ranks = defaultdict(list)
        for i in self.nodes:
            ranks[self.nodes[i].rank].append(i)
        for i, rank in pipe(
                ranks.items(),
                sorted,
                partial(map,lambda x: x[1]),
                enumerate):
            for j, node in rank |p| enumerate:
                self.grid[(i*2+1, j*2+1)] = self.nodes[node]
                self.grid[(i*2+1, j*2+1)].coords = Vec(i*2+1, j*2+1)

        self.grid_dims = Vec(pipe(
                self.grid.keys(),
                Map(lambda x: x[0]),
                max) + 2,
            pipe(
                self.grid.keys(),
                Map(lambda x: x[1]),
                max
            ) + 2
        )

        for i in Vec.dim_range((0,0),self.grid_dims):
            if i not in self.grid:
                self.grid[i] = Conduit()
                self.grid[i].coords = i

        self.grid_col_widths = {}
        self.grid_row_heights = {}

        for x in range(self.grid_dims.x):
            self.grid_col_widths[x] = pipe(
                range(self.grid_dims.y),
                Map(lambda y: self.grid[x,y].dims.x),
                max
            )
        for y in range(self.grid_dims.y):
            self.grid_row_heights[y] = pipe(
                range(self.grid_dims.x),
                Map(lambda x: self.grid[x,y].dims.y),
                max
            )

        for item in self.grid.values():
            item.dims.x = self.grid_col_widths[item.coords.x]
            item.dims.y = self.grid_row_heights[item.coords.y]

term = Term()
graph = Graph()
graph.populate_from_file("test_graph.graph")
graph.render()
