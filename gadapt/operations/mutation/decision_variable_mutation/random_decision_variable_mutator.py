import sys

from gadapt.operations.mutation.decision_variable_mutation.base_decision_variable_mutator import BaseDecisionVariableMutator


class RandomDecisionVariableMutator(BaseDecisionVariableMutator):
    """
    Generates a random value within the specified range of the decision variable.
    """

    def _make_mutated_value(self):
        if ((self.variable_value.decision_variable.decimal_places is not None) and (self.variable_value.decision_variable.decimal_places > -1)) and 0 < self.variable_value.decision_variable.decimal_places < 308:
            return round(
                self.variable_value.decision_variable.make_random_value(),
                self.variable_value.decision_variable.decimal_places,
            )
        else:
            return self.variable_value.decision_variable.make_random_value()
