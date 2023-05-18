from abc import ABC, abstractmethod
from ParamHandler import ParamHandler

class Regressor(ABC):

    @abstractmethod
    def __init__(self, params: ParamHandler) -> None:
        pass

    @abstractmethod
    def fit(self) -> None:
        pass
