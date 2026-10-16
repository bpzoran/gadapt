import random
from typing import List

from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_rate_determinator import (
    BaseCandidateSolutionMutationRateDeterminator,
)


class ComposedCandidateSolutionMutationRateDeterminator(
    BaseCandidateSolutionMutationRateDeterminator
):
    """
    Allows for the composition of multiple determinators to be used in a random order.
    """

    def __init__(self) -> None:
        super().__init__()
        self.determinators: List[BaseCandidateSolutionMutationRateDeterminator] = []

    def append(self, determinator: BaseCandidateSolutionMutationRateDeterminator):
        """
        Appends determinator to the composition of determinators
        """
        self.determinators.append(determinator)

    def _get_number_of_mutation_candidate_solutions(self):
        if self.population is None:
            raise Exception("Population must not be null")
        if len(self.determinators) == 0:
            raise Exception("at least one determinator must be added")
        for determinator in self.determinators:
            determinator.population = self.population
            determinator.max_number_of_mutation_candidate_solutions = (
                self.max_number_of_mutation_candidate_solutions
            )
        if len(self.determinators) > 1:
            random.shuffle(self.determinators)
        current_determinator = self.determinators[0]
        return current_determinator._get_number_of_mutation_candidate_solutions()
