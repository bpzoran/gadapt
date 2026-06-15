import random
from abc import ABC
from typing import List

from gadapt.operations.crossover.base_crossover import BaseCrossover
from gadapt.operations.crossover.base_crossover_probability_determinator import BaseCrossoverProbabilityDeterminator


class ComposedCrossoverProbabilityDeterminator(BaseCrossoverProbabilityDeterminator):
    def __init__(self) -> None:
        super().__init__()
        self.determinators: List[BaseCrossoverProbabilityDeterminator] = []

    def append(self, determinator: BaseCrossoverProbabilityDeterminator):
        self.determinators.append(determinator)

    def get_crossover_probability(self, population):
        if len(self.determinators) > 1:
            random.shuffle(self.determinators)
        current_determinator = self.determinators[0]
        return current_determinator.get_crossover_probability(population)

    def __len__(self):
        return len(self.determinators)
