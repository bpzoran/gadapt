import random
from typing import List

from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_rate_determinator import (
    BaseDecisionVariableMutationRateDeterminator,
)


class ComposedDecisionVariableMutationRateDeterminator(BaseDecisionVariableMutationRateDeterminator):
    """
    Provides a way to combine multiple decision variable mutation rate determinators into a single determinator. It randomly selects one of the determinators to determine the number of mutation decision variables in a candidate solution.
    """

    def __init__(self) -> None:
        super().__init__()
        self.determinators: List[BaseDecisionVariableMutationRateDeterminator] = []

    def append(self, determinator: BaseDecisionVariableMutationRateDeterminator):
        """
        Adds a decision variable mutation rate determinator to the list of determinators.
        Args:
            determinator: A BaseDecisionVariableMutationRateDeterminator object representing a decision variable mutation rate determinator.
        """
        self.determinators.append(determinator)

    def _get_number_of_mutation_decision_variables(self):
        if self.candidate_solution is None:
            raise Exception("Candidate solution must not be null")
        if len(self.determinators) == 0:
            raise Exception("at least one determinator must be added")
        for determinator in self.determinators:
            determinator.candidate_solution = self.candidate_solution
            determinator.max_number_of_mutation_decision_variables = (
                self.max_number_of_mutation_decision_variables
            )
        if len(self.determinators) > 1:
            random.shuffle(self.determinators)
        current_determinator = self.determinators[0]
        return current_determinator._get_number_of_mutation_decision_variables()
