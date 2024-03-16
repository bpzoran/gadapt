import math
from gadapt.ga_model.gene import Gene
from gadapt.operations.mutation.gene_mutation.base_gene_mutator import BaseGeneMutator
from gadapt.utils.ga_utils import normally_distributed_random


class NormalDistributionGeneMutator(BaseGeneMutator):

    def _make_mutated_value(self, g: Gene):
        curr_value = g.variable_value
        if math.isnan(curr_value):
            curr_value = g.genetic_variable.make_random_value()
        range = g.genetic_variable.max_value - g.genetic_variable.min_value
        mean = (curr_value - g.genetic_variable.min_value) / (range)
        normal_distribution_random_value = normally_distributed_random(mean, 0.2, 0, 1)
        number_of_steps = round(
            (normal_distribution_random_value * range) / g.genetic_variable.step
        )
        return g.genetic_variable.min_value + number_of_steps * g.genetic_variable.step
