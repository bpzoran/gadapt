import math
import random
import sys

from gadapt.utils.ga_utils import (
    normally_distributed_random,
)
from gadapt.operations.mutation.decision_variable_mutation.base_decision_variable_mutator import BaseDecisionVariableMutator


class NormalDistributionDecisionVariableMutator(BaseDecisionVariableMutator):
    """
    Generates random or normally distributed values.
    """
    def __init__(self, min_std_dev: float = 0.001, max_std_dev: float = 0.6):
        if min_std_dev < 0.0 or max_std_dev < 0.0 or  max_std_dev > 1.0 or min_std_dev > 1.0 or max_std_dev <= min_std_dev:
            self.min_std_dev = 0.001
            self.max_std_dev = 0.6
            return
        self.min_std_dev = min_std_dev
        self.max_std_dev = max_std_dev

    def _make_mutated_value(self):
        return self._make_normally_distributed_random_value_until_changed()

    def _make_normally_distributed_random_value_until_changed(self):
        return self._execute_function_until_value_changed(
            self._make_normally_distributed_random_value
        )

    def _calculate_normal_distribution_standard_deviation(self):
        return 0.05

    def _make_normally_distributed_random_value(self):
        curr_value = self.variable_value.value
        if math.isnan(curr_value):
            curr_value = self.variable_value.decision_variable.make_random_value()

        decision_variable = self.variable_value.decision_variable
        decision_variable_range = decision_variable.max_value - decision_variable.min_value

        # mean normalized to [0,1]
        mean = (curr_value - decision_variable.min_value) / decision_variable_range
        std = self._calculate_normal_distribution_standard_deviation()
        normal_distribution_random_value = normally_distributed_random(mean, std, 0, 1)

        # Determine effective step: treat as continuous if step is None, <= 0, or too small relative to range
        if decision_variable.step is not None and decision_variable.step > 0 and not math.isnan(decision_variable.step) and decision_variable_range / decision_variable.step <= 1e9:
            effective_step = decision_variable.step
        else:
            effective_step = None

        if effective_step is not None:
            # --- Discrete case (snap to step multiples) ---
            number_of_steps = round(
                (normal_distribution_random_value * decision_variable_range) / effective_step
            )
            value = decision_variable.min_value + number_of_steps * effective_step

            # If snapping produced the same value, nudge by ±1 step
            if value == curr_value:
                direction = random.choice([-1, 1])
                value = value + direction * effective_step
                # If nudge goes out of bounds, try the other direction
                if value < decision_variable.min_value or value > decision_variable.max_value:
                    value = curr_value - direction * effective_step
                # Final clamp for safety
                value = max(decision_variable.min_value, min(value, decision_variable.max_value))

        else:
            # --- Continuous case (no step) ---
            value = decision_variable.min_value + normal_distribution_random_value * decision_variable_range

        return value
