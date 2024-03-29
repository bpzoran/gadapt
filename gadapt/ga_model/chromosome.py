"""
Chromosome
"""

from typing import List
from gadapt.ga_model.gene import Gene
from gadapt.ga_model.genetic_variable import GeneticVariable
from gadapt.ga_model.ranking_model import RankingModel
from gadapt.operations.immigration.chromosome_immigration.base_chromosome_immigrator import (
    BaseChromosomeImmigrator,
)
from gadapt.operations.mutation.chromosome_mutation.base_chromosome_mutator import (
    BaseChromosomeMutator,
)
import gadapt.ga_model.definitions as definitions
import gadapt.adapters.string_operation.ga_strings as ga_strings


class Chromosome(RankingModel):
    def __init__(
        self,
        mutator: BaseChromosomeMutator,
        immigrator: BaseChromosomeImmigrator,
        population_generation: int,
    ):
        """
        Chromosome class.
        Chromosome is a part of the Population. Chromosome consists of Genes.
        Args:
            immigrator (BaseChromosomeImmigrator): Immigration algorithm
            population_generation (int): Generation in which the\
                chromosome is created in the population
        """
        super().__init__()
        self._mutator = mutator
        self._immigrator = immigrator
        self._cost_value = definitions.FLOAT_NAN
        self._is_immigrant = False
        self._population_generation = population_generation
        self._chromosome_id = None
        self._mutated_variables_id_list: List[int] = []
        self._first_mutant_generation = 0
        self._first_immigrant_generation = 0
        self._last_mutant_generation = 0
        self._last_immigrant_generation = 0
        self._chromosome_string = None
        self._mother_id = -1
        self._father_id = -1
        self._is_mutated = False
        self._is_immigrant = False
        self._genes: List[Gene] = []

    def __str__(self) -> str:
        return self._get_chromosome_string()

    def __getitem__(self, index) -> Gene:
        return self._genes[index]

    def __next__(self):
        return next(self._genes)

    def __len__(self):
        return len(self._genes)

    def __iter__(self):
        return ChromosomeIterator(self)

    def _get_sorted(self, key: None = None, reverse: bool = False):
        return sorted(self._genes, key=key, reverse=reverse)

    def append(self, g: Gene):
        """
        Appends a new gene into the chromosom
        """
        self._genes.append(g)

    def clear(self):
        """
        Clears all genes from the chromosome
        """
        self._genes.clear()

    def _to_string(self):
        """
        Converts the chromosome to the string
        """
        return ga_strings.chromosome_to_string(self)

    def set_chromosome_string_none(self):
        """
        Sets the chromosome string to None
        """
        self._chromosome_string = None

    def _get_chromosome_string(self):
        if self._chromosome_string is None:
            self._chromosome_string = self._to_string()
        return self._chromosome_string

    @property
    def mutator(self) -> BaseChromosomeMutator:
        """
        Mutation algorithm
        """
        return self._mutator

    @mutator.setter
    def mutator(self, value: BaseChromosomeMutator):
        self._mutator = value

    @property
    def immigrator(self) -> BaseChromosomeImmigrator:
        """
        Immigration algorithm
        """
        return self._immigrator

    @immigrator.setter
    def immigrator(self, value: BaseChromosomeImmigrator):
        self._immigrator = value

    @property
    def number_of_mutation_genes(self):
        """
        The number of mutated genes in the chromosome.
        """
        return self._number_of_mutation_genes

    @number_of_mutation_genes.setter
    def number_of_mutation_genes(self, value):
        self._number_of_mutation_genes = value

    @property
    def chromosome_id(self):
        """
        Id of the chromosme
        """
        return self._chromosome_id

    @chromosome_id.setter
    def chromosome_id(self, value):
        self._chromosome_id = value

    @property
    def cost_value(self):
        """
        Calculated cost value  of the chromosome
        """
        return self._cost_value

    @cost_value.setter
    def cost_value(self, value):
        self._cost_value = value

    @property
    def is_mutated(self) -> bool:
        """
        Indicates if the chromosome is mutated
        """
        return self._is_mutated

    @is_mutated.setter
    def is_mutated(self, value: bool):
        self._is_mutated = value

    @property
    def is_immigrant(self) -> bool:
        """
        Indicates if the chromosome is immigrant
        """
        return self._is_immigrant

    @is_immigrant.setter
    def is_immigrant(self, value: bool):
        self._is_immigrant = value

    @property
    def mother_id(self) -> int:
        """
        ID of mother chromosome
        """
        return self._mother_id

    @mother_id.setter
    def mother_id(self, value: int):
        self._mother_id = value

    @property
    def father_id(self) -> int:
        """
        ID of father chromosome
        """
        return self._father_id

    @father_id.setter
    def father_id(self, value: int):
        self._father_id = value

    def add_gene(
        self, gen_var: GeneticVariable, gen_var_value: float = definitions.FLOAT_NAN
    ):
        """
        Adds a gene to the chromosome
        """
        g = Gene(gen_var, gen_var_value)
        self.append(g)

    @property
    def parent_diversity(self) -> float:
        """
        Diversity of parents
        """
        return self._parent_diversity

    @parent_diversity.setter
    def parent_diversity(self, value: float):
        self._parent_diversity = value

    @property
    def population_generation(self) -> int:
        """
        Population generation in which the chromosome appeared
        """
        return self._population_generation

    @population_generation.setter
    def population_generation(self, value: int):
        self._population_generation = value

    @property
    def chromosome_generation(self) -> int:
        """
        Generation of chromosome. It differs from the Population generation.
        It determines how many generations were needed for this chromosome to arise.
        """
        return self._chromosome_generation

    @chromosome_generation.setter
    def chromosome_generation(self, value: int):
        self._chromosome_generation = value

    @property
    def first_mutant_generation(self) -> int:
        """
        Indicates how many generations passed after a first mutation
        """
        return self._first_mutant_generation

    @first_mutant_generation.setter
    def first_mutant_generation(self, value: int):
        self._first_mutant_generation = value

    @property
    def last_mutant_generation(self) -> int:
        """
        Indicates how many generations passed after a last mutation
        """
        return self._last_mutant_generation

    @last_mutant_generation.setter
    def last_mutant_generation(self, value: int):
        self._last_mutant_generation = value

    @property
    def first_immigrant_generation(self) -> int:
        """
        Indicates how many generations passed after a first immigration
        """
        return self._first_immigrant_generation

    @first_immigrant_generation.setter
    def first_immigrant_generation(self, value: int):
        self._first_immigrant_generation = value

    @property
    def last_immigrant_generation(self) -> int:
        """
        Indicates how many generations passed after a last immigration
        """
        return self._last_immigrant_generation

    @last_immigrant_generation.setter
    def last_immigrant_generation(self, value: int):
        self._last_immigrant_generation = value

    @property
    def mutation_on_both_sides(self) -> bool:
        """
        Indicates if mutation should be applied on both sides
        """
        return self._mutation_on_both_sides

    @mutation_on_both_sides.setter
    def mutation_on_both_sides(self, value: bool):
        """
        Indicates if mutation of the chromosome shouls be applied with the\
            same probability of lower and higher value comparing with the current value
        """
        self._mutation_on_both_sides = value

    @property
    def succ(self) -> bool:
        """
        Indicates if cost function execution succeded
        """
        return self._succ

    @succ.setter
    def succ(self, value: bool):
        self._succ = value

    def mutate(self, number_of_mutation_genes: int):
        """
        Mutates chromosome
        """
        self.mutator.mutate(self, number_of_mutation_genes)

    def immigrate(self):
        """
        Immigrates chromosome
        """
        self.immigrator.immigrate(self)

    @property
    def mutated_variables_id_list(self) -> List[int]:
        """
        List of mutated variables
        """
        return self._mutated_variables_id_list


class ChromosomeIterator:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.chromosome._genes):
            result = self.chromosome._genes[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
