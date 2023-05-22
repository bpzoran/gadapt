from exit_check.avg_cost_exit_checker import AvgCostExitChecker
from exit_check.base_exit_checker import BaseExitChecker
from exit_check.min_cost_exit_checker import MinCostExitChecker
from exit_check.requested_cost_exit_checker import RequestedCostExitChecker
from cost_finding.base_cost_finder import BaseCostFinder
from cost_finding.common_cost_finder import CommonCostFinder
from crossover.base_crossover import BaseCrossover
from crossover.uniform_crossover import UniformCrossover
from ga_model.ga_options import GAOptions
from immigration.chromosome_immigration.base_chromosome_immigrator import BaseChromosomeImmigrator
from immigration.chromosome_immigration.random_chromosome_immigrator import RandomChromosomeImmigrator
from immigration.population_immigration.base_population_immigrator import BasePopulationImmigrator
from immigration.population_immigration.common_population_immigrator import CommonPopulationImmigrator
from mutation.chromosome_mutation.base_chromosome_mutator import BaseChromosomeMutator
from mutation.chromosome_mutation.cross_diversity_chromosome_mutator import CrossDiversityChromosomeMutator
from mutation.chromosome_mutation.random_chromosome_mutator import RandomChromosomeMutator
from mutation.population_mutation.base_population_mutator import BasePopulationMutator
from mutation.population_mutation.composed_population_mutator import ComposedPopulationMutator
from mutation.population_mutation.cost_diversity.cost_diversity_population_mutator import CostDiversityPopulationMutator
from mutation.population_mutation.parents_diversity_population_mutator import ParentsDiversityPopulationMutator
from mutation.population_mutation.previous_cost_diversity.previous_cost_diversity_population_mutator import PreviousCostDiversityPopulationMutator
from mutation.population_mutation.previous_cost_diversity.previous_cost_diversity_property_taker import AvgPreviousCostCostDiversityPropertyTaker, BasePreviousCostDiversityPropertyTaker, MinPreviousCostCostDiversityPropertyTaker
from mutation.population_mutation.random_population_mutator import RandomPopulationMutator
from parent_selection.base_parent_selector import BaseParentSelector
from parent_selection.sampling_parent_selector import SamplingParentSelector
from sampling.base_sampling import BaseSampling
from sampling.from_top_to_bottom_sampling import FromTopToBottomSampling
from sampling.random_sampling import RandomSampling
from sampling.roulette_wheel_sampling import RouletteWheelSampling
from sampling.tournament_sampling import TournamentSampling
from validation.base_options_validator import BaseOptionsValidator
from validation.common_options_validator import CommonOptionsValidator
from gene_combination.base_gene_combination import BaseGeneCombination
from gene_combination.blending_gene_combination import BlendingGeneCombination
from variable_update.common_variable_updater import CommonVariableUpdater
import ga_model.definitions


class GAFactory:
    def __init__(self, ga) -> None:
        self.ga_options = ga

    @property
    def ga_options(self):
        return self._ga_options

    @ga_options.setter
    def ga_options(self, value):
        self._ga_options = value

    def get_cost_finder(self) -> BaseCostFinder:
        return CommonCostFinder()

    def get_population_immigrator(self) -> BasePopulationImmigrator:
        return CommonPopulationImmigrator()

    def get_chromosome_immigrator(self) -> BaseChromosomeImmigrator:
        return RandomChromosomeImmigrator()

    def get_chromosome_mutator(self) -> BaseChromosomeMutator:
        if self.ga_options.chromosome_mutation.strip() == ga_model.definitions.CROSS_DIVERSITY:
            return CrossDiversityChromosomeMutator(self.get_sampling_method(self.ga_options.cross_diversity_mutation_gene_selection))
        elif self.ga_options.chromosome_mutation.strip() == ga_model.definitions.RANDOM:
            return RandomChromosomeMutator()
        else:
            raise Exception("unknown chromosome mutation")

    def population_mutator_options_validation(self):
        mutator_strings = self.ga_options.population_mutation.split(ga_model.definitions.PARAM_SEPARATOR)
        for s in mutator_strings:
            if not s.strip() in ga_model.definitions.POPULATION_MUTATOR_STRINGS:
                raise Exception(s + " is not defined as option for population mutation")

    def get_population_mutator(self, population_mutator_string=None) -> BasePopulationMutator:
        self.population_mutator_options_validation()
        if population_mutator_string is None:
            population_mutator_string = self.ga_options.population_mutation.strip()
        if population_mutator_string.find(ga_model.definitions.PARAM_SEPARATOR) > -1:
            return self.get_population_mutator_combined()
        elif population_mutator_string == ga_model.definitions.COST_DIVERSITY:
            return CostDiversityPopulationMutator(self.ga_options, ParentsDiversityPopulationMutator(self.get_sampling_method(self.ga_options.parent_diversity_mutation_chromosome_selection), self.ga_options))
        elif population_mutator_string == ga_model.definitions.PARENTS_DIVERSITY:
            return ParentsDiversityPopulationMutator(self.get_sampling_method(self.ga_options.parent_diversity_mutation_chromosome_selection), self.ga_options)
        elif population_mutator_string == ga_model.definitions.RANDOM:
            return RandomPopulationMutator(self.ga_options)
        else:
            raise Exception("unknown population mutation")

    def get_previous_cost_diversity_property_taker(self) -> BasePreviousCostDiversityPropertyTaker:
        return AvgPreviousCostCostDiversityPropertyTaker()

    def get_population_mutator_combined(self) -> ComposedPopulationMutator:
        mutator_strings = [ms.strip() for ms in self.ga_options.population_mutation.split(ga_model.definitions.PARAM_SEPARATOR)]
        if (self.is_cost_diversity_random(mutator_strings)):
            return CostDiversityPopulationMutator(self.ga_options, RandomPopulationMutator(self.ga_options))
        if (self.is_cost_diversity_parents_diversity(mutator_strings)):
            return CostDiversityPopulationMutator(self.ga_options, ParentsDiversityPopulationMutator(self.get_sampling_method(self.ga_options.parent_diversity_mutation_chromosome_selection), self.ga_options))
        if self.is_cost_diversity_parents_diversity_random(mutator_strings):
            composedPopulationMutator = ComposedPopulationMutator(self.ga_options)
            composedPopulationMutator.append(ParentsDiversityPopulationMutator(self.get_sampling_method(
                self.ga_options.parent_diversity_mutation_chromosome_selection), self.ga_options))
            composedPopulationMutator.append(
                RandomPopulationMutator(self.ga_options))
            return PreviousCostDiversityPopulationMutator(self.ga_options, composedPopulationMutator)
        composedPopulationMutator = ComposedPopulationMutator(self.ga_options)
        for ms in mutator_strings:
            composedPopulationMutator.append(self.get_population_mutator(ms))
        return composedPopulationMutator

    def is_cost_diversity_random(self, mutator_strings: list):
        if len(mutator_strings) == 2 and ga_model.definitions.COST_DIVERSITY in mutator_strings and ga_model.definitions.RANDOM in mutator_strings:
            return True
        return False

    def is_cost_diversity_parents_diversity(self, mutator_strings: list):
        if len(mutator_strings) == 2 and ga_model.definitions.COST_DIVERSITY in mutator_strings and ga_model.definitions.PARENTS_DIVERSITY in mutator_strings:
            return True
        return False

    def is_cost_diversity_parents_diversity_random(self, mutator_strings: list):
        if len(mutator_strings) == 3 and ga_model.definitions.COST_DIVERSITY in mutator_strings and ga_model.definitions.PARENTS_DIVERSITY in mutator_strings and ga_model.definitions.RANDOM in mutator_strings:
            return True
        return False

    def get_parent_selector(self) -> BaseParentSelector:
        return SamplingParentSelector(self.get_sampling_method(self.ga_options.parent_selection))

    def get_sampling_method(self, str) -> BaseSampling:
        str_value = str
        sampling_method_strings = str.split(ga_model.definitions.PARAM_SEPARATOR)
        other_value = None
        if len(sampling_method_strings) > 1:
            str_value = sampling_method_strings[0]
            try:
                other_value = int(sampling_method_strings[1])
            except:
                pass
        if str_value == ga_model.definitions.TOURNAMENT:
            return TournamentSampling(other_value)
        elif str_value == ga_model.definitions.FROM_TOP_TO_BOTTOM:
            return FromTopToBottomSampling()
        elif str_value == ga_model.definitions.RANDOM:
            return RandomSampling()
        return RouletteWheelSampling()

    def get_gene_combination(self) -> BaseGeneCombination:
        return BlendingGeneCombination()

    def get_exit_checker(self) -> BaseExitChecker:
        if self.ga_options.exit_check == ga_model.definitions.AVG_COST:
            return AvgCostExitChecker(self.ga_options.max_attempt_no)
        if self.ga_options.exit_check == ga_model.definitions.MIN_COST:
            return MinCostExitChecker(self.ga_options.max_attempt_no)
        return RequestedCostExitChecker(self.ga_options.requested_cost)

    def get_crossover(self, gene_combination: BaseGeneCombination, mutator: BaseChromosomeMutator, immigrator: BaseChromosomeImmigrator) -> BaseCrossover:
        return UniformCrossover(gene_combination, mutator, immigrator)

    def get_variable_updater(self):
        return CommonVariableUpdater()
    
    def get_options_validator(self) -> BaseOptionsValidator:
        return CommonOptionsValidator(self.ga_options)
