import random

from gadapt.ga_model.chromosome import Chromosome
from gadapt.operations.mutation.population_mutation.parent_diversity_chromosome_mutation_selector import \
    ParentDiversityChromosomeMutationSelector


class ParentCostDiversityChromosomeMutationSelector(ParentDiversityChromosomeMutationSelector):
    """
    Selects and mutates chromosomes in a population based on their parent structural diversity.
    """

    def _get_diversity_coefficient(self, chromosome):
        """Returns the structural diversity coefficient for a given chromosome."""
        return chromosome.parent_cost_diversity_coefficient

    def _sort_key_parent_diversity(self, c: Chromosome):
        return c.parent_cost_diversity_coefficient, random.random()
