import gadapt.utils.ga_utils as ga_utils
import statistics as stat

from operations.mutation.chromosome_mutation.base_gene_mutation_rate_determinator import \
    BaseGeneMutationRateDeterminator


class CrossDiversityGeneMutationRateDeterminator(BaseGeneMutationRateDeterminator):
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
        decision_variables = [g.decision_variable for g in chromosome]

        def get_mutation_rate() -> float:
            avg_rsd = ga_utils.average([dv.cross_diversity_coefficient for dv in decision_variables])
            if avg_rsd > 1:
                avg_rsd = 1
            if avg_rsd < 0:
                avg_rsd = 0
            return 1 - avg_rsd

        mutation_rate = get_mutation_rate()
        f_return_value = mutation_rate * float(self.max_number_of_mutation_genes)
        return round(f_return_value)
