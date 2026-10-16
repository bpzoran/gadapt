from gadapt.operations.immigration.candidate_solution_immigration.base_candidate_solution_immigrator import (
    BaseCandidateSolutionImmigrator,
)


class RandomCandidateSolutionImmigrator(BaseCandidateSolutionImmigrator):
    """
    New immigrated candidate solution with random decision variables
    """

    def _immigrate_candidate_solution(self):
        for g in self.candidate_solution:
            g.set_random_value()
