import random
from typing import List

from operations.mutation.chromosome_mutation.base_gene_mutation_rate_determinator import \
    BaseGeneMutationRateDeterminator
from operations.mutation.chromosome_mutation.base_gene_mutation_selector import BaseGeneMutationSelector


class ComposedGeneMutationSelector(BaseGeneMutationSelector):
    def __init__(self, gene_mutation_rate_determinator: BaseGeneMutationRateDeterminator) -> None:
        """
        Chromosome mutator that consists of more different chromosome mutators
        Args:
            options: genetic algorithm options
        """
        super().__init__(gene_mutation_rate_determinator)
        self.selectors: List[BaseGeneMutationSelector] = []

    def append(self, selector: BaseGeneMutationSelector):
        """
        Appends mutator to the composition of mutators
        """
        self.selectors.append(selector)

    def _mutate_chromosome(self, chromosome, max_number_of_mutation_genes):
        if chromosome is None:
            raise Exception("Chromosome must not be null")
        if len(self.selectors) == 0:
            raise Exception("at least one mutator must be added")
        if len(self.selectors) > 1:
            random.shuffle(self.selectors)
        nmg = 0
        number_of_mutation_genes = self._gene_mutation_rate_determinator.get_number_of_mutation_genes(chromosome, max_number_of_mutation_genes)
        if number_of_mutation_genes == 0:
            return 0
        for m in self.selectors:
            if nmg < number_of_mutation_genes:
                mg = m._mutate_chromosome(
                    chromosome, number_of_mutation_genes - nmg
                )
                nmg += mg
        return nmg