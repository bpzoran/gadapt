from abc import ABC, abstractmethod
from gadapt.ga_model.population import Population


class BaseCrossoverProbabilityDeterminator(ABC):

    @abstractmethod
    def get_crossover_probability(self, population: Population) -> float:
        pass
