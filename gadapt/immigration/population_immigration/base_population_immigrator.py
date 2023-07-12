import gadapt.ga_model.definitions as definitions
class BasePopulationImmigrator:

    """
    Base class for population immigration
    """

    def immigrate(self, population):
        """
        Immigrates chromosomes into the population
        Args:
            population: Population to immigrate new chromosomes
        """
        self._immigrate_population(population)
    
    def _immigrate_population(self, population):
        raise Exception(definitions.NOT_IMPLEMENTED)