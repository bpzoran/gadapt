from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_rate_determinator import (
    BaseCandidateSolutionMutationRateDeterminator,
)


class StrictCandidateSolutionMutationRateDeterminator(BaseCandidateSolutionMutationRateDeterminator):
    """
    Provides a strict determination of the number of candidate solutions to be mutated in a population.
    """

    def __init__(self) -> None:
        super().__init__()

    def _get_number_of_mutation_candidate_solutions(self) -> int:
        return self.max_number_of_mutation_candidate_solutions
