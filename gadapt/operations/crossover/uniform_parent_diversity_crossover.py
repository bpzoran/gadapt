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
from operations.crossover.uniform_crossover import UniformCrossover
from utils import ga_utils


class UniformParentDiversityCrossover(UniformCrossover):
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
        super(UniformParentDiversityCrossover, self).__init__(
            var_combination, mutator, immigrator
        )
        self._genetic_diversity = None

    def _get_genetic_diversity(self) -> float:
        return abs(self._mother_gene.variable_value - self._father_gene.variable_value) / (
                self._father_gene.decision_variable.max_value - self._father_gene.decision_variable.min_value
        )

    def _get_parent_diversity(self):
        return round(ga_utils.average(self._genetic_diversity), 2)

    def _decision_variable_crossed(self):
        self._genetic_diversity.append(
            self._get_genetic_diversity()
        )

    def _all_decision_variable_crossed(self):
        parent_diversity = self._get_parent_diversity()
        self._offspring1.parent_diversity = parent_diversity
        self._offspring2.parent_diversity = parent_diversity

    def _cross_genetic_material(
            self
    ):
        self._genetic_diversity = []
        super()._cross_genetic_material()
