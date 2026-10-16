from abc import ABC, abstractmethod
from typing import Optional

from gadapt.ga_model.population import Population
from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.operations.immigration.candidate_solution_immigration.base_candidate_solution_immigrator import (
    BaseCandidateSolutionImmigrator,
)


class BasePopulationImmigrator(ABC):
    """
    Base class for population immigration
    """

    def __init__(self, candidate_solution_immigrator: BaseCandidateSolutionImmigrator):
        self.population: Optional[Population] = None
        self._candidate_solution_immigrator = candidate_solution_immigrator

    def immigrate(self, population):
        """
        Immigrates candidate solutions into the population
        Args:
            population: Population to immigrate new candidate solutions
        """
        self.population = population
        self._immigrate_population()

    @abstractmethod
    def _immigrate_population(self):
        pass

    def _immigrate_candidate_solution(self, c: CandidateSolution):
        self._candidate_solution_immigrator.immigrate(c)
