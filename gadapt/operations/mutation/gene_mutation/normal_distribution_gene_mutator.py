import math
from gadapt.ga_model.gene import Gene
from gadapt.operations.mutation.gene_mutation.random_gene_mutator import (
    RandomGeneMutator,
)
from gadapt.utils.ga_utils import (
    get_rand_bool,
    get_rand_bool_with_probability,
    normally_distributed_random,
)


class NormalDistributionGeneMutator(RandomGeneMutator):

    def _make_mutated_value(self, g: Gene):
        f = self._get_mutate_func(g)
        return f(g)

    def _make_normally_distributed_random_value(self, g: Gene):
        if get_rand_bool():
            return super()._make_mutated_value(g)
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

    def _get_mutate_func(self, g: Gene):
        prob = g.genetic_variable.relative_standard_deviation
        if prob > 1.0:
            prob = 1.0
        should_mutate_random = get_rand_bool_with_probability(prob)
        if should_mutate_random:
            return super()._make_mutated_value
        else:
            return self._make_normally_distributed_random_value
