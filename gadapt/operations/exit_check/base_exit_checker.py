import logging
from abc import ABC, abstractmethod
from datetime import datetime


class BaseExitChecker(ABC):
    """
    Base class for exit check
    Args:
        max_attempt_no (int): Maximal number of attempts with no improvement,
        for the given criteria.

            After this number of attempts with no improvements, the GA exits
    """

    def __init__(self, max_attempt_no: int) -> None:
        self.max_attempt_no = max_attempt_no
        self.attempt_no = 0
        self.population = None

    @property
    def attempt_no(self) -> int:
        return self._attempt_no

    @attempt_no.setter
    def attempt_no(self, value: int):
        self._attempt_no = value

    def check(self, population):
        self.population = population
        time_diff = (datetime.now() - self.population.start_time).total_seconds()
        if time_diff >= self.population.options.timeout:
            self.population.timeout_expired = True
            return True
        if self._is_exit():
            self.attempt_no += 1
        else:
            self.attempt_no = 0
        if self.attempt_no >= self.max_attempt_no:
            logging.info("function exit.")
            return True
        return False

    @abstractmethod
    def _is_exit(self) -> bool:
        pass
