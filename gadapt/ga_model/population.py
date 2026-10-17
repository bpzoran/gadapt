"""
Population
"""

import math
import sys
from datetime import datetime
from typing import List

import gadapt.adapters.string_operation.ga_strings as ga_strings
import gadapt.ga_model.definitions as definitions
from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.ga_model.ga_options import GAOptions
from gadapt.ga_model.variable_value import VariableValue
from copy import copy as _shallow_copy, deepcopy as _deepcopy


class Population:
    def __init__(self, options: GAOptions):
        """Population for the genetic algorithm. It contains a collection of\
            candidate solutions, as well as additional parameters

        Args:

            options (GAOptions): Genetic Algorithm Options
        """
        self._seen_candidate_solutions = set()
        self._previous_min_cost = sys.float_info.min
        self._avg_cost = sys.float_info.min
        self._min_cost = sys.float_info.min
        if __name__ == "__main__":
            self._previous_avg_cost = sys.float_info.min
        if options.population_size < 4:
            raise Exception("Population size 4 must be higher than 3")
        self._set_init_values()
        self.last_candidate_solution_id = 1
        self._population_generation = 0
        self.options = options
        self.candidate_solutions: List[CandidateSolution] = []
        self.generate_initial_population()
        self.start_time = datetime.now()
        self.absolute_cost_diversity = float("NaN")
        self.relative_cost_diversity_coefficient = float("NaN")
        self.stddev_cost_diversity_coefficient = float("NaN")
        self.absolute_cost_diversity_in_first_population = float("NaN")
        self.relative_cost_diversity_in_first_population = float("NaN")
        self.timeout_expired = False
        self.min_cost_per_generation: List[float] = []
        self.generations_without_improvement = 0

    def __iter__(self):
        return PopulationIterator(self)

    def __getitem__(self, index):
        return self.candidate_solutions[index]

    def __next__(self):
        return next(self.candidate_solutions)

    def __len__(self):
        return len(self.candidate_solutions)

    def __str__(self):
        return self._to_string()

    def get_sorted(self, key=None, reverse: bool = False):
        """Sorted list of candidate solutions
        Args:
            key: Sorted key
            reverse (bool=False): is reversed
        """
        return sorted(self.candidate_solutions, key=key, reverse=reverse)

    def get_relative_cost_diversity_coefficient(self) -> float:
        return self.relative_cost_diversity_coefficient

    def append(self, c: CandidateSolution):
        self.candidate_solutions.append(c)

    def generate_initial_population(self):
        for i in range(self.options.population_size):
            self.add_new_candidate_solution()

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
    def best_individual(self) -> CandidateSolution:
        """
        Best individual candidate solution
        """
        return self._best_individual

    @best_individual.setter
    def best_individual(self, value: CandidateSolution):
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

    def update_generations_without_improvement(self):
        """
        Counts the consecutive generations in which the minimal cost did not improve.
        It is the same count that drives the exit check. The first costing is an improvement.
        """
        if math.isnan(self.previous_min_cost) or self.min_cost < self.previous_min_cost:
            self.generations_without_improvement = 0
        else:
            self.generations_without_improvement += 1

    def clear(self):
        """
        Clears all candidate solutions
        """
        self.candidate_solutions.clear()

    def clear_and_add_candidate_solutions(self, candidate_solutions: List[CandidateSolution]):
        """
        Clears candidate solutions and adds new ones
        Args:
            candidate_solutions (List[CandidateSolution]): candidate solutions to add
        """
        self.candidate_solutions.clear()
        self.add_candidate_solutions(candidate_solutions)

    def add_not_contained_candidate_solutions(self, candidate_solutions) -> int:
        """
        Adds only the candidate solutions whose variable values have never been in the population
        Args:
            candidate_solutions (Tuple[CandidateSolution]): candidate solutions to add
        Returns:
            int: number of candidate solutions added to the population
        """
        cnt = 0
        for c in candidate_solutions:
            if not self.contained_candidate_solution(c) and self.add_candidate_solution(c):
                cnt += 1
        return cnt

    def add_candidate_solutions(self, candidate_solutions) -> int:
        """
        Adds candidate solutions to population, as long as the population is not full
        Args:
            candidate_solutions (Tuple[CandidateSolution]): candidate solutions to add
        """
        for c in candidate_solutions:
            self.add_candidate_solution(c)

    def add_new_candidate_solution(self):
        """
        Adds a new candidate solution with random variable values to the population
        """
        candidate_solution = CandidateSolution(
            self.population_generation,
        )
        candidate_solution.candidate_solution_generation = 1
        self.add_candidate_solution(candidate_solution)

    def add_candidate_solution(self, candidate_solution) -> bool:
        """
        Adds candidate solution to the population
        Args:
            candidate_solution: candidate solution to add
        Returns:
            bool: True if the candidate solution is added, False if the population is full
        """
        if len(self) >= self.options.population_size:
            return False
        if candidate_solution.candidate_solution_id is None or candidate_solution.candidate_solution_id == -1:
            candidate_solution.candidate_solution_id = self.last_candidate_solution_id
            self.last_candidate_solution_id += 1
        if len(candidate_solution) == 0:
            for g in self.options.decision_variables:
                a = VariableValue(g)
                candidate_solution.append(a)
        self.append(candidate_solution)
        self.register_candidate_solution(candidate_solution)
        return True

    def register_candidate_solution(self, candidate_solution: CandidateSolution):
        """
        Remembers the current variable values of the candidate solution.
        It must be called again when the variable values of the candidate solution change.
        Args:
            candidate_solution: candidate solution to remember
        """
        self._seen_candidate_solutions.add(candidate_solution.get_values_tuple())

    def contained_candidate_solution(self, candidate_solution: CandidateSolution) -> bool:
        """
        Checks if the population has already contained a candidate solution with the same variable values.
        Args:
            candidate_solution: Candidate solution to check
        Returns:
            bool: True if the population ever contained a candidate solution with the same variable values, False otherwise.
        """
        return candidate_solution.get_values_tuple() in self._seen_candidate_solutions

    def clone(self) -> "Population":
        """Deep clone of the entire population (lists, candidate solutions, variable values, etc.)."""
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
        dup._seen_candidate_solutions = set(self._seen_candidate_solutions)
        dup.last_candidate_solution_id = self.last_candidate_solution_id
        dup._population_generation = self._population_generation
        dup.start_time = _deepcopy(self.start_time, memo)
        dup.absolute_cost_diversity = self.absolute_cost_diversity
        dup.absolute_cost_diversity_in_first_population = self.absolute_cost_diversity_in_first_population
        dup.timeout_expired = self.timeout_expired
        dup.min_cost_per_generation = _deepcopy(self.min_cost_per_generation, memo)
        dup.generations_without_improvement = self.generations_without_improvement

        # options: choose deep or shallow
        dup._options = _deepcopy(self._options, memo)  # deep
        # dup._options = self._options                      # or share same options

        # best individual (if set)
        dup._best_individual = _deepcopy(getattr(self, "_best_individual", None), memo)

        # candidate solutions list
        dup.candidate_solutions = _deepcopy(self.candidate_solutions, memo)

        return dup


class PopulationIterator:
    def __init__(self, population):
        self.population = population
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.population.candidate_solutions):
            result = self.population.candidate_solutions[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
