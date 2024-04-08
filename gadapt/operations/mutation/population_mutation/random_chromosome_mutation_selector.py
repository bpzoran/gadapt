from gadapt.operations.mutation.population_mutation.base_chromosome_mutation_rate_determinator import (
    BaseChromosomeMutationRateDeterminator,
)
from operations.mutation.population_mutation.base_chromosome_mutation_selector import BaseChromosomeMutationSelector


class RandomChromosomeMutationSelector(BaseChromosomeMutationSelector):
    """
    Random population mutator
    """

    def __init__(self, chromosome_mutation_rate_determinator: BaseChromosomeMutationRateDeterminator) -> None:
        super().__init__(chromosome_mutation_rate_determinator)

    def _mutate_population(self, population, max_number_of_mutation_chromosomes):
        if population is None:
            raise Exception("population must not be None")
        number_of_mutation_genes = population.options.number_of_mutation_genes
        unallocated_chromosomes = self._get_unallocated_chromosomes(
            population, self._sort_key_random
        )
        mutation_chromosome_number = self._chromosome_mutation_rate_determinator.get_number_of_mutation_chromosomes(
            population, max_number_of_mutation_chromosomes)
        chromosomes_for_mutation = unallocated_chromosomes[
                                   :mutation_chromosome_number
                                   ]
        for c in chromosomes_for_mutation:
            c.mutate(number_of_mutation_genes)
        return mutation_chromosome_number
