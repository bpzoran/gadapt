"""
Population
"""

import sys
from datetime import datetime
from typing import List

import gadapt.adapters.string_operation.ga_strings as ga_strings
import gadapt.ga_model.definitions as definitions
from gadapt.ga_model.chromosome import Chromosome
from gadapt.ga_model.ga_options import GAOptions
from gadapt.ga_model.allele import Allele
from copy import copy as _shallow_copy, deepcopy as _deepcopy


class Population:
    def __init__(self, options: GAOptions):
        """Population for the genetic algorithm. It contains a collection of\
            chromosomes, as well as additional parameters

        Args:

            options (GAOptions): Genetic Algorithm Options
        """
        self._previous_min_cost = sys.float_info.min
        self._avg_cost = sys.float_info.min
        self._min_cost = sys.float_info.min
        if __name__ == "__main__":
            self._previous_avg_cost = sys.float_info.min
        if options.population_size < 4:
            raise Exception("Population size 4 must be higher than 3")
        self.options = options
        self._set_init_values()
        self.last_chromosome_id = 1
        self._population_generation = 0
        self.options = options
        self.chromosomes: List[Chromosome] = []
        self.generate_initial_population()
        self.start_time = datetime.now()
        self.absolute_cost_diversity = float("NaN")
        self.absolute_cost_diversity_in_first_population = float("NaN")
        self.timeout_expired = False
        self.min_cost_per_generation: List[float] = []

    def __iter__(self):
        return PopulationIterator(self)

    def __getitem__(self, index):
        return self.chromosomes[index]

    def __next__(self):
        return next(self.chromosomes)

    def __len__(self):
        return len(self.chromosomes)

    def __str__(self):
        return self._to_string()

    def get_sorted(self, key=None, reverse: bool = False):
        """Sorted list of chromosomes
        Args:
            key: Sorted key
            reverse (bool=False): is reversed
        """
        return sorted(self.chromosomes, key=key, reverse=reverse)

    def append(self, c: Chromosome):
        self.chromosomes.append(c)

    def generate_initial_population(self):
        for i in range(self.options.population_size):
            self.add_new_chromosome()

    def _to_string(self):
        return ga_strings.population_to_string(self)

    def _set_init_values(self):
        float_init_value = definitions.FLOAT_NAN
        self.avg_cost = float_init_value
        self.previous_avg_cost = float_init_value
        self.min_cost = float_init_value
        self.previous_min_cost = float_init_value

    @property
    def options(self) -> GAOptions:
        """
        Genetic algorithm options
        """
        return self._options

    @options.setter
    def options(self, value: GAOptions):
        self._options = value

    @property
    def avg_cost(self) -> float:
        """
        Average cost of the population
        """
        return self._avg_cost

    @avg_cost.setter
    def avg_cost(self, value: float):
        self._avg_cost = value

    @property
    def previous_avg_cost(self) -> float:
        """
        Previous average cost
        """
        return self._previous_avg_cost

    @previous_avg_cost.setter
    def previous_avg_cost(self, value: float):
        self._previous_avg_cost = value

    @property
    def min_cost(self):
        """
        Minimum cost
        """
        return self._min_cost

    @min_cost.setter
    def min_cost(self, value: float):
        self._min_cost = value

    @property
    def previous_min_cost(self):
        """
        Previous minimum cost
        """
        return self._previous_min_cost

    @previous_min_cost.setter
    def previous_min_cost(self, value: float):
        self._previous_min_cost = value

    @property
    def best_individual(self) -> Chromosome:
        """
        Best individual chromosome
        """
        return self._best_individual

    @best_individual.setter
    def best_individual(self, value: Chromosome):
        self._best_individual = value

    @property
    def population_generation(self):
        """
        Current generation of the population
        """
        return self._population_generation

    @population_generation.setter
    def population_generation(self, value):
        self._population_generation = value

    def clear(self):
        """
        Clears all chromosomes
        """
        self.chromosomes.clear()

    def clear_and_add_chromosomes(self, chromosomes: List[Chromosome]):
        """
        Clears chromosomes and adds new ones
        Args:
            chromosomes (List[Chromosome]): chromosomes to add
        """
        self.chromosomes.clear()
        self.add_chromosomes(chromosomes)

    def add_chromosomes(self, chromosomes):
        """
        Adds chromosomes to population
        Args:
            chromosomes (Tuple[Chromosome]): chromosomes to add
        """
        for c in chromosomes:
            self.add_chromosome(c)

    def add_new_chromosome(self):
        """
        Adds new chromosomes to the population
        """
        chromosome = Chromosome(
            self.population_generation,
        )
        chromosome.chromosome_generation = 1
        self.add_chromosome(chromosome)

    def add_chromosome(self, chromosome):
        """
        Adds chromosome to the population
        Args:
            chromosome: chromosome to add
        """
        if len(self) >= self.options.population_size:
            return
        if chromosome.chromosome_id is None or chromosome.chromosome_id == -1:
            chromosome.chromosome_id = self.last_chromosome_id
            self.last_chromosome_id += 1
        if len(chromosome) == 0:
            for g in self.options.genes:
                a = Allele(g)
                chromosome.append(a)
        self.append(chromosome)

    def clone(self) -> "Population":
        """Deep clone of the entire population (lists, chromosomes, alleles, etc.)."""
        return _deepcopy(self)

    def copy(self) -> "Population":
        """Shallow copy (top-level object only; lists/objects are shared!)."""
        return _shallow_copy(self)

    def __deepcopy__(self, memo):
        # allocate without calling __init__
        cls = self.__class__
        dup = cls.__new__(cls)
        memo[id(self)] = dup

        # copy simple fields
        dup._previous_min_cost = self._previous_min_cost
        dup._avg_cost = self._avg_cost
        dup._min_cost = self._min_cost
        dup._previous_avg_cost = getattr(self, "_previous_avg_cost", self._avg_cost)
        dup.last_chromosome_id = self.last_chromosome_id
        dup._population_generation = self._population_generation
        dup.start_time = _deepcopy(self.start_time, memo)
        dup.absolute_cost_diversity = self.absolute_cost_diversity
        dup.absolute_cost_diversity_in_first_population = self.absolute_cost_diversity_in_first_population
        dup.timeout_expired = self.timeout_expired
        dup.min_cost_per_generation = _deepcopy(self.min_cost_per_generation, memo)

        # options: choose deep or shallow
        dup._options = _deepcopy(self._options, memo)  # deep
        # dup._options = self._options                      # or share same options

        # best individual (if set)
        dup._best_individual = _deepcopy(getattr(self, "_best_individual", None), memo)

        # chromosomes list
        dup.chromosomes = _deepcopy(self.chromosomes, memo)

        return dup


class PopulationIterator:
    def __init__(self, population):
        self.population = population
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.population.chromosomes):
            result = self.population.chromosomes[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
