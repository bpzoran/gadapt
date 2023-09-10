from abc import ABC, abstractmethod
import gadapt.ga_model.definitions as definitions
class BaseVariableUpdater(ABC):

    """
    Base class for variable update
    """

    @abstractmethod
    def update_variables(self, population):
        pass