from typing import Tuple
from gadapt.ga_model.chromosome import Chromosome
from gadapt.operations.crossover.base_crossover import BaseCrossover
from gadapt.ga_model.gene import Gene
from gadapt.operations.immigration.chromosome_immigration.base_chromosome_immigrator import (
    BaseChromosomeImmigrator,
)
from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_selector import (
    BaseGeneMutationSelector,
)
from gadapt.operations.gene_combination.base_gene_combination import BaseGeneCombination
from utils import ga_utils


class UniformCrossover(BaseCrossover):
    """
    Uniform Crossover. Genes from parents' chromosomes are combined in a uniform way.
    Calculates diversity of parents and save it to chromosomes.
    """

    def __init__(
        self,
        var_combination: BaseGeneCombination,
        mutator: BaseGeneMutationSelector,
        immigrator: BaseChromosomeImmigrator,
    ):
        super(UniformCrossover, self).__init__(
            var_combination, mutator, immigrator
        )
        self._current_gene_number = -1

    def _get_mother_father_genes(self) -> Tuple[Gene, Gene]:
        if self._current_gene_number == -1:
            raise Exception("_current_gene_number not set")
        father_gene = self._father[self._current_gene_number]
        mother_gene = self._mother[self._current_gene_number]
        return mother_gene, father_gene
