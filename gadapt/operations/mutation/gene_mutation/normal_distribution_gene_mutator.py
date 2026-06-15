import math
import random
import sys

from gadapt.utils.ga_utils import (
    normally_distributed_random,
)
from gadapt.operations.mutation.gene_mutation.base_gene_mutator import BaseGeneMutator


class NormalDistributionGeneMutator(BaseGeneMutator):
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
        curr_value = self.gene_value.variable_value
        if math.isnan(curr_value):
            curr_value = self.gene_value.gene.make_random_value()

        gene = self.gene_value.gene
        gene_range = gene.max_value - gene.min_value

        # mean normalized to [0,1]
        mean = (curr_value - gene.min_value) / gene_range
        std = self._calculate_normal_distribution_standard_deviation()
        normal_distribution_random_value = normally_distributed_random(mean, std, 0, 1)

        # Determine effective step: treat as continuous if step is None, <= 0, or too small relative to range
        if gene.step is not None and gene.step > 0 and not math.isnan(gene.step) and gene_range / gene.step <= 1e9:
            effective_step = gene.step
        else:
            effective_step = None

        if effective_step is not None:
            # --- Discrete case (snap to step multiples) ---
            number_of_steps = round(
                (normal_distribution_random_value * gene_range) / effective_step
            )
            value = gene.min_value + number_of_steps * effective_step

            # If snapping produced the same value, nudge by ±1 step
            if value == curr_value:
                direction = random.choice([-1, 1])
                value = value + direction * effective_step
                # If nudge goes out of bounds, try the other direction
                if value < gene.min_value or value > gene.max_value:
                    value = curr_value - direction * effective_step
                # Final clamp for safety
                value = max(gene.min_value, min(value, gene.max_value))

        else:
            # --- Continuous case (no step) ---
            value = gene.min_value + normal_distribution_random_value * gene_range

        return value
