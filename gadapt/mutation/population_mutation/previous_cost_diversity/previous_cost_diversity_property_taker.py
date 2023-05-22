import ga_model.definitions
class BasePreviousCostDiversityPropertyTaker:
    def take_property(self, mutator):
        raise Exception(ga_model.definitions.NOT_IMPLEMENTED)
    
class MinPreviousCostCostDiversityPropertyTaker:
    def take_property(self, mutator):
        return mutator.previous_min_costs
    
class AvgPreviousCostCostDiversityPropertyTaker:
    def take_property(self, mutator):
        return mutator.previous_avg_costs    