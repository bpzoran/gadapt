import math
import random
from typing import List
from gadapt.ga_model.chromosome import Chromosome
from gadapt.ga_model.ga_options import GAOptions
import gadapt.ga_model.definitions as definitions
class BasePopulationMutator:    

    def mutate(self, population):
        """
        Mutates chromosomes in the population
        Args:
            population: Population to mutate
        """
        number_of_mutated_chromosomes = population.options.number_of_mutation_chromosomes  
        self._mutate_population(population, number_of_mutated_chromosomes)
    
    def __init__(self, options: GAOptions) -> None:
        """
        Base class for mutating chromosomes in population
        Args:
            options: genetic algorithm options
        """
        self.options = options     

    def _mutate_population(self, population, number_of_mutated_chromosomes):
        raise Exception(definitions.NOT_IMPLEMENTED)
    
    def _get_unallocated_chromosomes(self, population, sort_key_function = None) -> List[Chromosome]:
        def unallocated_chromosomes_condition(c: Chromosome) -> bool:
            return math.isnan(c.cost_value) and (not c.is_immigrant) and c.population_generation == population.population_generation and not c.is_mutated
        lst = [c for c in population if (unallocated_chromosomes_condition(c))]
        if not sort_key_function is None:
            lst.sort(key=sort_key_function)
        return lst
    
    def _sort_key_random(self, c: Chromosome):
        return random.random()