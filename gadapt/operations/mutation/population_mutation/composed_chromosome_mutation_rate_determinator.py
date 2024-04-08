import random
from typing import List

from operations.mutation.population_mutation.base_chromosome_mutation_rate_determinator import \
    BaseChromosomeMutationRateDeterminator


class ComposedChromosomeMutationRateDeterminator(BaseChromosomeMutationRateDeterminator):
    def __init__(self) -> None:
        """
        Population mutator that consists of more different population mutators
        Args:
            options: genetic algorithm options
        """
        super().__init__()
        self.determinators: List[BaseChromosomeMutationRateDeterminator] = []

    def append(self, determinator: BaseChromosomeMutationRateDeterminator):
        """
        Appends mutator to the composition of mutators
        """
        self.determinators.append(determinator)

    def _get_number_of_mutation_chromosomes(self, population, max_number_of_mutation_chromosomes):
        if population is None:
            raise Exception("Population must not be null")
        if len(self.determinators) == 0:
            raise Exception("at least one mutator must be added")
        if len(self.determinators) > 1:
            random.shuffle(self.determinators)
        current_determinator = self.determinators[0]
        return current_determinator.get_number_of_mutation_chromosomes(population, max_number_of_mutation_chromosomes)
