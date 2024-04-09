import random

from operations.mutation.chromosome_mutation.base_gene_mutation_rate_determinator import \
    BaseGeneMutationRateDeterminator


class RandomGeneMutationRateDeterminator(BaseGeneMutationRateDeterminator):
    """
    Population mutator based on cross diversity
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def _get_number_of_mutation_genes(
            self, chromosome, max_number_of_mutation_genes
    ) -> int:
        return random.randint(1, max_number_of_mutation_genes)
