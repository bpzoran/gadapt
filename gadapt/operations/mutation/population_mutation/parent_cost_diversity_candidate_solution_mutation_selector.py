import random

from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.operations.mutation.population_mutation.parent_diversity_candidate_solution_mutation_selector import \
    ParentDiversityCandidateSolutionMutationSelector


class ParentCostDiversityCandidateSolutionMutationSelector(ParentDiversityCandidateSolutionMutationSelector):
    """
    Selects and mutates candidate solutions in a population based on the cost diversity of their parents.
    """

    def _get_diversity_coefficient(self, candidate_solution):
        """Returns the parent cost diversity coefficient for a given candidate solution."""
        return candidate_solution.parent_cost_diversity_coefficient

    def _sort_key_parent_diversity(self, c: CandidateSolution):
        return c.parent_cost_diversity_coefficient, random.random()
