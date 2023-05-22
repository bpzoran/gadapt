import math
from ga_model.genetic_variable import GeneticVariable
from ga_model.ranking_model import RankingModel
import string_operation.ga_strings
import ga_model.definitions
class Gene(RankingModel):

    def __init__(self, gen_variable, var_value = None):
        super().__init__()
        self.genetic_variable = gen_variable        
        self.variable_value = var_value
        self._rank = -1
        self._cummulative_probability = ga_model.definitions.FLOAT_NAN
        if (self.variable_value == None or math.isnan(self.variable_value)):
            self.set_random_value()

    def __str__(self) -> str:
        return self.to_string()
    
    def to_string(self):
        return string_operation.ga_strings.gene_to_string(self)

    @property
    def genetic_variable(self) -> GeneticVariable:
        return self._genetic_variable
    
    @genetic_variable.setter
    def genetic_variable(self, value: GeneticVariable):
        self._genetic_variable = value

    @property
    def variable_value(self):
        return self._variable_value
    
    @variable_value.setter
    def variable_value(self, value):
        self._variable_value = value

    def set_random_value(self):
        self.variable_value = self.genetic_variable.make_random_value()