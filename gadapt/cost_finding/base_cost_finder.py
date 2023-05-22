import sys
import traceback
from typing import List
from ga_model.chromosome import Chromosome
import ga_model.definitions

class BaseCostFinder:
    def execute_function(self, cost_function, c: Chromosome):
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

    def find_costs_for_chromosome(self, population):
        raise Exception(ga_model.definitions.NOT_IMPLEMENTED)