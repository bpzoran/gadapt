from abc import ABC, abstractmethod
import math
import random
from typing import List
from gadapt.ga_model.gene import Gene


class BaseGeneMutationRateDeterminator(ABC):
    def __init__(self) -> None:
        """
        Base class for mutating genes in population
        Args:
            options: genetic algorithm options
        """
        super().__init__()
        self.max_number_of_mutation_genes = None

    def get_number_of_mutation_genes(self, chromosome, max_number_of_mutation_genes):
        if max_number_of_mutation_genes is None:
            raise Exception("max_number_of_mutation_genes must not be None")
        if not chromosome:
            raise Exception("chromosome must not be None")

        return self._get_number_of_mutation_genes(
                chromosome, max_number_of_mutation_genes
            )

    @abstractmethod
    def _get_number_of_mutation_genes(
            self, chromosome, max_number_of_mutation_genes
    ) -> int:
        pass