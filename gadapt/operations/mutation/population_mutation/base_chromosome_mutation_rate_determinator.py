from abc import ABC, abstractmethod
import math
import random
from typing import List
from gadapt.ga_model.chromosome import Chromosome


class BaseChromosomeMutationRateDeterminator(ABC):
    def __init__(self) -> None:
        """
        Base class for mutating chromosomes in population
        Args:
            options: genetic algorithm options
        """
        super().__init__()

    def get_number_of_mutation_chromosomes(self, population, max_number_of_mutation_chromosomes):
        if population is None:
            raise Exception("Population must not be null")
        return self._get_number_of_mutation_chromosomes(
                population, max_number_of_mutation_chromosomes
            )

    @abstractmethod
    def _get_number_of_mutation_chromosomes(
            self, population, max_number_of_mutation_chromosomes
    ) -> int:
        pass
