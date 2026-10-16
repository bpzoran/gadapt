import random

from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_rate_determinator import (
    BaseCandidateSolutionMutationRateDeterminator,
)
from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_selector import (
    BaseCandidateSolutionMutationSelector,
)
from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_selector import (
    BaseDecisionVariableMutationSelector,
)


class RandomCandidateSolutionMutationSelector(BaseCandidateSolutionMutationSelector):
    """
    Implements the mutation of candidate solutions in a population based on a random selection of candidate solutions
    """

    def __init__(
        self,
        candidate_solution_mutation_rate_determinator: BaseCandidateSolutionMutationRateDeterminator,
        decision_variable_mutation_selector: BaseDecisionVariableMutationSelector,
    ) -> None:
        super().__init__(candidate_solution_mutation_rate_determinator, decision_variable_mutation_selector)

    def _get_candidate_solutions_for_mutation(self):
        if self.population is None:
            raise Exception("population must not be None")
        unallocated_candidate_solutions = self._get_unallocated_candidate_solutions(
            self._sort_key_random
        )
        mutation_candidate_solution_number = self.number_of_mutation_candidate_solutions
        if mutation_candidate_solution_number == 0:
            return 0
        candidate_solutions_for_mutation = unallocated_candidate_solutions[:mutation_candidate_solution_number]
        return candidate_solutions_for_mutation

    def _sort_key_random(self, _: CandidateSolution):
        return random.random()
