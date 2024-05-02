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


class UniformParentDiversityCrossover(BaseCrossover):
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
        self._current_gene_number = -1

    def _get_mother_father_genes(
        self, mother: Chromosome, father: Chromosome
    ) -> Tuple[Gene, Gene]:
        if self._current_gene_number == -1:
            raise Exception("_current_gene_number not set")
        father_gene = father[self._current_gene_number]
        mother_gene = mother[self._current_gene_number]
        return mother_gene, father_gene

    def _combine(self, mother_gene: Gene, father_gene: Gene):
        if self._gene_combination is None:
            raise Exception("gene_combination must not be null!")
        return self._gene_combination.combine(mother_gene, father_gene)

    def _get_genetic_diversity(self, g_m: Gene, g_f: Gene) -> float:
        return abs(g_m.variable_value - g_f.variable_value) / (
            g_f.decision_variable.max_value - g_f.decision_variable.min_value
        )

    def _cross_genetic_material(
        self,
        mother: Chromosome,
        father: Chromosome,
        offspring1: Chromosome,
        offspring2: Chromosome,
    ):
        self.number_of_genes = len(father)
        genetic_diversity = []
        for self._current_gene_number in range(self.number_of_genes):
            mother_gene, father_gene = self._get_mother_father_genes(mother, father)
            decision_variable_father = father_gene.decision_variable
            decision_variable_mother = mother_gene.decision_variable
            if decision_variable_father != decision_variable_mother:
                decision_variable_mother = next(
                    (
                        item.decision_variable
                        for item in mother
                        if item.decision_variable == decision_variable_father
                    ),
                    None,
                )
            if decision_variable_mother is None:
                raise Exception(
                    "chromosomes in crossover do not have the same structure!"
                )
            genetic_diversity.append(
                self._get_genetic_diversity(mother_gene, father_gene)
            )
            var1, var2 = self._combine(mother_gene, father_gene)
            offspring1.add_gene(decision_variable_father, var1)
            offspring2.add_gene(decision_variable_father, var2)
        parent_diversity = round(ga_utils.average(genetic_diversity), 2)
        offspring1.parent_diversity = parent_diversity
        offspring2.parent_diversity = parent_diversity
        offspring1.mutation_on_both_sides = self._mutation_on_both_sides
        offspring2.mutation_on_both_sides = self._mutation_on_both_sides
        offspring1.mother_id = mother.chromosome_id
        offspring2.mother_id = mother.chromosome_id
        offspring1.father_id = father.chromosome_id
        offspring2.father_id = father.chromosome_id
