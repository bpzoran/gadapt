from abc import ABC

from gadapt.operations.crossover.base_crossover_probability_determinator import BaseCrossoverProbabilityDeterminator


class CostDiversityCrossoverProbabilityDeterminator(BaseCrossoverProbabilityDeterminator):
    def get_crossover_probability(self, population):
        crossover_probability_range = population.options.crossover_max_probability - population.options.crossover_min_probability
        crossover_rate = population.get_relative_cost_diversity_coefficient()
        return population.options.crossover_min_probability + crossover_probability_range * crossover_rate
