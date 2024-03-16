import random
from gadapt.ga_model.gene import Gene
from gadapt.operations.mutation.gene_mutation.random_gene_mutator import (
    RandomGeneMutator,
)
from gadapt.utils.ga_utils import get_rand_bool, get_rand_bool_with_probability


class ExtremePointedGeneMutator(RandomGeneMutator):

    def _make_mutated_value(self, g: Gene):
        return self._make_mutation(g)

    def _make_rounded_random_value_below_or_above(self, g: Gene):
        return round(
            self._make_random_value_below_or_above(g), g.genetic_variable.decimal_places
        )

    def _make_random_value_below_or_above(self, g: Gene):
        if get_rand_bool():
            return self._make_random_value_above(g)
        return self._make_random_value_below(g)

    def _make_random_value_below(self, g: Gene):
        if g.variable_value == g.genetic_variable.min_value:
            return g.genetic_variable.make_random_value()
        number_of_steps = random.randint(
            0,
            round(
                (g.variable_value - g.genetic_variable.min_value)
                / g.genetic_variable.step
            ),
        )
        return g.genetic_variable.min_value + number_of_steps * g.genetic_variable.step

    def _make_random_value_above(self, g: Gene):
        if g.variable_value == g.genetic_variable.max_value:
            return g.genetic_variable.make_random_value()
        number_of_steps = random.randint(
            0,
            round(
                (g.genetic_variable.max_value - g.variable_value)
                / g.genetic_variable.step
            ),
        )
        return g.variable_value + number_of_steps * g.genetic_variable.step

    def _get_mutate_func(self, g: Gene):
        prob = g.genetic_variable.relative_standard_deviation
        if prob > 1.0:
            prob = 1.0
        should_mutate_random = get_rand_bool_with_probability(prob)
        if should_mutate_random:
            return super()._make_mutated_value
        else:
            return self._make_rounded_random_value_below_or_above

    def _make_mutation(self, g: Gene):
        f = self._get_mutate_func(g)
        return f(g)
