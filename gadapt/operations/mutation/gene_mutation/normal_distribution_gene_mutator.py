import math
import sys

from gadapt.utils.ga_utils import (
    normally_distributed_random,
)
from gadapt.operations.mutation.gene_mutation.base_gene_mutator import BaseGeneMutator


class NormalDistributionGeneMutator(BaseGeneMutator):
    """
    Generates random or normally distributed values.
    """

    def _make_mutated_value(self):
        return self._make_normally_distributed_random_value_until_changed()

    def _make_normally_distributed_random_value_until_changed(self):
        return self._execute_function_until_value_changed(
            self._make_normally_distributed_random_value
        )

    def _calculate_normal_distribution_standard_deviation(self):
        return 0.05

    def _make_normally_distributed_random_value(self):
        curr_value = self.gene_value.variable_value
        if math.isnan(curr_value):
            curr_value = self.gene_value.gene.make_random_value()

        gene = self.gene_value.gene
        gene_range = gene.max_value - gene.min_value

        # mean normalized to [0,1]
        mean = (curr_value - gene.min_value) / gene_range
        std = self._calculate_normal_distribution_standard_deviation()

        # draw random value from truncated normal in [0,1]
        normal_distribution_random_value = normally_distributed_random(mean, std, 0, 1)

        if hasattr(gene, "step") and gene.step is not None and gene.step > 0 and gene.step > sys.float_info.min:
            # --- Discrete case (snap to step multiples) ---
            number_of_steps = round(
                (normal_distribution_random_value * gene_range) / gene.step
            )
            value = gene.min_value + number_of_steps * gene.step
        else:
            # --- Continuous case (no step) ---
            value = gene.min_value + normal_distribution_random_value * gene_range

        return value
