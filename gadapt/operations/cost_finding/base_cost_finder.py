import sys
import traceback
from abc import ABC, abstractmethod
from typing import Optional, Callable

from gadapt.ga_model.allele import Allele
from gadapt.ga_model.population import Population
from gadapt.ga_model.chromosome import Chromosome


class BaseCostFinder(ABC):
    """
    Base class for cost finding
    """

    def __init__(self):
        super().__init__()
        self.population: Optional[Population] = None

    def _execute_single_cost_function(self, alleles: list[Allele], cost_function: Callable):
        gene_values = [a.variable_value for a in alleles]
        cost_value = cost_function(gene_values)

        # Check if any allele has step < initial_step (step was decreased for exploitation)
        needs_refinement = any(
            a.gene.step is not None
            and a.gene.initial_step is not None
            and a.gene.step < a.gene.initial_step
            for a in alleles
        )
        if not needs_refinement:
            return cost_value

        # Build per-allele temporary steps (start at current step)
        temp_steps = []
        for a in alleles:
            if (a.gene.step is not None
                    and a.gene.initial_step is not None
                    and a.gene.step < a.gene.initial_step):
                temp_steps.append(a.gene.step)
            else:
                # Already at or above initial_step – no further refinement
                temp_steps.append(None)

        best_cost = cost_value
        best_values = list(gene_values)  # copy of original values

        # Iteratively coarsen: multiply each temp_step by 10 until all reach initial_step
        while True:
            all_reached = True
            for i, a in enumerate(alleles):
                if temp_steps[i] is not None:
                    temp_steps[i] = temp_steps[i] * 10.0
                    if temp_steps[i] > a.gene.initial_step:
                        temp_steps[i] = a.gene.initial_step
                    if temp_steps[i] < a.gene.initial_step:
                        all_reached = False
                # If temp_steps[i] is None the allele is already settled

            # Round values according to decimal places of the current temp_step
            rounded_values = []
            for i, a in enumerate(alleles):
                if temp_steps[i] is not None:
                    dp = a.gene._get_decimal_places(temp_steps[i])
                    rounded_values.append(round(best_values[i], dp))
                else:
                    rounded_values.append(best_values[i])

            new_cost = cost_function(rounded_values)

            if new_cost < best_cost:
                best_cost = new_cost
                best_values = list(rounded_values)
            else:
                # Cost did not improve – stop refining
                break

            if all_reached:
                break

        # If the refined cost is better than the original, update allele values
        if best_cost < cost_value:
            for i, a in enumerate(alleles):
                a.variable_value = best_values[i]

        return best_cost

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
            cost_value = self._execute_single_cost_function(alleles, cost_function)
            c.cost_value = cost_value
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
