from gadapt.operations.mutation.population_mutation.base_chromosome_mutation_rate_determinator import (
    BaseChromosomeMutationRateDeterminator,
)
from gadapt.operations.mutation.population_mutation.base_chromosome_mutation_selector import (
    BaseChromosomeMutationSelector,
)


class RandomChromosomeMutationSelector(BaseChromosomeMutationSelector):
    """
    Implements the mutation of chromosomes in a population based on a random selection of chromosomes
    """

    def __init__(
        self,
        chromosome_mutation_rate_determinator: BaseChromosomeMutationRateDeterminator,
    ) -> None:
        super().__init__(chromosome_mutation_rate_determinator)

    def _mutate_population(self):
        if self.population is None:
            raise Exception("population must not be None")
        number_of_mutation_genes = self.population.options.number_of_mutation_genes
        unallocated_chromosomes = self._get_unallocated_chromosomes(
            self._sort_key_random
        )
        mutation_chromosome_number = self.number_of_mutation_chromosomes
        if mutation_chromosome_number == 0:
            return 0
        chromosomes_for_mutation = unallocated_chromosomes[:mutation_chromosome_number]
        for c in chromosomes_for_mutation:
            c.mutate(number_of_mutation_genes)
        return mutation_chromosome_number
