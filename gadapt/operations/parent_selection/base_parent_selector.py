import random
from abc import ABC, abstractmethod
from typing import List, Tuple

from gadapt.ga_model.candidate_solution import CandidateSolution


class BaseParentSelector(ABC):
    """
    Base Parent Selector

    Selects individuals for mating from the population
    """

    def __init__(self):
        super().__init__()
        self.population = None

    def select_mates(self, population) -> List[Tuple[CandidateSolution, CandidateSolution]]:
        """
        Selects and returns individuals for the crossover from the population
        Args:
            population: the population for the mates selection
        """
        self.population = population
        return self._select_mates_from_population()

    def _select_mates_from_population(self) -> List[Tuple[CandidateSolution, CandidateSolution]]:
        working_candidate_solutions = self._select_potential_parents()
        num_of_crossover_parents = self.population.options.number_of_crossover_parents
        working_candidate_solutions_len = len(working_candidate_solutions)
        if num_of_crossover_parents > working_candidate_solutions_len:
            num_of_crossover_parents = working_candidate_solutions_len
        working_candidate_solutions = working_candidate_solutions[:num_of_crossover_parents]
        working_candidate_solutions_len = len(working_candidate_solutions)
        random_number_for_reserve = random.randint(0, working_candidate_solutions_len - 1)
        reserve_candidate_solution = working_candidate_solutions[random_number_for_reserve]
        list_of_mates: List[Tuple[CandidateSolution, CandidateSolution]] = []
        while len(working_candidate_solutions) > 0:
            c1 = working_candidate_solutions.pop(0)
            if len(working_candidate_solutions) > 0:
                c2 = working_candidate_solutions.pop(0)
            else:
                c2 = reserve_candidate_solution
            list_of_mates.append((c1, c2))
        return list_of_mates

    @abstractmethod
    def _select_potential_parents(self):
        pass
