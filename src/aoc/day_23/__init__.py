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


ans = 0


def dfs(v, d, end, neighbors, visited):
    # it occures that "visited" implementation based on list of lists is way
    # faster than set or dict based one
    global ans
    r, c = v
    if visited[r][c]:
        return
    visited[r][c] = True
    if r == end[0]:
        ans = max(ans, d)
    for nr, nc, dist in neighbors[v]:
        dfs((nr, nc), d + dist, end, neighbors, visited)
    visited[r][c] = False


class Challenge(BaseChallenge):
    def part_1(self):
        data = self.get_input_lines(part=1)
        neighbors = get_neighbours(data)
        n, m = len(data), len(data[0])
        result = longest_path((0, 1), (n - 1, m - 2), neighbors)

        return result

    def part_2(self):
        global ans
        ans = 0
        data = self.get_input_lines(part=2)
        neighbors = get_neighbours2(data)
        reduce_neighbours(neighbors)
        n, m = len(data), len(data[0])
        visited = [[False for _ in range(m)] for _ in range(n)]
        dfs((0, 1), 0, (n - 1, m - 2), neighbors, visited=visited)
        return ans
        # iterative approach is slower than recursive one
        # longest_path((0, 1), (n - 1, m - 2), neighbors)  # noqa: ERA003


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
