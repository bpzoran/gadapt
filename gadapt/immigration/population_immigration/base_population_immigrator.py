import ga_model.definitions
class BasePopulationImmigrator:
    def immigrate(self, population):
        raise Exception(ga_model.definitions.NOT_IMPLEMENTED)