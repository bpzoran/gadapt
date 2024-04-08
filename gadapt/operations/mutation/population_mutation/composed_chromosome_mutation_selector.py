import random
from typing import List

from operations.mutation.population_mutation.base_chromosome_mutation_rate_determinator import \
    BaseChromosomeMutationRateDeterminator
from operations.mutation.population_mutation.base_chromosome_mutation_selector import BaseChromosomeMutationSelector


class ComposedChromosomeMutationSelector(BaseChromosomeMutationSelector):
    def __init__(self, chromosome_mutation_rate_determinator: BaseChromosomeMutationRateDeterminator) -> None:
        """
        Population mutator that consists of more different population mutators
        Args:
            options: genetic algorithm options
        """
        super().__init__(chromosome_mutation_rate_determinator)
        self.selectors: List[BaseChromosomeMutationSelector] = []

    def append(self, mutator: BaseChromosomeMutationSelector):
        """
        Appends mutator to the composition of mutators
        """
        self.selectors.append(mutator)

    def _mutate_population(self, population, max_number_of_mutation_chromosomes):
        if population is None:
            raise Exception("Population must not be null")
        if len(self.selectors) == 0:
            raise Exception("at least one mutator must be added")
        random.shuffle(self.selectors)
        nmc = 0
        number_of_mutation_chromosomes = self._chromosome_mutation_rate_determinator.get_number_of_mutation_chromosomes(population, max_number_of_mutation_chromosomes)
        for m in self.selectors:
            if nmc < number_of_mutation_chromosomes:
                mc = m._mutate_population(
                    population, number_of_mutation_chromosomes - nmc
                )
                nmc += mc
        return nmc
