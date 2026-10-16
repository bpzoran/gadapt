import random

from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.operations.mutation.population_mutation.parent_diversity_candidate_solution_mutation_selector import \
    ParentDiversityCandidateSolutionMutationSelector


class ParentStructuralDiversityCandidateSolutionMutationSelector(ParentDiversityCandidateSolutionMutationSelector):
    """
    Selects and mutates candidate solutions in a population based on their parent structural diversity.
    """

    def _get_diversity_coefficient(self, candidate_solution):
        """Returns the structural diversity coefficient for a given candidate solution."""
        return candidate_solution.parent_structural_diversity_coefficient

    def _sort_key_parent_diversity(self, c: CandidateSolution):
        return c.parent_structural_diversity_coefficient, random.random()
