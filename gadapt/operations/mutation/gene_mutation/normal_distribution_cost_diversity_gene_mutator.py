import math
from typing import Callable

import numpy as np

from gadapt.adapters.ga_logging.logging_settings import gadapt_log_error
from gadapt.operations.mutation.gene_mutation.normal_distribution_gene_mutator import (
    NormalDistributionGeneMutator,
)


class NormalDistributionCostDiversityGeneMutator(NormalDistributionGeneMutator):
    """
    Generates random or normally distributed values. Calculates standard deviation based on
    the cross-diversity coefficient
    """

    def __init__(self, get_cost_diversity_function: Callable,  min_std_dev: float = 0.001, max_std_dev: float = 0.6):
        super().__init__(min_std_dev, max_std_dev)
        self.get_cost_diversity_function = get_cost_diversity_function


    def _calculate_normal_distribution_standard_deviation(self):
        cost_diversity_coefficient_fun = self.get_cost_diversity_function()
        if cost_diversity_coefficient_fun is None:
            return 0.01
        cost_diversity_coefficient = cost_diversity_coefficient_fun()
        if cost_diversity_coefficient is None or math.isnan(
            cost_diversity_coefficient
        ):
            gadapt_log_error("cost_diversity_coefficient not set!")
            return 0.01
        min_std_dev = self.min_std_dev
        max_std_dev = self.max_std_dev
        std_dev_range = max_std_dev - min_std_dev
        dv_rsd = np.clip(cost_diversity_coefficient, 0, 1)
        return min_std_dev + (std_dev_range * dv_rsd)
