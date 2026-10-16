import math

import numpy as np

from gadapt.adapters.ga_logging.logging_settings import gadapt_log_error
from gadapt.operations.mutation.decision_variable_mutation.normal_distribution_decision_variable_mutator import (
    NormalDistributionDecisionVariableMutator,
)


class NormalDistributionVariableColumnarDiversityDecisionVariableMutator(NormalDistributionDecisionVariableMutator):
    """
    Generates random or normally distributed values. Calculates standard deviation based on
    the variable-columnar-diversity coefficient
    """

    def _calculate_normal_distribution_standard_deviation(self):
        if self.variable_value.decision_variable.columnar_diversity_coefficient is None or math.isnan(
            self.variable_value.decision_variable.columnar_diversity_coefficient
        ):
            gadapt_log_error("variable_columnar_diversity_coefficient not set!")
            return 0.01
        min_std_dev = self.min_std_dev
        max_std_dev = self.max_std_dev
        std_dev_range = max_std_dev - min_std_dev
        dv_rsd = np.clip(self.variable_value.decision_variable.columnar_diversity_coefficient, 0, 1)
        return min_std_dev + (std_dev_range * dv_rsd)
