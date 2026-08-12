from gadapt.operations.crossover.base_crossover_probability_determinator import BaseCrossoverProbabilityDeterminator
from gadapt.utils import ga_utils


class ColumnarDiversityCrossoverProbabilityDeterminator(BaseCrossoverProbabilityDeterminator):
    def get_crossover_probability(self, population):
        crossover_probability_range = population.options.crossover_max_probability - population.options.crossover_min_probability
        crossover_rate = 1 - ga_utils.get_columnar_diversity_rate(population)
        return population.options.crossover_min_probability + crossover_probability_range * crossover_rate