import math
from gadapt.operations.population_update.base_population_updater import (
    BasePopulationUpdater,
)


class CommonPopulationUpdater(BasePopulationUpdater):
    """
    Common population updater
    """

    def update_population(self, population):
        population.average_cost_step = population.calculate_average_cost_step()
        if math.isnan(population.average_cost_step_in_first_population):
            population.average_cost_step_in_first_population = (
                population.average_cost_step
            )
