from typing import List
from gadapt.ga_model.ranking_model import RankingModel
from gadapt.sampling.base_sampling import BaseSampling

class FromTopToBottomSampling(BaseSampling):

    def prepare_sample(self, lst: List[RankingModel]) -> List[RankingModel]:
        members_for_action = sorted(lst, key=self.sort_key)
        return [m.replace_rank(rank) for rank, m in enumerate(members_for_action[:self.max_num])]
        