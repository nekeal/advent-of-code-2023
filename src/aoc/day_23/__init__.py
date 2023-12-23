from collections import defaultdict, deque

from aoc.base import BaseChallenge


def get_neighbours(data):
    edges = defaultdict(set)
    v_dir = {
        ">": (1, 0),
        "v": (0, 1),
    }
    for r, row in enumerate(data):
        for c, v in enumerate(row):
            if v == ".":
                for dc, dr in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    ar, ac = r + dr, c + dc
                    if (
                        0 <= ar < len(data)
                        and 0 <= ac < len(data[0])
                        and (
                            (av := data[ar][ac]) == "."
                            or (
                                av in v_dir
                                and (
                                    v_dir[av][0] != -dc or v_dir[av][1] != -dr
                                )  # not opposite direction
                            )
                        )
                    ):
                        edges[r, c].add((ar, ac, 1))
            elif v in v_dir:
                edges[r, c].add((r + v_dir[v][1], c + v_dir[v][0], 1))
    return edges


def get_neighbours2(matrix):
    """
    Used for part 2
    """
    neighbours: dict[tuple[int, int], set[tuple[int, int, int]]] = defaultdict(set)
    for r, row in enumerate(matrix):
        for c, v in enumerate(row):
            if v in ".>v":
                for dc, dr in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    ar, ac = r + dr, c + dc
                    if (
                        0 <= ar < len(matrix)
                        and 0 <= ac < len(matrix[0])
                        and matrix[ar][ac] in ".>v"
                    ):
                        neighbours[r, c].add((ar, ac, 1))
                        neighbours[ar, ac].add((r, c, 1))

    return neighbours


def reduce_neighbours(neighbors: dict[tuple[int, int], set[tuple[int, int, int]]]):
    while True:
        for node, neighbours in neighbors.items():
            if len(neighbours) == 2:
                n1, n2 = neighbours
                neighbors[n1[:2]].remove((node[0], node[1], n1[2]))
                neighbors[n2[:2]].remove((node[0], node[1], n2[2]))
                neighbors[n1[:2]].add((n2[0], n2[1], n1[2] + n2[2]))
                neighbors[n2[:2]].add((n1[0], n1[1], n1[2] + n2[2]))
                neighbors.pop(node)
                break
        else:
            break


def longest_path(start, end, neighbors):
    q = deque([(start, 0)])
    result = 0
    visited: set[tuple[int, int]] = set()
    # dfs
    while q:
        (r, c), d = q.pop()
        if d == -1:
            visited.remove((r, c))
            continue
        if (r, c) == end:
            result = max(result, d)
            continue
        if (r, c) in visited:
            continue
        visited.add((r, c))
        q.append(((r, c), -1))
        for nr, nc, dist in neighbors[r, c]:
            q.append(((nr, nc), d + dist))
    return result


class Challenge(BaseChallenge):
    def part_1(self):
        data = self.get_input_lines(part=1)
        neighbors = get_neighbours(data)
        n, m = len(data), len(data[0])
        result = longest_path((0, 1), (n - 1, m - 2), neighbors)

        return result

    def part_2(self):
        data = self.get_input_lines(part=2)
        neighbors = get_neighbours2(data)
        reduce_neighbours(neighbors)
        n, m = len(data), len(data[0])

        return longest_path((0, 1), (n - 1, m - 2), neighbors)


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
