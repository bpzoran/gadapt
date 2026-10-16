from abc import ABC, abstractmethod
from typing import Optional

from gadapt.ga_model.ga_options import GAOptions
from gadapt.operations.cost_finding.base_cost_finder import BaseCostFinder
from gadapt.operations.crossover.base_crossover import BaseCrossover
from gadapt.operations.exit_check.base_exit_checker import BaseExitChecker
from gadapt.operations.immigration.candidate_solution_immigration.base_candidate_solution_immigrator import (
    BaseCandidateSolutionImmigrator,
)
from gadapt.operations.immigration.population_immigration.base_population_immigrator import (
    BasePopulationImmigrator,
)
from gadapt.operations.mutation.candidate_solution_mutation.base_decision_variable_mutation_selector import (
    BaseDecisionVariableMutationSelector,
)
from gadapt.operations.mutation.decision_variable_mutation.base_decision_variable_mutator import BaseDecisionVariableMutator
from gadapt.operations.parent_selection.base_parent_selector import BaseParentSelector
from gadapt.operations.mutation.population_mutation.base_candidate_solution_mutation_selector import (
    BaseCandidateSolutionMutationSelector,
)

"""
    Factory definition for creating  class instances based on GA options
"""


class BaseGAFactory(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.population_updater = None
        self._ga = None
        self._options = None
        self.decision_variable_updater = None
        self.candidate_solution_updater = None
        self.cost_finder: Optional[BaseCostFinder] = None
        self.population_immigrator: Optional[BasePopulationImmigrator] = None
        self.candidate_solution_immigrator: Optional[BaseCandidateSolutionImmigrator] = None
        self.decision_variable_mutator: Optional[BaseDecisionVariableMutator] = None
        self.decision_variable_mutation_selector: Optional[BaseDecisionVariableMutationSelector] = None
        self.candidate_solution_mutation_selector: Optional[BaseCandidateSolutionMutationSelector] = (
            None
        )
        self.parent_selector: Optional[BaseParentSelector] = None
        self.exit_checker: Optional[BaseExitChecker] = None
        self.crossover: Optional[BaseCrossover] = None

    def initialize_factory(self, ga, options: GAOptions):
        self._ga = ga
        self._options = options

    def get_cost_finder(self) -> BaseCostFinder:
        """
        Cost Finder instance
        """
        if self.cost_finder is None:
            self.cost_finder = self._get_cost_finder()
        return self.cost_finder

    def get_population_immigrator(self) -> BasePopulationImmigrator:
        """
        Population Immigrator Instance
        """
        if self.population_immigrator is None:
            self.population_immigrator = self._get_population_immigrator()
        return self.population_immigrator

    def get_candidate_solution_immigrator(self) -> BaseCandidateSolutionImmigrator:
        """
        Candidate Solution Immigrator Instance
        """
        if self.candidate_solution_immigrator is None:
            self.candidate_solution_immigrator = self._get_candidate_solution_immigrator()
        return self.candidate_solution_immigrator

    def get_decision_variable_mutation_selector(self) -> BaseDecisionVariableMutationSelector:
        """
        Decision Variable Mutation Selector Instance
        """
        if self.decision_variable_mutation_selector is None:
            self.decision_variable_mutation_selector = self._get_decision_variable_mutation_selector()
        return self.decision_variable_mutation_selector

    def get_decision_variable_mutator(self) -> BaseDecisionVariableMutator:
        """
        Decision Variable Mutator Instance
        """
        if self.decision_variable_mutator is None:
            self.decision_variable_mutator = self._get_decision_variable_mutator()
        return self.decision_variable_mutator

    def get_candidate_solution_mutation_selector(self) -> BaseCandidateSolutionMutationSelector:
        """
        Candidate Solution Mutation Selector Instance
        """
        if self.candidate_solution_mutation_selector is None:
            self.candidate_solution_mutation_selector = self._get_candidate_solution_mutation_selector()
        return self.candidate_solution_mutation_selector

    def get_parent_selector(self) -> BaseParentSelector:
        """
        Parent Selector Instance
        """
        if self.parent_selector is None:
            self.parent_selector = self._get_parent_selector()
        return self.parent_selector

    def get_exit_checker(self) -> BaseExitChecker:
        """
        Exit Checker Instance
        """
        if self.exit_checker is None:
            self.exit_checker = self._get_exit_checker()
        return self.exit_checker

    def get_decision_variable_updater(self):
        """
        Decision Variable Updater Instance
        """
        if self.decision_variable_updater is None:
            self.decision_variable_updater = self._get_decision_variable_updater()
        return self.decision_variable_updater

    def get_candidate_solution_updater(self):
        """
        Candidate Solution Updater Instance
        """
        if self.candidate_solution_updater is None:
            self.candidate_solution_updater = self._get_candidate_solution_updater()
        return self.candidate_solution_updater

    def get_population_updater(self):
        """
        Population Updater Instance
        """
        if self.population_updater is None:
            self.population_updater = self._get_population_updater()
        return self.population_updater

    def get_crossover(self) -> BaseCrossover:
        """
        Crossover Instance
        """
        if self.crossover is None:
            self.crossover = self._get_crossover()
        return self.crossover

    @abstractmethod
    def _get_cost_finder(self) -> BaseCostFinder:
        """
        Cost Finder instance
        """
        pass

    @abstractmethod
    def _get_population_immigrator(self) -> BasePopulationImmigrator:
        """
        Population Immigrator Instance
        """
        pass

    @abstractmethod
    def _get_candidate_solution_immigrator(self) -> BaseCandidateSolutionImmigrator:
        """
        Candidate Solution Immigrator Instance
        """
        pass

    @abstractmethod
    def _get_decision_variable_mutation_selector(self) -> BaseDecisionVariableMutationSelector:
        """
        Decision Variable Mutation Selector Instance
        """
        pass

    @abstractmethod
    def _get_decision_variable_mutator(self) -> BaseDecisionVariableMutator:
        """
        Decision Variable Mutator Instance
        """
        pass

    @abstractmethod
    def _get_candidate_solution_mutation_selector(self) -> BaseCandidateSolutionMutationSelector:
        """
        Population Mutator Instance
        """
        pass

    @abstractmethod
    def _get_parent_selector(self) -> BaseParentSelector:
        """
        Parent Selector Instance
        """
        pass

    @abstractmethod
    def _get_exit_checker(self) -> BaseExitChecker:
        """
        Exit Checker Instance
        """
        pass

    @abstractmethod
    def _get_decision_variable_updater(self):
        """
        Decision Variable Updater Instance
        """
        pass

    @abstractmethod
    def _get_candidate_solution_updater(self):
        """
        Candidate Solution Updater Instance
        """
        pass

    @abstractmethod
    def _get_population_updater(self):
        """
        Population Updater Instance
        """
        pass

    @abstractmethod
    def _get_crossover(self) -> BaseCrossover:
        """
        Crossover Instance
        """
        pass
