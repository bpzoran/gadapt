import sys
import traceback
from typing import List
from gadapt.ga_model.chromosome import Chromosome
import gadapt.ga_model.definitions as definitions

class BaseCostFinder:
    """
    Base class for cost finding
    """
    def _execute_function(self, cost_function, c: Chromosome):
        """
        Executes the cost function
        
        Args:
            cost_function: Function to execute
            c (Chromosome): The chromosome with genes containing values for the function execution.
        """
        dict = {}
        for g in c:
            dict[g.genetic_variable.variable_id] = g.variable_value
        try:
            cost_value = cost_function(dict)
            c.cost_value = cost_value
        except Exception:
            print(Exception)
            traceback.print_exc()
            c.succ = False
            c.cost_value = sys.float_info.max

    def _find_costs_for_population(self, population):
        raise Exception(definitions.NOT_IMPLEMENTED)
    
    def find_costs(self, population):
        """
        Finds costs for the population
        
        Args:
            population (Population): The population to find costs for each chromosome
        """
        self._find_costs_for_population(population)