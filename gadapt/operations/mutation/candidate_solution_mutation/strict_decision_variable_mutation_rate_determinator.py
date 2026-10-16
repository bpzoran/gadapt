from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_rate_determinator import (
    BaseDecisionVariableMutationRateDeterminator,
)


class StrictDecisionVariableMutationRateDeterminator(BaseDecisionVariableMutationRateDeterminator):
    """
    Determines the strict number of mutation decision variables in a candidate solution.
    """

    def __init__(self) -> None:
        super().__init__()

    def _get_number_of_mutation_decision_variables(self) -> int:
        return self.max_number_of_mutation_decision_variables
