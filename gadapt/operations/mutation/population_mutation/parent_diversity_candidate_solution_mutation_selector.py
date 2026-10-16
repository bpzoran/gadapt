import random
from abc import abstractmethod
from math import isnan

from gadapt.adapters.ga_logging.logging_settings import gadapt_log_error
from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_rate_determinator import (
    BaseCandidateSolutionMutationRateDeterminator,
)
from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_selector import (
    BaseCandidateSolutionMutationSelector,
)
from gadapt.operations.sampling.base_sampling import BaseSampling
from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_selector import (
    BaseDecisionVariableMutationSelector,
)


class ParentDiversityCandidateSolutionMutationSelector(BaseCandidateSolutionMutationSelector):
    """
    Selects and mutates candidate solutions in a population based on their parent diversity.
    """

    def __init__(
        self,
        candidate_solution_mutation_rate_determinator: BaseCandidateSolutionMutationRateDeterminator,
        decision_variable_mutation_selector: BaseDecisionVariableMutationSelector,
        sampling: BaseSampling,
    ) -> None:
        super().__init__(candidate_solution_mutation_rate_determinator, decision_variable_mutation_selector)
        self._sampling = sampling

    @abstractmethod
    def _sort_key_parent_diversity(self, c: CandidateSolution):
        pass

    @abstractmethod
    def _get_diversity_coefficient(self, candidate_solution):
        """Returns the diversity coefficient for a given candidate solution."""
        pass

    def _get_candidate_solutions_for_mutation(self):
        if self.population is None:
            raise Exception("Population must not be null")
        unallocated_candidate_solutions: list[CandidateSolution] = self._get_unallocated_candidate_solutions(
            self._sort_key_parent_diversity
        )
        if any(isnan(c.parent_structural_diversity_coefficient) for c in unallocated_candidate_solutions):
            gadapt_log_error("parent_structural_diversity_coefficient not set!")
        candidate_solutions_for_mutation: list[CandidateSolution] = []
        if self.population.options.must_mutate_for_same_parents:
            candidate_solutions_for_mutation = [
                c
                for c in unallocated_candidate_solutions
                if c.parent_structural_diversity_coefficient == 0
            ]
        candidate_solutions_for_mutation_count = len(candidate_solutions_for_mutation)
        rest_number = (
            self.number_of_mutation_candidate_solutions - candidate_solutions_for_mutation_count
        )
        if rest_number > 0:
            if self.population.options.must_mutate_for_same_parents:
                other_candidate_solutions_for_mutation = [
                    c
                    for c in unallocated_candidate_solutions
                    if (not c.parent_structural_diversity_coefficient == 0)
                ]
            else:
                other_candidate_solutions_for_mutation = [c for c in unallocated_candidate_solutions]
            other_candidate_solutions_for_mutation = self._sampling.get_sample(
                other_candidate_solutions_for_mutation,
                rest_number,
                self._get_diversity_coefficient,
            )
            candidate_solutions_for_mutation.extend(other_candidate_solutions_for_mutation)
        return candidate_solutions_for_mutation
