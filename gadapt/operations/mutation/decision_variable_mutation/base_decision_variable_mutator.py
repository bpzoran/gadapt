from abc import ABC, abstractmethod

from gadapt.ga_model.variable_value import VariableValue


class BaseDecisionVariableMutator(ABC):
    """
    Mutates the variable value of a decision variable.
    """

    def mutate(self, variable_value: VariableValue):
        self.variable_value = variable_value
        self.variable_value.value = self._make_mutated_value()

    @abstractmethod
    def _make_mutated_value(self):
        pass

    def _execute_function_until_value_changed(self, f):
        current_variable_value = self.variable_value.value
        number_of_attempts = 5
        i = 0
        while True:
            new_variable_value = f()
            i += 1
            if new_variable_value != current_variable_value or i >= number_of_attempts:
                break
        return new_variable_value
