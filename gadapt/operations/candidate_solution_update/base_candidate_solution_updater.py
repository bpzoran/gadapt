from gadapt.ga_model.candidate_solution import CandidateSolution
from gadapt.ga_model.variable_value import VariableValue


class BaseCandidateSolutionUpdater:
    """
    Updates candidate solution
    """

    def candidate_solution_prepare_update(self, mother_variable_value: VariableValue, father_variable_value: VariableValue):
        pass

    def candidate_solution_update(self, offspring1: CandidateSolution, offspring2: CandidateSolution, mother: CandidateSolution, father: CandidateSolution):
        pass

    def candidate_solution_start_update(self, *args, **kwargs):
        pass
