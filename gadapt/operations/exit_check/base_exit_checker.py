from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Callable

from gadapt.adapters.ga_logging.logging_settings import gadapt_log_info
from gadapt.ga_model.population import Population


class BaseExitChecker(ABC):
    """
    Base class for exit check
    Args:
        max_attempt_no (int): Maximal number of attempts with no improvement,
        for the given criteria.

            After this number of attempts with no improvements, the GA exits
    """

    def __init__(self, max_attempt_no: int, number_of_generations: int = -1, exit_function: Callable = None) -> None:
        self.max_attempt_no = max_attempt_no
        self.exit_function = exit_function
        self.attempt_no = 0
        self.population: Optional[Population] = None
        m_a_n = max_attempt_no - 1
        if m_a_n < 1:
            m_a_n = 0
        self.number_of_generations = number_of_generations - m_a_n

    @property
    def attempt_no(self) -> int:
        return self._attempt_no

    @attempt_no.setter
    def attempt_no(self, value: int):
        self._attempt_no = value

    def check(self, population: Population):
        if self.exit_function is not None and self.exit_function():
            gadapt_log_info("Exit function returned True, exiting.")
            return True

        self.population = population
        if self.population is None:
            raise Exception("Population is None!")
        if self.population is None:
            raise Exception("Population is None!")
        time_diff = (datetime.now() - self.population.start_time).total_seconds()
        if time_diff >= self.population.options.timeout:
            self.population.timeout_expired = True
            return True
        if self._is_exit():
            self.attempt_no += 1
        else:
            self.attempt_no = 0
        if self.attempt_no >= self.max_attempt_no:
            gadapt_log_info("function exit.")
            return True
        return False

    @abstractmethod
    def _is_exit(self) -> bool:
        pass

    def _min_step_stuck(self) -> bool:
        return self.population.min_cost >= self.population.previous_min_cost

    def _avg_step_stuck(self) -> bool:
        return self.population.avg_cost >= self.population.previous_avg_cost

    def _number_of_generations_stuck(self) -> bool:
        return 0 < self.number_of_generations <= self.population.population_generation
