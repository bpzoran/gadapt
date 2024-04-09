from gadapt.ga_model.chromosome import Chromosome
import random

from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_selector import (
    BaseGeneMutationSelector,
)
from operations.mutation.chromosome_mutation.base_gene_mutation_rate_determinator import \
    BaseGeneMutationRateDeterminator


class RandomGeneMutationSelector(BaseGeneMutationSelector):
    """
    Random mutation of the chromosome.
    """

    def __init__(self, gene_mutation_rate_determinator: BaseGeneMutationRateDeterminator):
        super().__init__(gene_mutation_rate_determinator)

    def _mutate_chromosome(self, c: Chromosome, max_number_of_mutation_genes: int):
        if max_number_of_mutation_genes == 0:
            return
        genes_to_mutate = list(c)
        random.shuffle(genes_to_mutate)
        var_num = random.randint(1, self._gene_mutation_rate_determinator.get_number_of_mutation_genes(c, max_number_of_mutation_genes))
        for g in genes_to_mutate[:var_num]:
            g.mutate()
            self._gene_mutated(g, c)

        return var_num
