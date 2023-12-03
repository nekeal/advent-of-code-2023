import re

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    def find_first_digit(self, sequence: str):
        for c in sequence:
            if c.isdigit():
                return c

    def part_1(self):
        total_sum = 0
        for line in self.get_input_lines(part=1):
            val1 = self.find_first_digit(line)
            val2 = self.find_first_digit(line[::-1])
            total_sum += int(val1 + val2)
        return total_sum

    def get_first_and_last_digit(self, line):
        possible_strings = (
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "zero",
        ) + tuple(map(str, range(10)))
        min_index, max_index = len(line), 0
        first_digit, last_digit = None, None
        for string in possible_strings:
            if (left_index := line.find(string)) >= 0 and left_index < min_index:
                min_index = min(min_index, left_index)
                first_digit = string
            if (right_index := line.rfind(string)) >= 0 and right_index >= max_index:
                max_index = max(max_index, right_index)
                last_digit = string
        return self.preprocess_line(first_digit), self.preprocess_line(last_digit)

    def part_2(self):
        total_sum = 0
        for line in self.get_input_lines(part=2):
            val1, val2 = self.get_first_and_last_digit(line)
            total_sum += int(val1 + val2)
        return total_sum

    def preprocess_line(self, line):
        str_to_digit = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
            "zero": "0",
        }
        for key, value in reversed(str_to_digit.items()):
            line = line.replace(key, value)
        return line


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
