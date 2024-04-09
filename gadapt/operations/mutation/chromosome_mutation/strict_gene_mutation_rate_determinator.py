import math
from gadapt.ga_model.chromosome import Chromosome
from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_rate_determinator import (
    BaseGeneMutationRateDeterminator,
)
import gadapt.utils.ga_utils as ga_utils
import statistics as stat


class StrictGeneMutationRateDeterminator(BaseGeneMutationRateDeterminator):
    """
    Chromosome mutator based on cross diversity
    """

    def __init__(
        self
    ) -> None:
        super().__init__()

    def _get_number_of_mutation_genes(
        self, chromosome: Chromosome, max_number_of_mutation_genes
    ) -> int:
        return max_number_of_mutation_genes
