from typing import List, Tuple
from gadapt.ga_model.chromosome import Chromosome
import gadapt.ga_model.definitions as definitions

class BaseParentSelector:    
    """
    Base Parent Selector

    Selects mates for mating from the population
    """
    def select_mates(self, population) -> List[Tuple[Chromosome, Chromosome]]:
        """
        Selects and returns mates for the crossover from the population
        Args:
            population: the population for the mates selection
        """
        return self._select_mates_from_population(population)
    
    def _select_mates_from_population(self, population) -> List[Tuple[Chromosome, Chromosome]]:
        raise Exception(definitions.NOT_IMPLEMENTED)