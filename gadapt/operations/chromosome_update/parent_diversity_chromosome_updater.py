from gadapt.ga_model.chromosome import Chromosome
from gadapt.ga_model.allele import Allele
from gadapt.utils import ga_utils
from gadapt.operations.chromosome_update.base_chromosome_updater import (
    BaseChromosomeUpdater,
)


class ParentDiversityChromosomeUpdater(BaseChromosomeUpdater):
    """
    Updates chromosome for the parent diversity purpose.
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ParentDiversityChromosomeUpdater, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._genetic_diversity = None
        self.cost_diversity_in_initial_population = float('NaN')

    def _get_genetic_diversity(self, mother_gene, father_gene) -> float:
        return abs(mother_gene.variable_value - father_gene.variable_value) / (
            father_gene.gene.max_value - father_gene.gene.min_value
        )

    def _get_parent_structural_diversity(self):
        return round(ga_utils.average(self._genetic_diversity), 8)

    def chromosome_prepare_update(self, mother_gene: Allele, father_gene: Allele):
        if mother_gene is None or father_gene is None:
            return
        self._genetic_diversity.append(
            self._get_genetic_diversity(mother_gene, father_gene)
        )

    def chromosome_update(self, offspring1: Chromosome, offspring2: Chromosome, mother: Chromosome, father: Chromosome):
        parent_structural_diversity = self._get_parent_structural_diversity()
        offspring1.parent_structural_diversity_coefficient = parent_structural_diversity
        offspring2.parent_structural_diversity_coefficient = parent_structural_diversity
        parent_cost_diversity_coefficient = self.calculate_parent_cost_diversity_coefficient(father, mother)
        offspring2.parent_cost_diversity_coefficient = parent_cost_diversity_coefficient
        offspring1.parent_cost_diversity_coefficient = parent_cost_diversity_coefficient

    def chromosome_start_update(self, *args, **kwargs):
        self._genetic_diversity = []

    def calculate_parent_cost_diversity_coefficient(self, father_chromosome: Chromosome, mother_chromosome: Chromosome):


        parents_avg_difference = ga_utils.average_difference([father_chromosome.cost_value, mother_chromosome.cost_value])
        if self.cost_diversity_in_initial_population is None or self.cost_diversity_in_initial_population == 0:
            return parents_avg_difference
        return min(parents_avg_difference / self.cost_diversity_in_initial_population, 1)
