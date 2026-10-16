from abc import ABC, abstractmethod


class BaseCandidateSolutionMutationRateDeterminator(ABC):
    """
    Provides a framework for determining the number of candidate solutions to be mutated in a population.
    """

    def __init__(self) -> None:
        super().__init__()
        self.population = None
        self.max_number_of_mutation_candidate_solutions = -1

    def get_number_of_mutation_candidate_solutions(
        self, population, max_number_of_mutation_candidate_solutions
    ):
        if population is None:
            raise Exception("Population must not be null")
        self.population = population
        self.max_number_of_mutation_candidate_solutions = max_number_of_mutation_candidate_solutions
        return self._get_number_of_mutation_candidate_solutions()

    @abstractmethod
    def _get_number_of_mutation_candidate_solutions(self) -> int:
        pass
