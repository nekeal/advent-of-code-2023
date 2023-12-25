import math
import random
from pathlib import Path

from z3 import Real, Solver

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    def __init__(self, use_test_data: bool = False, data_dir: Path | None = None):
        super().__init__(use_test_data, data_dir)
        if self._use_test_data:
            self.RANGE = [7, 27]
        else:
            self.RANGE = [200000000000000, 400000000000000]

    def part_1(self):
        points = list(self.get_points(part=1))
        result = 0
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if (point := self.are_intersecting(points[i], points[j])) is True:
                    result += 1
                elif (
                    point
                    and self.RANGE[0] <= point[0] <= self.RANGE[1]
                    and self.RANGE[0] <= point[1] <= self.RANGE[1]
                ):
                    result += 1
        return result

    def part_2(self):
        points = list(self.get_points(part=2))
        # variables to be solved (related to the rock)
        x = Real("x")
        y = Real("y")
        z = Real("z")
        vx = Real("vx")
        vy = Real("vy")
        vz = Real("vz")
        s = Solver()

        # it's enough to check 3 hailstones
        for idx, shard in enumerate(random.sample(points, 3)):
            x0, y0, z0, xv, yv, zv = shard
            t = Real(f"t_{idx}")  # each collision occurs at a different time

            # collision for each axis
            s.add(x + vx * t == x0 + xv * t)
            s.add(y + vy * t == y0 + yv * t)
            s.add(z + vz * t == z0 + zv * t)

        s.check()
        m = s.model()
        return m[x].as_long() + m[y].as_long() + m[z].as_long()

    def get_points(self, part):
        input_lines = self.get_input_lines(part=part)
        for line in input_lines:
            x, y, z, vx, vy, vz = (int(x.strip(",")) for x in line.split() if x != "@")
            yield x, y, z, vx, vy, vz

    @staticmethod
    def are_intersecting(h1, h2):
        a1 = h1[4] / h1[3]
        b1 = h1[1] - a1 * h1[0]
        a2 = h2[4] / h2[3]
        b2 = h2[1] - a2 * h2[0]
        if math.isclose(a1, a2):
            if math.isclose(b1, b2):
                return True
            return False
        cx = (b2 - b1) / (a1 - a2)
        cy = cx * a1 + b1
        if (cx > h1[0]) == (h1[3] > 0) and (cx > h2[0]) == (h2[3] > 0):
            return cx, cy
        return False


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
