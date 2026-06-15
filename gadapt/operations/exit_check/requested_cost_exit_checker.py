from typing import Callable

from gadapt.operations.exit_check.base_exit_checker import BaseExitChecker


class RequestedCostExitChecker(BaseExitChecker):
    """
    Exit check based on requested cost.
    The GA exits when the minimum cost reaches a defined value.
    """

    def __init__(self, requested_cost: float, max_attempt_no_for_step_decrease: int | None, number_of_generations: int = -1, exit_function: Callable = None) -> None:
        if max_attempt_no_for_step_decrease is None:
            max_attempt_no_for_step_decrease = 3
        super().__init__(1, max_attempt_no_for_step_decrease, -1, exit_function)
        self.requested_cost = requested_cost
        self.number_of_generations = number_of_generations

    def _is_exit(self):
        if self.population.min_cost <= self.requested_cost:
            return True
        return False

    def _should_decrease_step(self):
        return self._min_step_stuck()
