import ga_model.definitions
class BaseVariableUpdater:
    def update_variables(self, population):
        raise Exception(ga_model.definitions.NOT_IMPLEMENTED)