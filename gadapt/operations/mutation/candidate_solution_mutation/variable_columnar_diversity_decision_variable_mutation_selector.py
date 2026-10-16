import random

from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_rate_determinator import (
    BaseDecisionVariableMutationRateDeterminator,
)
from gadapt.operations.mutation.candidate_solution_mutation.random_decision_variable_mutation_selector import (
    RandomDecisionVariableMutationSelector,
)
from gadapt.operations.sampling.base_sampling import BaseSampling
from gadapt.operations.mutation.decision_variable_mutation.base_decision_variable_mutator import BaseDecisionVariableMutator


class VariableColumnarDiversityDecisionVariableMutationSelector(RandomDecisionVariableMutationSelector):
    """
    Selects and mutates a candidate solution based on the variable columnar diversity of decision variables in the population.
    """

    def __init__(
        self,
        decision_variable_mutation_rate_determinator: BaseDecisionVariableMutationRateDeterminator,
        decision_variable_mutator: BaseDecisionVariableMutator,
        sampling: BaseSampling,
    ) -> None:
        super().__init__(decision_variable_mutation_rate_determinator, decision_variable_mutator)
        self._sampling = sampling

    def _mutate_candidate_solution(self):
        if self.number_of_mutation_decision_variables == 0:
            self.number_of_mutation_decision_variables = 1
        x_decision_variables = [g for g in self.candidate_solution]
        x_decision_variables.sort(key=lambda g: -g.decision_variable.columnar_diversity_coefficient)
        number_of_mutation_decision_variables = (
            self._decision_variable_mutation_rate_determinator.get_number_of_mutation_decision_variables(
                self.candidate_solution, self.number_of_mutation_decision_variables
            )
        )
        if number_of_mutation_decision_variables > len(x_decision_variables):
            number_of_mutation_decision_variables = len(x_decision_variables)
        if number_of_mutation_decision_variables == 0:
            max_number_of_mutation_decision_variables = 1
        else:
            max_number_of_mutation_decision_variables = random.randint(1, number_of_mutation_decision_variables)
        decision_variables_for_mutation = self._sampling.get_sample(
            x_decision_variables,
            max_number_of_mutation_decision_variables,
            lambda g: g.decision_variable.columnar_diversity_coefficient,
        )
        for g in decision_variables_for_mutation:
            self._mutate_decision_variable(g)
        return len(decision_variables_for_mutation)
