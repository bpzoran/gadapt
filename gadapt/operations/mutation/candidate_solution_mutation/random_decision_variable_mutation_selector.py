import random

from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_rate_determinator import (
    BaseDecisionVariableMutationRateDeterminator,
)
from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_selector import (
    BaseDecisionVariableMutationSelector,
)
from gadapt.operations.mutation.decision_variable_mutation.base_decision_variable_mutator import BaseDecisionVariableMutator


class RandomDecisionVariableMutationSelector(BaseDecisionVariableMutationSelector):
    """
    Selects and mutates decision variables in a candidate solution using a random mutation strategy.
    """

    def __init__(
        self,
        decision_variable_mutation_rate_determinator: BaseDecisionVariableMutationRateDeterminator,
        decision_variable_mutator: BaseDecisionVariableMutator,
    ):
        super().__init__(decision_variable_mutation_rate_determinator, decision_variable_mutator)

    def _mutate_candidate_solution(self):
        if self.number_of_mutation_decision_variables < 1:
            self.number_of_mutation_decision_variables = 1
        decision_variables_to_mutate = list(self.candidate_solution)
        random.shuffle(decision_variables_to_mutate)
        number_of_mutation_decision_variables = (
            self._decision_variable_mutation_rate_determinator.get_number_of_mutation_decision_variables(
                self.candidate_solution, self.number_of_mutation_decision_variables
            )
        )
        if number_of_mutation_decision_variables < 1:
            number_of_mutation_decision_variables = 1
        var_num = random.randint(1, number_of_mutation_decision_variables)
        for g in decision_variables_to_mutate[:var_num]:
            self._mutate_decision_variable(g)

        return var_num
