from abc import ABC, abstractmethod
from typing import List, Tuple

from gadapt.ga_model.chromosome import Chromosome


class BaseParentSelector(ABC):
    """
    Base Parent Selector

    Selects individuals for mating from the population
    """

    def __init__(self):
        super().__init__()
        self.population = None

    def select_mates(self, population) -> List[Tuple[Chromosome, Chromosome]]:
        """
        Selects and returns individuals for the crossover from the population
        Args:
            population: the population for the mates selection
        """
        self.population = population
        return self._select_mates_from_population()

    @abstractmethod
    def _select_mates_from_population(self) -> List[Tuple[Chromosome, Chromosome]]:
        pass
