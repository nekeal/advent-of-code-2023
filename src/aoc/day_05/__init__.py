from pprint import pprint
from typing import Generator

from aoc.base import BaseChallenge


class Range:
    def __init__(self, begin: int, end: int):
        self.begin = begin
        self.end = end

    def shift_by(self, amount: int):
        self.begin += amount
        self.end += amount
        return self

    def overlaps(self, other: "Range"):
        return self.begin <= other.end and other.begin <= self.end

    def intersection(self, other: "Range"):
        """
        Return the intersection of two ranges.
        If the ranges do not overlap, return None.
        """
        if not self.overlaps(other):
            return None
        return Range(max(self.begin, other.begin), min(self.end, other.end))

    def diff(self, other: "Range"):
        """
        Return a list of ranges that are the result of subtracting other from self.
        If other does not overlap with self, return self.
        If other is a subset of self, return two ranges.
        If other overlaps with self, but is not a subset, return one range.
        """
        if not self.overlaps(other):
            return [self]
        if other.begin <= self.begin and other.end >= self.end:
            return []
        intersection = self.intersection(other)
        if intersection.begin == self.begin:
            return [Range(intersection.end + 1, self.end)]
        elif intersection.end == self.end:
            return [Range(self.begin, intersection.begin - 1)]
        else:
            return [
                Range(self.begin, intersection.begin - 1),
                Range(intersection.end + 1, self.end),
            ]

    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end

    def __iter__(self):
        return range(self.begin, self.end + 1)

    def __contains__(self, item: int):
        return self.begin <= item <= self.end

    def __len__(self):
        return self.end - self.begin + 1

    def __repr__(self):
        return f"Range({self.begin}, {self.end})"

    def __str__(self):
        return f"[{self.begin}-{self.end}]"


class Challenge(BaseChallenge):
    def part_1(self):
        input_blocks = self.get_input_blocks()
        sources = list(map(int, input_blocks[0].split(":")[1].split()))
        destinations = []
        for block in input_blocks[1:]:
            for source in sources[:]:
                for range_ in self.iter_mappings(block):
                    if source in Range(range_[1], range_[1] + range_[2] - 1):
                        destinations.append(source + range_[0] - range_[1])
                        sources.remove(source)
                        break
                else:
                    sources.remove(source)
                    destinations.append(source)
            sources, destinations = destinations, sources
        return min(sources)

    def part_2(self):
        input_blocks = self.get_input_blocks()
        destinations = []
        sources: list[Range] = list(self.get_seeds_ranges(input_blocks[0]))
        for block in input_blocks[1:]:
            for range_ in self.iter_mappings(block):
                source_map = Range(range_[1], range_[1] + range_[2] - 1)
                shifted_by = range_[0] - source_map.begin
                for source in sources[:]:
                    if intersection := source.intersection(source_map):
                        destinations.append(intersection.shift_by(shifted_by))
                        sources.remove(source)
                        if source_diff := source.diff(source_map):
                            sources.extend(source_diff)
            destinations.extend(sources)
            sources.clear()
            sources, destinations = destinations, sources
        return min(sources, key=lambda x: x.begin).begin

    @staticmethod
    def get_seeds_ranges(seeds_line: str):
        """
        :param seeds_line: i.e "seeds: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14"
        :return:
        """
        seeds_ranges: list[int] = list(map(int, seeds_line.split(":")[1].split()))
        for i in range(0, len(seeds_ranges), 2):
            yield Range(seeds_ranges[i], seeds_ranges[i] + seeds_ranges[i + 1] - 1)

    def get_input_blocks(self):
        input_lines = "\n".join(self.get_input_lines(part=1))
        input_blocks = input_lines.split("\n\n")
        return input_blocks

    @staticmethod
    def iter_mappings(block: str) -> Generator[tuple[int, int, int], None, None]:
        """Iterate over the ranges in a block.
        First element is the name of the mapping.
        :return: Generator of (dest_start, src_start, length)
        """
        for line in block.splitlines()[1:]:
            dest_start, src_start, length = map(int, line.split())
            yield dest_start, src_start, length


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
