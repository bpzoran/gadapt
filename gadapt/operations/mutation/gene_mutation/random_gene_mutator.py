from gadapt.ga_model.gene import Gene
from gadapt.operations.mutation.gene_mutation.base_gene_mutator import BaseGeneMutator


class RandomGeneMutator(BaseGeneMutator):

    def _make_mutated_value(self, g: Gene):
        return round(
            g.genetic_variable.make_random_value(), g.genetic_variable.decimal_places
        )
