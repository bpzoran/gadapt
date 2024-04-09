import random
from typing import List

from operations.mutation.chromosome_mutation.base_gene_mutation_rate_determinator import \
    BaseGeneMutationRateDeterminator


class ComposedGeneMutationRateDeterminator(BaseGeneMutationRateDeterminator):
    def __init__(self) -> None:
        """
        Chromosome mutator that consists of more different chromosome mutators
        Args:
            options: genetic algorithm options
        """
        super().__init__()
        self.determinators: List[BaseGeneMutationRateDeterminator] = []

    def append(self, determinator: BaseGeneMutationRateDeterminator):
        """
        Appends mutator to the composition of mutators
        """
        self.determinators.append(determinator)

    def _get_number_of_mutation_genes(self, chromosome, max_number_of_mutation_genes):
        if chromosome is None:
            raise Exception("Chromosome must not be null")
        if len(self.determinators) == 0:
            raise Exception("at least one mutator must be added")
        if len(self.determinators) > 1:
            random.shuffle(self.determinators)
        current_determinator = self.determinators[0]
        return current_determinator.get_number_of_mutation_genes(chromosome, max_number_of_mutation_genes)
