from math import isnan

import gadapt.utils.ga_utils as ga_utils
from gadapt.adapters.ga_logging.logging_settings import gadapt_log_error
from gadapt.operations.mutation.chromosome_mutation.random_gene_mutation_rate_determinator import (
    RandomGeneMutationRateDeterminator,
)


class CrossDiversityGeneMutationRateDeterminator(RandomGeneMutationRateDeterminator):
    """
    Determines the number of mutation alleles in a chromosome based on the cross diversity coefficient of the gene.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def _get_mutation_rate(self, genes) -> float:
        avg_rsd = ga_utils.average([g.columnar_diversity_coefficient for g in genes])
        if avg_rsd > 1:
            avg_rsd = 1
        if avg_rsd < 0:
            avg_rsd = 0
        return avg_rsd

    def _get_number_of_mutation_genes(self) -> int:
        genes = [g.gene for g in self.chromosome]
        if any(
                g.columnar_diversity_coefficient is None
                or isnan(g.columnar_diversity_coefficient)
            for g in genes
        ):
            gadapt_log_error("cross_diversity_coefficient not set!")
            return super()._get_number_of_mutation_genes()

        mutation_rate = self._get_mutation_rate(genes)
        limit_number_of_mutation_genes = mutation_rate * float(
            len(genes)
        )
        limit_number_of_mutation_genes_rounded = round(limit_number_of_mutation_genes)
        preferred_number_of_mutation_genes =  round(len(self.chromosome) / 5)
        if limit_number_of_mutation_genes_rounded < preferred_number_of_mutation_genes:
            limit_number_of_mutation_genes_rounded = max(preferred_number_of_mutation_genes, 1)
        self.max_number_of_mutation_genes = limit_number_of_mutation_genes_rounded
        return super()._get_number_of_mutation_genes()
