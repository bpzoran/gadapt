from abc import ABC, abstractmethod


class BaseDecisionVariableMutationRateDeterminator(ABC):
    def __init__(self) -> None:
        """
        Provides a framework for determining the number of mutation decision variables in a candidate solution.
        """
        super().__init__()
        self.max_number_of_mutation_decision_variables: int = -1

    def get_number_of_mutation_decision_variables(
        self, candidate_solution, max_number_of_mutation_decision_variables: int
    ):
        if max_number_of_mutation_decision_variables is None:
            raise Exception("max_number_of_mutation_decision_variables must not be None")
        if not candidate_solution:
            raise Exception("candidate solution must not be None")
        self.candidate_solution = candidate_solution
        self.max_number_of_mutation_decision_variables = max_number_of_mutation_decision_variables
        return self._get_number_of_mutation_decision_variables()

    @abstractmethod
    def _get_number_of_mutation_decision_variables(self) -> int:
        pass
