import sys
import traceback
from abc import ABC, abstractmethod
from typing import Optional

from gadapt.ga_model.population import Population
from gadapt.ga_model.chromosome import Chromosome


class BaseCostFinder(ABC):
    """
    Base class for cost finding
    """

    def __init__(self):
        super().__init__()
        self.population: Optional[Population] = None

    def _execute_function(self, cost_function, c: Chromosome):
        """
        Executes the cost function

        Args:
            cost_function: Function to execute
            c (Chromosome): The chromosome with
            genes containing values for the function execution.
        """
        alleles = list(sorted(c, key=lambda gn: gn.gene.variable_id))
        try:
            gene_values = [a.variable_value for a in alleles]
            c.cost_value = cost_function(gene_values)
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            c.succ = False
            c.cost_value = sys.float_info.max

    @abstractmethod
    def _find_costs_for_population(self):
        pass

    def find_costs(self, population):
        """
        Finds costs for the population

        Args:
            population (Population): The population to find costs for each chromosome
        """
        self.population = population
        self._find_costs_for_population()
        self.population.min_cost_per_generation.append(self.population.min_cost)
