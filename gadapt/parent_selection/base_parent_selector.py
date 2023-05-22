from typing import List, Tuple
from ga_model.chromosome import Chromosome
import ga_model.definitions

class BaseParentSelector:    
    def select_mates(self, population) -> List[Tuple[Chromosome, Chromosome]]:
        raise Exception(ga_model.definitions.NOT_IMPLEMENTED)