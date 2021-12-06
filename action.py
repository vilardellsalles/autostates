from abc import ABC, abstractmethod


class Action(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    def requires(self):
        pass

    def provides(self):
        pass

    def execute(self):
        pass
