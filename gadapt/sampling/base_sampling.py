from typing import List
from gadapt.ga_model.ranking_model import RankingModel
import gadapt.ga_model.definitions as definitions
class BaseSampling:

    """
    The algorithm for extracting a sample from the population.
    """

    def get_sample(self, lst: List[RankingModel], max_num, sort_key=None) -> List[RankingModel]:
        """
        Gets the sample from the list of RankingModel objects.
        Args:
            lst (List[RankingModel]): list of RankingModel objects to get the sample
            max_num: (int): Maximal number of objects in the sample
            sort_key: sorting key for the sample
        """
        if len(lst) == 0:
            return lst
        for m in lst:
            m.reset_for_sampling()
        if max_num < 1 or max_num > len(lst):
            self.max_num = len(lst)
        else:
            self.max_num = max_num
        self._sort_key = sort_key
        return self._prepare_sample(lst)
    
    def _prepare_sample(self, lst: List[RankingModel]) -> List[RankingModel]:
        raise Exception(definitions.NOT_IMPLEMENTED)