from abc import ABC, abstractmethod


class BasePopulationUpdater(ABC):
    """
    Base class for population update
    """

    @abstractmethod
    def update_population(self, population):
        pass
