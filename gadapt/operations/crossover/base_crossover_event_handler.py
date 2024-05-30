from gadapt.ga_model.chromosome import Chromosome
from gadapt.ga_model.gene import Gene


class BaseCrossoverEventHandler:
    """
    Handles crossover events
    """
    def on_decision_variable_crossed(self, mother_gene: Gene, father_gene: Gene):
        pass

    def on_all_decision_variable_crossed(self, offspring1: Chromosome, offspring2: Chromosome):
        pass

    def pre_cross_genetic_material(self, *args, **kwargs):
        pass
