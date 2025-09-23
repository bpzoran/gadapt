import random
import sys

from gadapt.operations.crossover.base_crossover import BaseCrossover
from gadapt.operations.chromosome_update.base_chromosome_updater import (
    BaseChromosomeUpdater,
)


class BlendingCrossover(BaseCrossover):
    """
    Blending Crossover combines
    gene values from the two parents into new variable values in offsprings.
    One value of the offspring variable comes from a combination of the two
    corresponding values of the parental genes
    """

    def __init__(self, chromosome_updater: BaseChromosomeUpdater):
        super(BlendingCrossover, self).__init__(chromosome_updater)
        self._current_gene_number = -1

    def _combine(self):
        gene = self._father_allele.gene
        val_father = self._father_allele.variable_value
        val_mother = self._mother_allele.variable_value
        if hasattr(gene, "step") and gene.step is not None and gene.step > 0 and gene.step > sys.float_info.min:
            val1, val2 = self._combine_with_step(gene, val_father, val_mother)
        else:
            val1, val2 = self._combine_without_step(gene, val_father, val_mother)
        return val1, val2

    def _combine_with_step(self, gene, val_father, val_mother):
        x = 1
        if val_mother > val_father:
            x = -1
        beta_steps = random.randint(
            0, round(abs((val_father - val_mother) / gene.step))
        )
        val1 = round(
            val_father - (beta_steps * x) * gene.step,
            gene.decimal_places,
        )
        val2 = round(
            val_mother + (beta_steps * x) * gene.step,
            gene.decimal_places,
        )
        return val1, val2

    def _combine_without_step(self, gene, val_father, val_mother):
        # --- Continuous case (no step defined) ---
        alpha = random.random()  # uniform in [0,1]
        val1 = alpha * val_father + (1 - alpha) * val_mother
        # use a different alpha for second offspring
        alpha = random.random()
        val2 =alpha * val_mother + (1 - alpha) * val_father
        return val1, val2
