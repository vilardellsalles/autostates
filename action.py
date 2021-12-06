from abc import ABC, abstractmethod


class Action(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def requires(self):
        pass

    @abstractmethod
    def provides(self):
        pass

    @abstractmethod
    def execute(self):
        pass
