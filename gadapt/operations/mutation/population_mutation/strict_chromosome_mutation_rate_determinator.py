import math
from gadapt.ga_model.population import Population
from gadapt.operations.mutation.population_mutation.base_chromosome_mutation_rate_determinator import (
    BaseChromosomeMutationRateDeterminator,
)
import gadapt.utils.ga_utils as ga_utils
import statistics as stat


class StrictChromosomeMutationRateDeterminator(BaseChromosomeMutationRateDeterminator):
    """
    Population mutator based on cross diversity
    """

    def __init__(
        self
    ) -> None:
        super().__init__()

    def _get_number_of_mutation_chromosomes(
        self, population: Population, max_number_of_mutation_chromosomes
    ) -> int:
        return max_number_of_mutation_chromosomes