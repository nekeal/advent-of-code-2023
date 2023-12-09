import itertools
import operator as op
from typing import Callable, Literal

from aoc.base import BaseChallenge


class Challenge(BaseChallenge):
    def part_1(self):
        histories = self.get_histories(part=1)
        total_sum = 0
        for history in histories:
            result = self.process_history_forward(history)
            total_sum += result[0][-1]
        return total_sum

    def part_2(self):
        histories = self.get_histories(part=2)
        total_sum = 0
        for history in histories:
            result = self.process_history_backward(history)
            total_sum += result[0][0]
        return total_sum

    def get_histories(self, part: int):
        input_lines = self.get_input_lines(part=part)
        return list(self.parse_input_lines(input_lines))

    @staticmethod
    def parse_input_lines(input_lines: list[str]):
        for line in input_lines:
            yield list(map(int, line.split()))

    @staticmethod
    def get_history_child(history: list[int]):
        return [history[i] - history[i - 1] for i in range(1, len(history))]

    def _process_history(
        self, history: list[int], index, operator: Callable[[int, int], int]
    ):
        """
        Calculates history with predicted value.
        :param index: index determining index of the value prediction is based on.
        :param history: list of values
        :param operator: operator to use for prediction (add or sub)
        :return:
        """
        _reverse = 1 if index == -1 else -1
        if set(history) == {0}:
            return list(itertools.chain(*[history, [0]][::_reverse])), 0
        child = self.get_history_child(history)
        predicted_child, total_sum = self._process_history(child, index, operator)
        result = list(
            itertools.chain(
                *[history, [operator(history[index], predicted_child[index])]][
                    ::_reverse
                ]
            )
        )
        return result, total_sum + result[index]

    def process_history_forward(self, history: list[int]):
        return self._process_history(history, -1, op.add)

    def process_history_backward(self, history: list[int]):
        return self._process_history(history, 0, op.sub)


if __name__ == "__main__":
    Challenge().run()
    Challenge(use_test_data=True).run()
