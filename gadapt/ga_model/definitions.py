"""
Genetic algorithm definitions
"""

RANDOM = "random"
COST_DIVERSITY = "cost_diversity"
PARENT_DIVERSITY = "parent_diversity"
CROSS_DIVERSITY = "cross_diversity"
TOURNAMENT = "tournament"
FROM_TOP_TO_BOTTOM = "from_top_to_bottom"
ROULETTE_WHEEL = "roulette_wheel"
AVG_COST = "avg_cost"
MIN_COST = "min_cost"
REQUESTED = "requested"
AVG = "avg"
MIN = "min"
PARAM_SEPARATOR = ","
FLOAT_NAN = float("NaN")
NOT_IMPLEMENTED = "not implemented"
EXTREME_POINTED = "extreme_pointed"
NORMAL_DISTRIBUTION = "normal_distribution"
POPULATION_MUTATOR_STRINGS = [COST_DIVERSITY, PARENT_DIVERSITY, RANDOM]
CHROMOSOME_MUTATOR_STRINGS = [RANDOM, CROSS_DIVERSITY]
SELECTION_STRINGS = [RANDOM, FROM_TOP_TO_BOTTOM, ROULETTE_WHEEL, TOURNAMENT]
EXIT_CRITERIA_STRINGS = [AVG_COST, MIN_COST, REQUESTED]
