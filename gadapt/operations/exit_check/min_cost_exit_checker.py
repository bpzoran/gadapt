from gadapt.operations.exit_check.base_exit_checker import BaseExitChecker


class MinCostExitChecker(BaseExitChecker):
    """
    Exit check based on minimal cost.
    The GA exits when there is no improvement in the minimal cost in a
    defined number of iterations.
    """

    def _is_exit(self):
        if self.population is None:
            raise Exception("population must not be null")
        return self._min_step_stuck() or self._number_of_generations_stuck()

    def _should_decrease_step(self) -> bool:
        return  self._is_exit()
