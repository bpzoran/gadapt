"""
Genetic algorithm options
"""

from typing import List

from gadapt.ga_model.gene import Gene


class GAOptions:
    def __init__(self, ga) -> None:
        """
        Genetic algorithm options class
        Args:
            ga: Genetic algorithm class, containing data to initialize options
        """
        super().__init__()
        self._population_size = ga.population_size
        self._keep_elitism_percentage = ga.keep_elitism_percentage
        self._number_of_crossover_parents = ga.number_of_crossover_parents
        self._cost_function = ga.cost_function
        self._cost_diversity_coefficient_function = None
        self._immigration_number = ga.immigration_number
        self._crossover_probability = ga.crossover_probability
        self._crossover_min_probability = ga.crossover_min_probability
        self._crossover_max_probability = ga.crossover_max_probability
        self._set_number_of_mutation_chromosomes(ga)
        self._max_attempt_no = ga.max_attempt_no
        self._requested_cost = ga.requested_cost
        self._ensure_unique_individuals = ga.ensure_unique_individuals
        self._decrease_step_automatically = ga.decrease_step_automatically
        self._normal_distribution_mutation_min_std_dev = ga.normal_distribution_mutation_min_std_dev
        self._normal_distribution_mutation_max_std_dev = ga.normal_distribution_mutation_max_std_dev
        self._logging = ga.logging
        self._genes = ga._genes
        self._set_number_of_mutation_genes(ga)
        self._must_mutate_for_same_parents = ga.must_mutate_for_same_parents
        self._timeout = ga.timeout

    def _set_number_of_mutation_chromosomes(self, ga):
        if (
            (ga.number_of_mutation_chromosomes is not None)
            and isinstance(ga.number_of_mutation_chromosomes, int)
            and ga.number_of_mutation_chromosomes >= 0
        ):
            self._number_of_mutation_chromosomes = ga.number_of_mutation_chromosomes
        elif (
            (ga.percentage_of_mutation_chromosomes is not None)
            and isinstance(ga.percentage_of_mutation_chromosomes, float)
            and 0.0 <= ga.percentage_of_mutation_chromosomes <= 100
        ):
            nomc = round(
                (self.population_size / 2)
                * (ga.percentage_of_mutation_chromosomes / 100)
            )
            while (
                nomc
                >= round(self.population_size * (self.keep_elitism_percentage / 100))
                - self.immigration_number
            ):
                nomc -= 1
            if nomc < 0:
                raise Exception(
                    "Invalid percentage of mutation chromosomes and immigration number"
                )
            self._number_of_mutation_chromosomes = nomc
        else:
            self._number_of_mutation_chromosomes = ga.number_of_mutation_chromosomes

    def _set_number_of_mutation_genes(self, ga):
        if (
            (ga.number_of_mutation_genes is not None)
            and isinstance(ga.number_of_mutation_genes, int)
            and ga.number_of_mutation_genes >= 0
        ):
            self._number_of_mutation_genes = ga.number_of_mutation_genes
        elif (
            (ga.percentage_of_mutation_genes is not None)
            and isinstance(ga.percentage_of_mutation_genes, float)
            and 0.0 <= ga.percentage_of_mutation_genes <= 100
        ):
            self._number_of_mutation_genes = round(
                float(len(self._genes)) * (ga.percentage_of_mutation_genes / 100)
            )
        else:
            self._number_of_mutation_genes = ga.number_of_mutation_genes

    @property
    def requested_cost(self) -> float:
        """
        Determines the requested value which causes the exit from the genetic algorithm
        """
        return self._requested_cost

    @requested_cost.setter
    def requested_cost(self, value: float):
        self._requested_cost = value

    @property
    def ensure_unique_individuals(self) -> bool:
        return self._ensure_unique_individuals

    @ensure_unique_individuals.setter
    def ensure_unique_individuals(self, value: bool):
        self._ensure_unique_individuals = value

    @property
    def decrease_step_automatically(self) -> bool:
        return self._decrease_step_automatically

    @decrease_step_automatically.setter
    def decrease_step_automatically(self, value: bool):
        self._decrease_step_automatically = value

    @property
    def normal_distribution_mutation_min_std_dev(self) -> float:
        return self._normal_distribution_mutation_min_std_dev

    @normal_distribution_mutation_min_std_dev.setter
    def normal_distribution_mutation_min_std_dev(self, value: float):
        self._normal_distribution_mutation_min_std_dev = value

    @property
    def normal_distribution_mutation_max_std_dev(self) -> float:
        return self._normal_distribution_mutation_max_std_dev

    @normal_distribution_mutation_max_std_dev.setter
    def normal_distribution_mutation_max_std_dev(self, value: float):
        self._normal_distribution_mutation_max_std_dev = value

    @property
    def max_attempt_no(self) -> int:
        """
        Determines the number of generations in which there is no\
            improvement in the average/minimal cost.
        """
        return self._max_attempt_no

    @max_attempt_no.setter
    def max_attempt_no(self, value: int):
        self._max_attempt_no = value

    @property
    def immigration_number(self) -> int:
        """
        Number of immigration chromosomes
        """
        return self._immigration_number

    @immigration_number.setter
    def immigration_number(self, value: int):
        self._immigration_number = value

    @property
    def crossover_probability(self) -> float:
        return self._crossover_probability

    @crossover_probability.setter
    def crossover_probability(self, value: float):
        self._crossover_probability = value

    @property
    def crossover_min_probability(self) -> float:
        return self._crossover_min_probability

    @crossover_min_probability.setter
    def crossover_min_probability(self, value: float):
        self._crossover_min_probability = value

    @property
    def crossover_max_probability(self) -> float:
        return self._crossover_max_probability

    @crossover_max_probability.setter
    def crossover_max_probability(self, value: float):
        self._crossover_max_probability = value

    @property
    def number_of_mutation_chromosomes(self) -> int:
        """
        The number of mutation chromosomes in the population.
        """
        return self._number_of_mutation_chromosomes

    @number_of_mutation_chromosomes.setter
    def number_of_mutation_chromosomes(self, value: int):
        self._number_of_mutation_chromosomes = value

    @property
    def number_of_mutation_genes(self) -> int:
        """
        The number of mutated genes in each chromosome.
        """
        return self._number_of_mutation_genes

    @number_of_mutation_genes.setter
    def number_of_mutation_genes(self, value: int):
        self._number_of_mutation_genes = value

    @property
    def cost_function(self):
        """
        Custom function for the cost calculation (fitness)
        """
        return self._cost_function

    @property
    def cost_diversity_coefficient_function(self):
        return self._cost_diversity_coefficient_function

    @cost_diversity_coefficient_function.setter
    def cost_diversity_coefficient_function(self, value):
        self._cost_diversity_coefficient_function = value

    @cost_function.setter
    def cost_function(self, value):
        self._cost_function = value

    def get_cost_diversity_coefficient_function(self):
        return self.cost_diversity_coefficient_function

    @property
    def population_size(self) -> int:
        """
        Number of chromosomes in the population.
        """
        return self._population_size

    @population_size.setter
    def population_size(self, value: int):
        self._population_size = value

    @property
    def keep_elitism_percentage(self) -> int:
        """
        Percentage number of chromosomes to be kept in the population by the cost value
        """
        return self._keep_elitism_percentage

    @keep_elitism_percentage.setter
    def keep_elitism_percentage(self, value: int):
        self._keep_elitism_percentage = value

    @property
    def number_of_crossover_parents(self) -> int:
        """
        Number of parents to be included in the mating pool
        """
        if self._number_of_crossover_parents > 1:
            return self._number_of_crossover_parents
        return self.keep_number

    @number_of_crossover_parents.setter
    def number_of_crossover_parents(self, value: int):
        self._number_of_crossover_parents = value

    @property
    def genes(self) -> List[Gene]:
        """
        Collection of genes
        """
        return self._genes

    @property
    def _abandon_number(self) -> int:
        return self._get_abandon_number()

    def _get_abandon_number(self) -> int:
        return round(self.population_size * (1 - self.keep_elitism_percentage / 100))

    @property
    def keep_number(self) -> int:
        return self.population_size - self._abandon_number

    @property
    def logging(self) -> bool:
        """
        If True, the log file will be created in the\
            current working directory.
        """
        return self._logging

    @logging.setter
    def logging(self, value: bool):
        self._logging = value

    @property
    def must_mutate_for_same_parents(self) -> bool:
        """
        Indicates if completely the same parents must influence\
            mutation for their children.
        """
        return self._must_mutate_for_same_parents

    @must_mutate_for_same_parents.setter
    def must_mutate_for_same_parents(self, value: bool):
        self._must_mutate_for_same_parents = value

    @property
    def timeout(self) -> int:
        """
        A number of seconds after which the genetic algorithm optimisation will\
            exit, regardless of whether exit_check criteria is reached.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        self._timeout = value
