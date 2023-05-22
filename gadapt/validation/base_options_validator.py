from typing import List, Tuple
import ga_model.message_levels
import ga_model.definitions

class BaseOptionsValidator:
    
    def __init__(self, options) -> None:
        self._validation_messages = []
        self.options = options
        self.success = True
    
    def validate(self) -> bool:
        raise Exception(ga_model.definitions.NOT_IMPLEMENTED)
    
    @property
    def validation_messages(self):
        return self._validation_messages
    
    @validation_messages.setter
    def validation_messages(self, value):
        self._validation_messages = value

    def add_message(self, message, message_level = ga_model.message_levels.ERROR):
        self.validation_messages.append((message_level, message))
    
