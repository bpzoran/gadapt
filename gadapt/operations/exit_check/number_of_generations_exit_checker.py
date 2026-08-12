from typing import Callable

from gadapt.operations.exit_check.base_exit_checker import BaseExitChecker


class NumberOfGenerationsExitChecker(BaseExitChecker):
    """
    Exit check based on the number of generations.
    The GA exits when the defined number of generations is reached.
    """

    def __init__(self, number_of_generations: int, max_attempt_no_for_step_decrease: int | None, exit_function: Callable = None) -> None:
        if max_attempt_no_for_step_decrease is None:
            max_attempt_no_for_step_decrease = 3
        if number_of_generations <= 0:
            number_of_generations = 200
        super().__init__(1, max_attempt_no_for_step_decrease, number_of_generations, exit_function)

    def _is_exit(self):
        return self._number_of_generations_stuck()

    def _should_decrease_step(self):
        for g in self.population.options.genes:
            if g.min_step_target is not None:
                continue
            g.min_step_target = 100000000
        return self._min_step_stuck()
