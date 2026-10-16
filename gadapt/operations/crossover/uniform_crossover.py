import random
from typing import Tuple

from gadapt.operations.crossover.base_crossover import BaseCrossover
from gadapt.operations.candidate_solution_update.base_candidate_solution_updater import (
    BaseCandidateSolutionUpdater,
)
from gadapt.operations.crossover.base_crossover_probability_determinator import BaseCrossoverProbabilityDeterminator
from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_selector import BaseDecisionVariableMutationSelector


class UniformCrossover(BaseCrossover):
    """
    Uniform Crossover. Decision variables from parents' candidate solutions are combined in a uniform way.
    """

    def __init__(self, candidate_solution_updater: BaseCandidateSolutionUpdater, mutator: BaseDecisionVariableMutationSelector, crossover_rate_determinator: BaseCrossoverProbabilityDeterminator):
        super(UniformCrossover, self).__init__(candidate_solution_updater, mutator, crossover_rate_determinator)

    def _combine(self) -> Tuple[float, float]:
        rnd = random.randint(0, 2)
        if rnd == 0:
            return self._father_variable_value.value, self._mother_variable_value.value
        elif rnd == 1:
            return self._father_variable_value.value, self._father_variable_value.value
        else:
            return self._mother_variable_value.value, self._mother_variable_value.value
