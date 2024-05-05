from abc import ABC, abstractmethod


class BasePopulationImmigrator(ABC):
    """
    Base class for population immigration
    """

    def __init__(self):
        self.population = None

    def immigrate(self, population):
        """
        Immigrates chromosomes into the population
        Args:
            population: Population to immigrate new chromosomes
        """
        self.population = population
        self._immigrate_population()

    @abstractmethod
    def _immigrate_population(self):
        pass
