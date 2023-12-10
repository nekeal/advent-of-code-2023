from collections import deque
from functools import cached_property

from aoc.base import BaseChallenge
from aoc.data_structures import Matrix

pipe_to_neighbors: dict[str, list[tuple[int, int]]] = {
    "|": [(0, -1), (0, 1)],
    "-": [(-1, 0), (1, 0)],
    "L": [(1, 0), (0, -1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(-1, 0), (0, 1)],
    "F": [(1, 0), (0, 1)],
    ".": [],
    "S": [],
}


class PipeMatrix(Matrix):
    @cached_property
    def starting_point(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x] == "S":
                    return x, y

    def replace_starting_point_with_pipe(self):
        neighbours = list(self.get_neighbors(*self.starting_point))
        vectors_to_neighbors = [
            (n[0] - self.starting_point[0], n[1] - self.starting_point[1])
            for n in neighbours
        ]
        for pipe, vectors in pipe_to_neighbors.items():
            if set(vectors) == set(vectors_to_neighbors):
                self.matrix[self.starting_point[1]].replace("S", pipe)
                return
        raise Exception("Could not find pipe for starting point")

    def get_direct_neighbors(self, x, y):
        """
        Returns neighbors that this pipe points to.
        :param x: x coordinate of the pipe
        :param y: y coordinate of the pipe
        :return: generator of neighbors that this pipe points to
        """
        for direction in pipe_to_neighbors[self.matrix[y][x]]:
            yield x + direction[0], y + direction[1]

    def get_neighbors(self, x, y):
        """
        Returns neighbors pipe that point to this pipe.
        :param x: x coordinate of the pipe
        :param y: y coordinate of the pipe
        :return: generator of neighbors that point to this pipe
        """
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for direction in directions:
            potential_neighbor = x + direction[0], y + direction[1]
            if (
                potential_neighbor[0] < 0
                or potential_neighbor[1] < 0
                or potential_neighbor[0] >= self.width
                or potential_neighbor[1] >= self.height
            ):
                continue
            if (x, y) in self.get_direct_neighbors(*potential_neighbor):
                yield x + direction[0], y + direction[1]

    def bfs(self):
        start = self.starting_point
        queue: deque[tuple[int, int]] = deque()
        distance = {start: 0}
        for neighbor in self.get_neighbors(*start):
            queue.append(neighbor)
            distance[neighbor] = 1
        while queue:
            x, y = queue.popleft()
            for neighbor in self.get_direct_neighbors(x, y):
                if neighbor not in distance:
                    queue.append(neighbor)
                    distance[neighbor] = distance[(x, y)] + 1

        return distance


class Challenge(BaseChallenge):
    def part_1(self):
        input_lines = self.get_input_lines(part=1)
        matrix = PipeMatrix(input_lines)
        distances = matrix.bfs()
        return max(distances.values())

    def part_2(self):
        input_lines = self.get_input_lines(part=2)
        matrix = PipeMatrix(input_lines)
        matrix.replace_starting_point_with_pipe()
        distances = matrix.bfs()
        inside_count = self.count_enclosed_points(distances, matrix)
        return inside_count

    @staticmethod
    def count_enclosed_points(distances, matrix):
        inside_count = 0
        for y, line in enumerate(matrix.matrix):
            for x, _ in enumerate(line):
                if (x, y) in distances:  # skip borders
                    continue
                crossed_count = 0

                ray_position = (x, y)
                while (
                    ray_position[0] < matrix.width and ray_position[1] < matrix.height
                ):
                    c2 = matrix.matrix[ray_position[1]][ray_position[0]]
                    if ray_position in distances and c2 not in [
                        "L",
                        "7",
                    ]:
                        crossed_count += 1
                    ray_position = ray_position[0] + 1, ray_position[1] + 1
                inside_count += crossed_count % 2
        return inside_count


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
