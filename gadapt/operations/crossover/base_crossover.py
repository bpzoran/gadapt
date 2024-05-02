from abc import ABC, abstractmethod
from gadapt.ga_model.chromosome import Chromosome
from gadapt.operations.immigration.chromosome_immigration.base_chromosome_immigrator import (
    BaseChromosomeImmigrator,
)
from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_selector import (
    BaseGeneMutationSelector,
)
from gadapt.operations.gene_combination.base_gene_combination import BaseGeneCombination


class BaseCrossover(ABC):
    """Base Crossover Class

    Args:
        gene_combination (BaseGeneCombination): the algorithm
        for how genes are to be combined
        mutator (BaseGeneMutationSelector): mutation algorithm to
        be passed to offspring chromosomes
        immigrator (BaseChromosomeImmigrator): immigration algorithm
        to be passed to offspring chromosomes
        mutation_on_both_sides (bool): indicates if offspring chromosomes
        should be mutated on both sides with the same probability
    """

    def __init__(
        self,
        gene_combination: BaseGeneCombination,
        mutator: BaseGeneMutationSelector,
        immigrator: BaseChromosomeImmigrator,
        mutation_on_both_sides: bool = True,
    ):
        self._mutation_on_both_sides = True
        self._gene_combination = gene_combination
        self._mutator = mutator
        self._immigrator = immigrator
        self._mutation_on_both_sides = mutation_on_both_sides
        self.number_of_genes = 0

    def mate(self, mother: Chromosome, father: Chromosome, population_generation: int):
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
        offspring1 = Chromosome(self._mutator, self._immigrator, population_generation)
        offspring2 = Chromosome(self._mutator, self._immigrator, population_generation)
        self._cross_genetic_material(mother, father, offspring1, offspring2)
        self._increase_generation(offspring1, offspring2, mother, father)
        return offspring1, offspring2

    @abstractmethod
    def _cross_genetic_material(
        self,
        mother: Chromosome,
        father: Chromosome,
        offspring1: Chromosome,
        offspring2: Chromosome,
    ):
        pass

    def _increase_generation(
        self,
        offspring1: Chromosome,
        offspring2: Chromosome,
        mother: Chromosome,
        father: Chromosome,
    ):
        current_generation = mother.chromosome_generation
        if current_generation == 0 or current_generation < father.chromosome_generation:
            current_generation = father.chromosome_generation
        current_generation += 1
        offspring1.chromosome_generation = current_generation
        offspring2.chromosome_generation = current_generation

        current_generation = 0
        if mother.first_mutant_generation > 0 or father.first_mutant_generation > 0:
            current_generation = mother.first_mutant_generation
            if (
                current_generation == 0
                or father.first_mutant_generation > current_generation
            ):
                current_generation = father.first_mutant_generation
            current_generation += 1
        offspring1.first_mutant_generation = current_generation
        offspring2.first_mutant_generation = current_generation

        current_generation = 0
        if mother.last_mutant_generation > 0 or father.last_mutant_generation > 0:
            current_generation = mother.last_mutant_generation
            if current_generation == 0 or (
                father.last_mutant_generation > 0
                and father.last_mutant_generation < current_generation
            ):
                current_generation = father.last_mutant_generation
            current_generation += 1
        offspring1.last_mutant_generation = current_generation
        offspring2.last_mutant_generation = current_generation

        current_generation = 0
        if (
            mother.first_immigrant_generation > 0
            or father.first_immigrant_generation > 0
        ):
            current_generation = mother.first_immigrant_generation
            if (
                current_generation == 0
                or father.first_immigrant_generation > current_generation
            ):
                current_generation = father.first_immigrant_generation
            current_generation += 1
        offspring1.first_immigrant_generation = current_generation
        offspring2.first_immigrant_generation = current_generation

        current_generation = 0
        if mother.last_immigrant_generation > 0 or father.last_immigrant_generation > 0:
            current_generation = mother.last_immigrant_generation
            if current_generation == 0 or (
                father.last_immigrant_generation > 0
                and father.last_immigrant_generation < current_generation
            ):
                current_generation = father.last_immigrant_generation
            current_generation += 1
        offspring1.last_immigrant_generation = current_generation
        offspring2.last_immigrant_generation = current_generation
