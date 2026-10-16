from typing import List

from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.operations.immigration.population_immigration.base_population_immigrator import (
    BasePopulationImmigrator,
)


class CommonPopulationImmigrator(BasePopulationImmigrator):
    """
    Common class for the self.population immigration.
    In kept part of the self.population lower ranked candidate solutions are replaced with new ones
    """

    def _immigrate_population(self):
        if self.population.options.immigration_number < 1:
            return
        keep_number = self.population.options.keep_number
        candidate_solution_list: List[CandidateSolution] = list(
            self.population.get_sorted(key=lambda c: c.cost_value)
        )[:keep_number]
        candidate_solution_list = sorted(
            candidate_solution_list, key=lambda c: (-c.cost_value, -c.candidate_solution_id)
        )[: self.population.options.immigration_number]
        for c in candidate_solution_list:
            self._candidate_solution_immigrator.immigrate(c)
            c.population_generation = self.population.population_generation
