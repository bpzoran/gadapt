from ast import Tuple
from ga_model.chromosome import Chromosome
from ga_model.gene import Gene
import ga_model.definitions

class BaseGeneCombination:
    def combine(self, mother_gene: Gene, father_gene: Gene):
        raise Exception(ga_model.definitions.NOT_IMPLEMENTED)