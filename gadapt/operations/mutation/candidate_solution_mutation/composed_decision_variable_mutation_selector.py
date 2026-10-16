import random
from typing import List

from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_rate_determinator import (
    BaseDecisionVariableMutationRateDeterminator,
)
from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_selector import (
    BaseDecisionVariableMutationSelector,
)
from gadapt.operations.mutation.decision_variable_mutation.base_decision_variable_mutator import BaseDecisionVariableMutator


class ComposedDecisionVariableMutationSelector(BaseDecisionVariableMutationSelector):
    """
    Allows for the composition of multiple mutation selectors and applies them sequentially to the candidate solution.
    """

    def __init__(
        self,
        decision_variable_mutation_rate_determinator: BaseDecisionVariableMutationRateDeterminator,
        decision_variable_mutator: BaseDecisionVariableMutator,
    ) -> None:
        super().__init__(decision_variable_mutation_rate_determinator, decision_variable_mutator)
        self.selectors: List[BaseDecisionVariableMutationSelector] = []

    def append(self, selector: BaseDecisionVariableMutationSelector):
        """
        Appends mutation selectors to a list of selectors.
        Args:
            selector: An instance of the BaseDecisionVariableMutationSelector class that will be added to the list of selectors.
        """
        self.selectors.append(selector)

    def _mutate_candidate_solution(self):
        if self.candidate_solution is None:
            raise Exception("Candidate solution must not be null")
        if len(self.selectors) == 0:
            raise Exception("at least one selector must be added")
        if len(self.selectors) > 1:
            random.shuffle(self.selectors)
        nmg = 0
        number_of_mutation_decision_variables = (
            self._decision_variable_mutation_rate_determinator.get_number_of_mutation_decision_variables(
                self.candidate_solution, self.number_of_mutation_decision_variables
            )
        )
        if number_of_mutation_decision_variables == 0:
            number_of_mutation_decision_variables = 1
        for s in self.selectors:
            if nmg < number_of_mutation_decision_variables:
                s.number_of_mutation_decision_variables = number_of_mutation_decision_variables - nmg
                s.candidate_solution = self.candidate_solution
                mg = s._mutate_candidate_solution()
                nmg += mg
        return nmg
