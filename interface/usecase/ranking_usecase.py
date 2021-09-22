from abc import ABCMeta, abstractmethod


class RankingUsecase(metaclass=ABCMeta):
    @abstractmethod
    def get_ranking(self) -> list:
        pass
