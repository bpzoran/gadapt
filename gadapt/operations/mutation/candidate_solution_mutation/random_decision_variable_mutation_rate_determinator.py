import random

from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_rate_determinator import (
    BaseDecisionVariableMutationRateDeterminator,
)


class RandomDecisionVariableMutationRateDeterminator(BaseDecisionVariableMutationRateDeterminator):
    """
    Determines the random number of mutation decision variables in a candidate solution between 1 and the maximum number of mutation decision variables specified.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def _get_number_of_mutation_decision_variables(self) -> int:
        if self.max_number_of_mutation_decision_variables <= 1:
            return 1
        return random.randint(1, self.max_number_of_mutation_decision_variables)
