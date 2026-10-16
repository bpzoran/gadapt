"""
Variable value
"""

import math

import gadapt.adapters.string_operation.ga_strings as ga_strings
import gadapt.ga_model.definitions as definitions
from gadapt.ga_model.decision_variable import DecisionVariable
from gadapt.ga_model.ranking_model import RankingModel


class VariableValue(RankingModel):
    def __init__(self, decision_variable, value=None):
        """
        VariableValue class. A variable value is a part of a candidate solution.
        It contains the concrete value of a decision variable.
        Args:
            decision_variable: DecisionVariable which defines the variable value
            value: Variable value
        """
        super().__init__()
        self.decision_variable = decision_variable
        self.value = value
        self._rank = -1
        self._cummulative_probability = definitions.FLOAT_NAN
        if self.value is None or math.isnan(self.value):
            self.set_random_value()

    def __str__(self) -> str:
        return self._to_string()

    def _to_string(self):
        return ga_strings.variable_value_to_string(self)

    @property
    def decision_variable(self) -> DecisionVariable:
        """
        Decision variable which defines the variable value
        """
        return self._decision_variable

    @decision_variable.setter
    def decision_variable(self, value: DecisionVariable):
        if not isinstance(value, DecisionVariable):
            raise
        self._decision_variable = value

    @property
    def value(self):
        """
        Variable value
        """
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def set_random_value(self):
        """
        Sets a random value for the value property
        """
        self.value = self.decision_variable.make_random_value()
