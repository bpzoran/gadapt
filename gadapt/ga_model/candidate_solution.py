"""
Candidate solution
"""
from typing import List

import gadapt.adapters.string_operation.ga_strings as ga_strings
import gadapt.ga_model.definitions as definitions
from gadapt.ga_model.decision_variable import DecisionVariable
from gadapt.ga_model.variable_value import VariableValue
from gadapt.ga_model.ranking_model import RankingModel


class CandidateSolution(RankingModel):
    def __init__(
        self,
        population_generation: int,
    ):
        """
        CandidateSolution class.
        A candidate solution is a part of the Population. It consists of variable values,
        one for each decision variable.
        Args:
            population_generation: population generation
        """
        super().__init__()
        self._candidate_solution_generation = None
        self._parent_structural_diversity_coefficient = float("NaN")
        self._parent_cost_diversity_coefficient = float("NaN")
        self._cost_value = definitions.FLOAT_NAN
        self._is_immigrant = False
        self._population_generation = population_generation
        self._candidate_solution_id = None
        self._mutated_variables_id_list: List[int] = []
        self._first_mutant_generation = 0
        self._first_immigrant_generation = 0
        self._last_mutant_generation = 0
        self._last_immigrant_generation = 0
        self._candidate_solution_string = None
        self._mother_id = -1
        self._father_id = -1
        self._is_mutated = False
        self._is_immigrant = False
        self._variable_values: List[VariableValue] = []
        self._hash_cache = None

    def __str__(self) -> str:
        return self._get_candidate_solution_string()

    def __getitem__(self, index) -> VariableValue:
        return self._variable_values[index]

    def __next__(self):
        return next(self._variable_values)

    def __len__(self):
        return len(self._variable_values)

    def __iter__(self):
        return CandidateSolutionIterator(self)

    def __eq__(self, other: object) -> bool:
        """
        Two candidate solutions are equal if they have the same variable values in the same order.
        """
        if self is other:
            return True
        if not isinstance(other, CandidateSolution):
            return False
        if len(self._variable_values) != len(other._variable_values):
            return False
        # Comparing tuples is very fast in Python
        return self.get_values_tuple() == other.get_values_tuple()

    def __hash__(self):
        if self._hash_cache is None:
            self._hash_cache = hash(tuple(g.value for g in self._variable_values))
        return self._hash_cache

    def reset_hash_cache(self):
        self._hash_cache = None

    def get_values_tuple(self) -> tuple:
        """
        Extracts variable values into a hashable tuple.
        """
        return tuple(variable_value.value for variable_value in self._variable_values)


    def _get_sorted(self, key: None = None, reverse: bool = False):
        return sorted(self._variable_values, key=key, reverse=reverse)

    def append(self, g: VariableValue):
        """
        Appends a new variable value into the candidate solution
        """
        self._variable_values.append(g)

    def clear(self):
        """
        Clears all decision variables from the candidate solution
        """
        self._variable_values.clear()

    def _to_string(self):
        """
        Converts the candidate solution to the string
        """
        return ga_strings.candidate_solution_to_string(self)

    def set_candidate_solution_string_none(self):
        """
        Sets the candidate solution string to None
        """
        self._candidate_solution_string = None

    def _get_candidate_solution_string(self):
        if self._candidate_solution_string is None:
            self._candidate_solution_string = self._to_string()
        return self._candidate_solution_string

    @property
    def number_of_mutation_decision_variables(self):
        """
        The number of mutated decision variables in the candidate solution.
        """
        return self._number_of_mutation_decision_variables

    @number_of_mutation_decision_variables.setter
    def number_of_mutation_decision_variables(self, value):
        self._number_of_mutation_decision_variables = value

    @property
    def candidate_solution_id(self):
        """
        Id of the candidate solution
        """
        return self._candidate_solution_id

    @candidate_solution_id.setter
    def candidate_solution_id(self, value):
        self._candidate_solution_id = value

    @property
    def cost_value(self):
        """
        Calculated cost value  of the candidate solution
        """
        return self._cost_value

    @cost_value.setter
    def cost_value(self, value):
        self._cost_value = value

    @property
    def is_mutated(self) -> bool:
        """
        Indicates if the candidate solution is mutated
        """
        return self._is_mutated

    @is_mutated.setter
    def is_mutated(self, value: bool):
        self._is_mutated = value

    @property
    def is_immigrant(self) -> bool:
        """
        Indicates if the candidate solution is immigrant
        """
        return self._is_immigrant

    @is_immigrant.setter
    def is_immigrant(self, value: bool):
        self._is_immigrant = value

    @property
    def mother_id(self) -> int:
        """
        ID of mother candidate solution
        """
        return self._mother_id

    @mother_id.setter
    def mother_id(self, value: int):
        self._mother_id = value

    @property
    def father_id(self) -> int:
        """
        ID of father candidate solution
        """
        return self._father_id

    @father_id.setter
    def father_id(self, value: int):
        self._father_id = value

    def add_variable_value(self, decision_variable: DecisionVariable, value: float = definitions.FLOAT_NAN):
        """
        Adds a variable value to the candidate solution
        """
        g = VariableValue(decision_variable, value)
        self.append(g)

    @property
    def parent_structural_diversity_coefficient(self) -> float:
        """
        Diversity of parents
        """
        return self._parent_structural_diversity_coefficient

    @parent_structural_diversity_coefficient.setter
    def parent_structural_diversity_coefficient(self, value: float):
        self._parent_structural_diversity_coefficient = value

    @property
    def parent_cost_diversity_coefficient(self) -> float:
        """
        Diversity of parents
        """
        return self._parent_cost_diversity_coefficient

    @parent_cost_diversity_coefficient.setter
    def parent_cost_diversity_coefficient(self, value: float):
        self._parent_cost_diversity_coefficient = value

    @property
    def population_generation(self) -> int:
        """
        Population generation in which the candidate solution appeared
        """
        return self._population_generation

    @population_generation.setter
    def population_generation(self, value: int):
        self._population_generation = value

    @property
    def candidate_solution_generation(self) -> int:
        """
        Generation of candidate solution. It differs from the Population generation.
        It determines how many generations were needed for this candidate solution to arise.
        """
        return self._candidate_solution_generation

    @candidate_solution_generation.setter
    def candidate_solution_generation(self, value: int):
        self._candidate_solution_generation = value

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
    def succ(self) -> bool:
        """
        Indicates if cost function execution succeded
        """
        return self._succ

    @succ.setter
    def succ(self, value: bool):
        self._succ = value

    @property
    def mutated_variables_id_list(self) -> List[int]:
        """
        List of mutated variables
        """
        return self._mutated_variables_id_list


class CandidateSolutionIterator:
    def __init__(self, candidate_solution):
        self.candidate_solution = candidate_solution
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.candidate_solution._variable_values):
            result = self.candidate_solution._variable_values[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
