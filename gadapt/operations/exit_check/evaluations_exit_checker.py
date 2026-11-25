from typing import Callable

from gadapt.operations.exit_check.base_exit_checker import BaseExitChecker


class EvaluationsExitChecker(BaseExitChecker):
    """
    Exit check based on the number of cost function evaluations.
    The budget itself (max_evaluations) is checked in BaseExitChecker.check and enforced
    exactly by the cost finder, so this checker has no criterion of its own: the GA exits
    when the budget is used up (or on timeout / exit_function).
    The number of generations, if limited, is an additional upper limit.
    """

    def __init__(self, number_of_generations: int = -1, exit_function: Callable = None) -> None:
        super().__init__(1, number_of_generations, exit_function)

    def _is_exit(self) -> bool:
        return self._number_of_generations_stuck()
