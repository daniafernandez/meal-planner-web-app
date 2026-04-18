from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError
