import random
from abc import abstractmethod
from math import isnan

from gadapt.adapters.ga_logging.logging_settings import gadapt_log_error
from gadapt.ga_model.chromosome import Chromosome
from gadapt.operations.mutation.population_mutation.base_chromosome_mutation_rate_determinator import (
    BaseChromosomeMutationRateDeterminator,
)
from gadapt.operations.mutation.population_mutation.base_chromosome_mutation_selector import (
    BaseChromosomeMutationSelector,
)
from gadapt.operations.sampling.base_sampling import BaseSampling
from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_selector import (
    BaseGeneMutationSelector,
)


class ParentDiversityChromosomeMutationSelector(BaseChromosomeMutationSelector):
    """
    Selects and mutates chromosomes in a population based on their parent diversity.
    """

    def __init__(
        self,
        chromosome_mutation_rate_determinator: BaseChromosomeMutationRateDeterminator,
        gene_mutation_selector: BaseGeneMutationSelector,
        sampling: BaseSampling,
    ) -> None:
        super().__init__(chromosome_mutation_rate_determinator, gene_mutation_selector)
        self._sampling = sampling

    @abstractmethod
    def _sort_key_parent_diversity(self, c: Chromosome):
        pass

    @abstractmethod
    def _get_diversity_coefficient(self, chromosome):
        """Returns the diversity coefficient for a given chromosome."""
        pass

    def _get_chromosomes_for_mutation(self):
        if self.population is None:
            raise Exception("Population must not be null")
        unallocated_chromosomes: list[Chromosome] = self._get_unallocated_chromosomes(
            self._sort_key_parent_diversity
        )
        if any(isnan(c.parent_structural_diversity_coefficient) for c in unallocated_chromosomes):
            gadapt_log_error("parent_structural_diversity_coefficient not set!")
        chromosomes_for_mutation: list[Chromosome] = []
        if self.population.options.must_mutate_for_same_parents:
            chromosomes_for_mutation = [
                c
                for c in unallocated_chromosomes
                if c.parent_structural_diversity_coefficient == 0
            ]
        chromosomes_for_mutation_count = len(chromosomes_for_mutation)
        rest_number = (
            self.number_of_mutation_chromosomes - chromosomes_for_mutation_count
        )
        if rest_number > 0:
            if self.population.options.must_mutate_for_same_parents:
                other_chromosomes_for_mutation = [
                    c
                    for c in unallocated_chromosomes
                    if (not c.parent_structural_diversity_coefficient == 0)
                ]
            else:
                other_chromosomes_for_mutation = [c for c in unallocated_chromosomes]
            other_chromosomes_for_mutation = self._sampling.get_sample(
                other_chromosomes_for_mutation,
                rest_number,
                self._get_diversity_coefficient,
            )
            chromosomes_for_mutation.extend(other_chromosomes_for_mutation)
        return chromosomes_for_mutation
