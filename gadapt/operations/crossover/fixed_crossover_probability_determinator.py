from abc import ABC

from gadapt.operations.crossover.base_crossover_probability_determinator import BaseCrossoverProbabilityDeterminator


class FixedCrossoverProbabilityDeterminator(BaseCrossoverProbabilityDeterminator):
    def get_crossover_probability(self, population):
        return population.options.crossover_probability
