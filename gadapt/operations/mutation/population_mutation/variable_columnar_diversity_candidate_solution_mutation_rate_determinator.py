import gadapt.utils.ga_utils as ga_utils
from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_rate_determinator import (
    BaseCandidateSolutionMutationRateDeterminator,
)


class VariableColumnarDiversityCandidateSolutionMutationRateDeterminator(
    BaseCandidateSolutionMutationRateDeterminator
):
    """
    Determining the number of candidate solutions to be mutated in a population based on the variable-columnar-diversity coefficient of the decision variables.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def _get_number_of_mutation_candidate_solutions(self) -> int:


        mutation_rate = ga_utils.get_columnar_diversity_rate(self.population)
        f_return_value = mutation_rate * float(self.max_number_of_mutation_candidate_solutions)
        return round(f_return_value)
