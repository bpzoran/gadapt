import math
import random
from abc import ABC, abstractmethod
from typing import Tuple, List

from gadapt.ga_model.variable_value import VariableValue
from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.operations.candidate_solution_update.base_candidate_solution_updater import (
    BaseCandidateSolutionUpdater,
)
from gadapt.operations.crossover.base_crossover_probability_determinator import BaseCrossoverProbabilityDeterminator
from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_selector import BaseDecisionVariableMutationSelector


class BaseCrossover(ABC):
    """Base Crossover Class"""

    # Attempts to produce offspring that are not already seen, when ensuring unique individuals
    MAX_UNIQUE_ATTEMPTS = 15
    # After this many failed attempts, the offspring are mutated to escape duplicates
    MUTATE_AFTER_ATTEMPT = 5

    def __init__(self, candidate_solution_updater: BaseCandidateSolutionUpdater, mutator: BaseDecisionVariableMutationSelector, crossover_rate_determinator: BaseCrossoverProbabilityDeterminator):
        self._current_decision_variable_number = -1
        self._candidate_solution_updater = candidate_solution_updater
        self._mutator = mutator
        self.crossover_rate_determinator: BaseCrossoverProbabilityDeterminator = crossover_rate_determinator

    def _mate_pair_until_added(self, population, candidate_solution1, candidate_solution2 ) -> None:
        candidate_solutions_added = False
        number_of_added_candidate_solutions = 0

        new_offsprings = []
        number_of_attempts = 0
        while (not candidate_solutions_added) and number_of_attempts < self.MAX_UNIQUE_ATTEMPTS:
            number_of_attempts += 1
            offsprings_to_add = []
            if len(new_offsprings) == 0:
                new_offsprings.extend(list(self._mate_pair(
                    candidate_solution1, candidate_solution2, population
                )))
            if number_of_added_candidate_solutions == 0:
                offsprings_to_add.extend(new_offsprings)
                new_offsprings.clear()
            elif number_of_added_candidate_solutions == 1:
                offsprings_to_add.append(new_offsprings.pop())
            else:
                return
            if number_of_attempts > self.MUTATE_AFTER_ATTEMPT:
                for c in offsprings_to_add:
                    self._mutator.mutate(c, number_of_attempts - self.MUTATE_AFTER_ATTEMPT)
            number_of_added_candidate_solutions += population.add_not_contained_candidate_solutions(offsprings_to_add)
            offsprings_to_add.clear()
            if number_of_added_candidate_solutions >= 2:
                candidate_solutions_added = True
        if number_of_added_candidate_solutions < 2:
            new_offsprings = self._mate_pair(
                candidate_solution1, candidate_solution2, population
            )
            for i in range(number_of_added_candidate_solutions, 2):
                population.add_candidate_solution(new_offsprings[i])

    def _mate_pair_once(self, population, candidate_solution1, candidate_solution2 ) -> None:
        population.add_candidate_solutions(list(self._mate_pair(
            candidate_solution1, candidate_solution2, population
        )))

    def mate(self, candidate_solution_pairs: List[Tuple[CandidateSolution, CandidateSolution]], population):
        """
        Returns list of candidate solution pairs using parents' genetic material

        Args:
            candidate_solution_pairs (List[Tuple[CandidateSolution, CandidateSolution]]) : List of candidate solution pairs for mating
            population: Population
        """
        for candidate_solution1, candidate_solution2 in candidate_solution_pairs:
            if len(population) >= population.options.population_size:
                break
            if population.options.ensure_unique_individuals:
                self._mate_pair_until_added(population, candidate_solution1, candidate_solution2)
            else:
                self._mate_pair_once(population, candidate_solution1, candidate_solution2)

        current_len = len(population)
        candidate_solution_surplus = current_len - population.options.population_size
        if candidate_solution_surplus > 0:
            sorted_by_cost_value = sorted(
                population, key=lambda candidate_solution: candidate_solution.cost_value, reverse=True
            )
            ids_to_remove = set()
            for c in sorted_by_cost_value:
                if len(ids_to_remove) >= candidate_solution_surplus:
                    break
                if not math.isnan(c.cost_value):
                    ids_to_remove.add(id(c))
            # remove by identity - equal candidate solutions must not be removed instead
            population.candidate_solutions[:] = [
                c for c in population.candidate_solutions if id(c) not in ids_to_remove
            ]

    def _mate_pair(
        self, mother: CandidateSolution, father: CandidateSolution, population
    ):
        """Returns two offspring candidate solutions using parents' genetic material

        Args:
            mother (CandidateSolution): The first candidate solution for mating
            father (CandidateSolution): The second candidate solution for mating
            population: Population

        Returns:
            CandidateSolution: the first offspring candidate solution
            CandidateSolution: the second offspring candidate solution
        """
        if len(mother) != len(father):
            raise Exception("Mother and father must have the same number of decision variables!")
        self._mother = mother
        self._father = father
        self._offspring1 = CandidateSolution(population.population_generation)
        self._offspring2 = CandidateSolution(population.population_generation)
        c_o_p = self._get_crossover_probability(population)
        if math.isnan(c_o_p):
            # A NaN probability is never reached by random(), so the loop below would never end
            raise Exception("Crossover probability is not a number!")
        crossed = self._cross_genetic_material(c_o_p)
        while not crossed:
            c_o_p += 0.1
            c_o_p = min(c_o_p, 1.0)
            self._offspring1 = CandidateSolution(population.population_generation)
            self._offspring2 = CandidateSolution(population.population_generation)
            crossed = self._cross_genetic_material(c_o_p)

        self._offspring1.mother_id = self._mother.candidate_solution_id
        self._offspring2.mother_id = self._mother.candidate_solution_id
        self._offspring1.father_id = self._father.candidate_solution_id
        self._offspring2.father_id = self._father.candidate_solution_id
        self._all_decision_variables_crossed()
        self._increase_generation()

        return self._offspring1, self._offspring2

    def _cros_genetic_variables(self, crossover_probability: float):
        self._mother_variable_value, self._father_variable_value = self._get_mother_father_variable_value()
        decision_variable_father = self._mother_variable_value.decision_variable
        decision_variable_mother = self._father_variable_value.decision_variable
        if decision_variable_father != decision_variable_mother:
            decision_variable_mother = next(
                (item.decision_variable for item in self._mother if item.decision_variable == decision_variable_father),
                None,
            )
        if decision_variable_mother is None:
            raise Exception(
                "candidate solutions in crossover do not have the same structure!"
            )
        self._decision_variable_crossed()
        random_value = random.random()
        are_variables_crossed = False
        if random_value <= crossover_probability:
            var1, var2 = self._combine()
            are_variables_crossed = True
        else:
            var1, var2 = self._mother_variable_value.value, self._father_variable_value.value,
        self._offspring1.add_variable_value(decision_variable_father, var1)
        self._offspring2.add_variable_value(decision_variable_father, var2)
        return are_variables_crossed

    def _cross_genetic_material(self, crossover_prob: float):
        self._candidate_solution_updater.candidate_solution_start_update()
        number_of_decision_variables = len(self._father)
        are_variables_crossed = False
        for self._current_decision_variable_number in range(number_of_decision_variables):
            are_variables_crossed = self._cros_genetic_variables(crossover_prob) or are_variables_crossed
        return are_variables_crossed


    def _get_mother_father_variable_value(self) -> Tuple[VariableValue, VariableValue]:
        if self._current_decision_variable_number == -1:
            raise Exception("_current_decision_variable_number not set")
        father_variable_value = self._father[self._current_decision_variable_number]
        mother_variable_value = self._mother[self._current_decision_variable_number]
        return mother_variable_value, father_variable_value

    @abstractmethod
    def _combine(self):
        pass

    def _get_crossover_probability(self, population) -> float:
        return self.crossover_rate_determinator.get_crossover_probability(population)

    def _increase_generation(self):
        current_generation = self._mother.candidate_solution_generation
        if (
            current_generation == 0
            or current_generation < self._father.candidate_solution_generation
        ):
            current_generation = self._father.candidate_solution_generation
        current_generation += 1
        self._offspring1.candidate_solution_generation = current_generation
        self._offspring2.candidate_solution_generation = current_generation

        current_generation = 0
        if (
            self._mother.first_mutant_generation > 0
            or self._father.first_mutant_generation > 0
        ):
            current_generation = self._mother.first_mutant_generation
            if (
                current_generation == 0
                or self._father.first_mutant_generation > current_generation
            ):
                current_generation = self._father.first_mutant_generation
            current_generation += 1
        self._offspring1.first_mutant_generation = current_generation
        self._offspring2.first_mutant_generation = current_generation

        current_generation = 0
        if (
            self._mother.last_mutant_generation > 0
            or self._father.last_mutant_generation > 0
        ):
            current_generation = self._mother.last_mutant_generation
            if current_generation == 0 or (
                0 < self._father.last_mutant_generation < current_generation
            ):
                current_generation = self._father.last_mutant_generation
            current_generation += 1
        self._offspring1.last_mutant_generation = current_generation
        self._offspring2.last_mutant_generation = current_generation

        current_generation = 0
        if (
            self._mother.first_immigrant_generation > 0
            or self._father.first_immigrant_generation > 0
        ):
            current_generation = self._mother.first_immigrant_generation
            if (
                current_generation == 0
                or self._father.first_immigrant_generation > current_generation
            ):
                current_generation = self._father.first_immigrant_generation
            current_generation += 1
        self._offspring1.first_immigrant_generation = current_generation
        self._offspring2.first_immigrant_generation = current_generation

        current_generation = 0
        if (
            self._mother.last_immigrant_generation > 0
            or self._father.last_immigrant_generation > 0
        ):
            current_generation = self._mother.last_immigrant_generation
            if current_generation == 0 or (
                0 < self._father.last_immigrant_generation < current_generation
            ):
                current_generation = self._father.last_immigrant_generation
            current_generation += 1
        self._offspring1.last_immigrant_generation = current_generation
        self._offspring2.last_immigrant_generation = current_generation

    def _decision_variable_crossed(self):
        self._candidate_solution_updater.candidate_solution_prepare_update(
            mother_variable_value=self._mother_variable_value, father_variable_value=self._father_variable_value
        )

    def _all_decision_variables_crossed(self):
        self._candidate_solution_updater.candidate_solution_update(
            offspring1=self._offspring1, offspring2=self._offspring2, father=self._father, mother=self._mother
        )
