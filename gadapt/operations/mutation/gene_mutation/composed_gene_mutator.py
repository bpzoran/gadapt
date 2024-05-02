import random
from typing import List

from ga_model.gene import Gene
from operations.mutation.gene_mutation.base_gene_mutator import BaseGeneMutator


class ComposedGeneMutator(BaseGeneMutator):

    def __init__(self) -> None:
        super().__init__()
        self.mutators: List[BaseGeneMutator] = []

    def append(self, mutator: BaseGeneMutator):
        """
        Appends gene mutator to a list of mutators.
        Args:
            mutator: An instance of the BaseGeneMutator class that will be added to the list of mutator.
        """
        self.mutators.append(mutator)

    def _make_mutated_value(self, g: Gene):
        if g is None:
            raise Exception("Gene must not be null")
        if len(self.mutators) == 0:
            raise Exception("at least one mutator must be added")
        if len(self.mutators) > 1:
            random.shuffle(self.mutators)
        return self.mutators[0]._make_mutated_value(g)