import random
from typing import List

from gadapt.operations.mutation.decision_variable_mutation.base_decision_variable_mutator import BaseDecisionVariableMutator


class ComposedDecisionVariableMutator(BaseDecisionVariableMutator):
    def __init__(self) -> None:
        super().__init__()
        self.mutators: List[BaseDecisionVariableMutator] = []

    def append(self, mutator: BaseDecisionVariableMutator):
        """
        Appends decision variable mutator to a list of mutators.
        Args:
            mutator: An instance of the BaseDecisionVariableMutator class that will be added to the list of mutator.
        """
        self.mutators.append(mutator)

    def _make_mutated_value(self):
        if self.variable_value is None:
            raise Exception("Variable value must not be null")
        if len(self.mutators) == 0:
            raise Exception("at least one mutator must be added")
        for mutator in self.mutators:
            mutator.variable_value = self.variable_value
        if len(self.mutators) > 1:
            random.shuffle(self.mutators)
        return self.mutators[0]._make_mutated_value()
