from abc import ABC, abstractmethod


class BaseCandidateSolutionImmigrator(ABC):
    """
    Base class for candidate solution immigration
    """

    def __init__(self):
        super().__init__()
        self.candidate_solution = None

    def immigrate(self, c):
        """
        Makes one candidate solution immigrant
        Args:
            c: candidate solution to become the immigrant
        """
        self.candidate_solution = c
        self._immigrate_candidate_solution()
        self._candidate_solution_immigrated()

    @abstractmethod
    def _immigrate_candidate_solution(self):
        pass

    def _candidate_solution_immigrated(self):
        self.candidate_solution.is_immigrant = True
        if self.candidate_solution.first_immigrant_generation == 0:
            self.candidate_solution.first_immigrant_generation += 1
        self.candidate_solution.last_immigrant_generation = 1
        self.candidate_solution.first_mutant_generation = 0
        self.candidate_solution.last_mutant_generation = 0
        self.candidate_solution.set_candidate_solution_string_none()
