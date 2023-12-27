from collections import namedtuple
from heapq import heappop, heappush

from aoc.base import BaseChallenge

node = tuple[int, int]

path_node = namedtuple("path_node", ["heat", "ord", "pos", "direction"])


def find_path(graph: list[list[int]], start: node, end: node, min_step, max_step):
    heap = [path_node(0, 0, start, 1), path_node(0, 0, start, 1j)]
    visited = set()
    counter = 0  # used as a tiebreaker in a priority queue
    while heap:
        heat, _, current, direction = heappop(heap)
        if current == end:
            return heat
        if (current, direction) in visited:
            continue
        visited.add((current, direction))
        for turn in (1j * direction, -1j * direction):
            increase_heat_by = 0
            for step in range(1, max_step + 1):
                next_pos = (
                    int(current[0] + turn.real * step),
                    int(current[1] + turn.imag * step),
                )
                if next_pos_in_graph := (
                    0 <= next_pos[0] < len(graph[0]) and 0 <= next_pos[1] < len(graph)
                ):
                    increase_heat_by += graph[next_pos[0]][next_pos[1]]
                if next_pos_in_graph and min_step <= step <= max_step:
                    heappush(
                        heap,
                        path_node(
                            heat + increase_heat_by,
                            (counter := counter + 1),
                            next_pos,
                            turn,
                        ),
                    )


class Challenge(BaseChallenge):
    def part_1(self):
        input_lines, m, n = self.get_data(part=1)
        return find_path(input_lines, (0, 0), (n - 1, m - 1), min_step=1, max_step=3)

    def part_2(self):
        input_lines, n, m = self.get_data(part=2)
        return find_path(input_lines, (0, 0), (n - 1, m - 1), min_step=4, max_step=10)

    def get_data(self, part):
        input_lines = [
            [int(x) for x in list(line)] for line in self.get_input_lines(part=part)
        ]
        n, m = len(input_lines), len(input_lines[0])
        return input_lines, m, n


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
