import random
from typing import List

from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_rate_determinator import (
    BaseCandidateSolutionMutationRateDeterminator,
)
from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_selector import (
    BaseCandidateSolutionMutationSelector,
)
from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_selector import (
    BaseDecisionVariableMutationSelector,
)


class ComposedCandidateSolutionMutationSelector(BaseCandidateSolutionMutationSelector):
    def __init__(
        self,
        candidate_solution_mutation_rate_determinator: BaseCandidateSolutionMutationRateDeterminator,
        decision_variable_mutation_selector: BaseDecisionVariableMutationSelector,
    ) -> None:
        super().__init__(candidate_solution_mutation_rate_determinator, decision_variable_mutation_selector)
        self.selectors: List[BaseCandidateSolutionMutationSelector] = []

    def append(self, selector: BaseCandidateSolutionMutationSelector):
        """
        Appends selector to the composition of selectors
        """
        self.selectors.append(selector)

    def _get_candidate_solutions_for_mutation(self):
        if self.population is None:
            raise Exception("Population must not be null")
        if len(self.selectors) == 0:
            raise Exception("at least one selector must be added")
        if len(self.selectors) > 1:
            random.shuffle(self.selectors)
        limit_number_of_mutation_candidate_solutions = self.number_of_mutation_candidate_solutions
        if limit_number_of_mutation_candidate_solutions == 0:
            return []
        candidate_solutions_for_mutation = []
        # Nothing is mutated until all selectors have been asked, so two selectors can pick the same
        # candidate solution. It is taken once, so that it is counted and mutated once.
        selected_ids = set()
        for m in self.selectors:
            if len(candidate_solutions_for_mutation) >= limit_number_of_mutation_candidate_solutions:
                break
            m.population = self.population
            m.number_of_mutation_candidate_solutions = (
                limit_number_of_mutation_candidate_solutions - len(candidate_solutions_for_mutation)
            )
            for c in m._get_candidate_solutions_for_mutation():
                if id(c) not in selected_ids:
                    selected_ids.add(id(c))
                    candidate_solutions_for_mutation.append(c)
        return candidate_solutions_for_mutation
