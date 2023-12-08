import itertools
from math import lcm

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    def part_1(self):
        input_lines = self.get_input_lines(part=1)
        instructions: str = input_lines[0]
        starting_node: str = "AAA"
        node_map = self.get_node_map(input_lines[2:])

        for i, node in enumerate(
            self.iterate_nodes(instructions, starting_node, node_map)
        ):
            if node == "ZZZ":
                print(i)
                return i

    def part_2(self):
        input_lines = self.get_input_lines(part=2)
        instructions: str = input_lines[0]
        node_map = self.get_node_map(input_lines[2:])
        starting_nodes: list[str] = [node for node in node_map if node.endswith("A")][:]
        results = []
        for starting_node in starting_nodes:
            for i, node in enumerate(
                self.iterate_nodes(instructions, starting_node, node_map)
            ):
                if node.endswith("Z"):
                    results.append(i)
                    break
        return lcm(*results)

    @staticmethod
    def get_node_map(lines: list[str]) -> dict[str, tuple[str, str]]:
        result: dict[str, tuple[str, str]] = {}
        for line in lines:
            node, unparsed_choices = map(  # noqa: C417
                lambda s: s.strip().strip("()"), line.split("=")
            )
            result[node] = tuple(  # type: ignore
                map(lambda s: str(s.strip()), unparsed_choices.split(",", maxsplit=1))  # noqa: C417
            )
        return result

    @staticmethod
    def iterate_nodes(instructions, starting_node, node_map):
        instruction_to_number = {
            "L": 0,
            "R": 1,
        }
        current_node = starting_node
        yield current_node
        for instruction in itertools.cycle(instructions):
            current_node = node_map[current_node][instruction_to_number[instruction]]
            yield current_node


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
