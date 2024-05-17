import math
from abc import ABC, abstractmethod
from typing import Tuple, List

from gadapt.ga_model.gene import Gene
from gadapt.ga_model.chromosome import Chromosome
from gadapt.operations.immigration.chromosome_immigration.base_chromosome_immigrator import (
    BaseChromosomeImmigrator,
)
from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_selector import (
    BaseGeneMutationSelector,
)


class BaseCrossover(ABC):
    """Base Crossover Class

    Args:
        mutator (BaseGeneMutationSelector): mutation algorithm to
        be passed to offspring chromosomes
        immigrator (BaseChromosomeImmigrator): immigration algorithm
        to be passed to offspring chromosomes
        should be mutated on both sides with the same probability
    """

    def __init__(
        self,
        mutator: BaseGeneMutationSelector,
        immigrator: BaseChromosomeImmigrator,
    ):
        self._mutator = mutator
        self._immigrator = immigrator
        self._current_gene_number = -1

    def mate(self, chromosome_pairs: List[Tuple[Chromosome, Chromosome]], population):
        """
        Returns list of chromosome pairs using parents' genetic material

        Args:
            chromosome_pairs (List[Tuple[Chromosome, Chromosome]]) : List of chromosome pairs for mating
            population: Population
        """
        for chromosome1, chromosome2 in chromosome_pairs:
            offspring1, offspring2 = self._mate_pair(
                chromosome1, chromosome2, population.population_generation
            )
            population.add_chromosomes((offspring1, offspring2))
        current_len = len(population)
        chromosome_surplus = current_len - population.options.population_size
        if chromosome_surplus > 0:
            sorted_by_cost_value = sorted(
                population, key=lambda chrom: chrom.cost_value, reverse=True
            )
            i = 0
            for c in sorted_by_cost_value:
                if i >= chromosome_surplus:
                    break
                if not math.isnan(c.cost_value):
                    population.chromosomes.remove(c)

    def _mate_pair(
        self, mother: Chromosome, father: Chromosome, population_generation: int
    ):
        """Returns two offspring chromosomes using parents' genetic material

        Args:
            mother (Chromosome): The first chromosome for mating
            father (Chromosome): The second chromosome for mating
            population_generation (int): Current generation in the population

        Returns:
            Chromosome: the first offspring chromosome
            Chromosome: the second offspring chromosome
        """
        if len(mother) != len(father):
            raise Exception("Mother and father must have the same number of genes!")
        self._mother = mother
        self._father = father
        self._offspring1 = Chromosome(population_generation)
        self._offspring2 = Chromosome(population_generation)
        self._cross_genetic_material()
        self._increase_generation()
        return self._offspring1, self._offspring2

    def _cross_genetic_material(self):
        number_of_genes = len(self._father)
        for self._current_gene_number in range(number_of_genes):
            self._mother_gene, self._father_gene = self._get_mother_father_genes()
            decision_variable_father = self._mother_gene.decision_variable
            decision_variable_mother = self._father_gene.decision_variable
            if decision_variable_father != decision_variable_mother:
                decision_variable_mother = next(
                    (
                        item.decision_variable
                        for item in self._mother
                        if item.decision_variable == decision_variable_father
                    ),
                    None,
                )
            if decision_variable_mother is None:
                raise Exception(
                    "chromosomes in crossover do not have the same structure!"
                )
            self._decision_variable_crossed()
            var1, var2 = self._combine()
            self._offspring1.add_gene(decision_variable_father, var1)
            self._offspring2.add_gene(decision_variable_father, var2)
        self._all_decision_variable_crossed()
        self._offspring1.mother_id = self._mother.chromosome_id
        self._offspring2.mother_id = self._mother.chromosome_id
        self._offspring1.father_id = self._father.chromosome_id
        self._offspring2.father_id = self._father.chromosome_id

    def _get_mother_father_genes(self) -> Tuple[Gene, Gene]:
        if self._current_gene_number == -1:
            raise Exception("_current_gene_number not set")
        father_gene = self._father[self._current_gene_number]
        mother_gene = self._mother[self._current_gene_number]
        return mother_gene, father_gene

    @abstractmethod
    def _combine(self):
        pass

    def _increase_generation(self):
        current_generation = self._mother.chromosome_generation
        if (
            current_generation == 0
            or current_generation < self._father.chromosome_generation
        ):
            current_generation = self._father.chromosome_generation
        current_generation += 1
        self._offspring1.chromosome_generation = current_generation
        self._offspring2.chromosome_generation = current_generation

        current_generation = 0
        if (
            self._mother.first_mutant_generation > 0
            or self._father.first_mutant_generation > 0
        ):
            current_generation = self._mother.first_mutant_generation
            if (
                current_generation == 0
                or self._father.first_mutant_generation > current_generation
            ):
                current_generation = self._father.first_mutant_generation
            current_generation += 1
        self._offspring1.first_mutant_generation = current_generation
        self._offspring2.first_mutant_generation = current_generation

        current_generation = 0
        if (
            self._mother.last_mutant_generation > 0
            or self._father.last_mutant_generation > 0
        ):
            current_generation = self._mother.last_mutant_generation
            if current_generation == 0 or (
                0 < self._father.last_mutant_generation < current_generation
            ):
                current_generation = self._father.last_mutant_generation
            current_generation += 1
        self._offspring1.last_mutant_generation = current_generation
        self._offspring2.last_mutant_generation = current_generation

        current_generation = 0
        if (
            self._mother.first_immigrant_generation > 0
            or self._father.first_immigrant_generation > 0
        ):
            current_generation = self._mother.first_immigrant_generation
            if (
                current_generation == 0
                or self._father.first_immigrant_generation > current_generation
            ):
                current_generation = self._father.first_immigrant_generation
            current_generation += 1
        self._offspring1.first_immigrant_generation = current_generation
        self._offspring2.first_immigrant_generation = current_generation

        current_generation = 0
        if (
            self._mother.last_immigrant_generation > 0
            or self._father.last_immigrant_generation > 0
        ):
            current_generation = self._mother.last_immigrant_generation
            if current_generation == 0 or (
                0 < self._father.last_immigrant_generation < current_generation
            ):
                current_generation = self._father.last_immigrant_generation
            current_generation += 1
        self._offspring1.last_immigrant_generation = current_generation
        self._offspring2.last_immigrant_generation = current_generation

    def _decision_variable_crossed(self):
        pass

    def _all_decision_variable_crossed(self):
        pass
