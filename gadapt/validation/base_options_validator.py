from abc import ABC, abstractmethod
from typing import List, Tuple
import gadapt.ga_model.message_levels as message_levels
import gadapt.ga_model.definitions as definitions

class BaseOptionsValidator(ABC):


    def __init__(self, options) -> None:
        """
        Base class for options validation
        Args:
            options: Options to validate
        """
        self._validation_messages = []
        self.options = options
        self.success = True
    
    def validate(self) -> bool:
        """
        Validates options
        """
        self._validate_options()
    
    @abstractmethod
    def _validate_options(self) -> bool:
        pass
    
    @property
    def validation_messages(self):
        """
        Returns validation messages
        """
        return self._validation_messages

    def _add_message(self, message, message_level = message_levels.ERROR):
        self.validation_messages.append((message_level, message))
    
