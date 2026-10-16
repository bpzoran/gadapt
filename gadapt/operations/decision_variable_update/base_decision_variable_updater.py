class BaseDecisionVariableUpdater:
    """
    Base class for variable update
    """

    def __init__(self):
        self.population = None

    def update_decision_variables(self, population):
        self.population = population
        self._update_decision_variables()

    def _update_decision_variables(self):
        pass
