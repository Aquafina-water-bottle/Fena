from abc import ABC, abstractmethod

class Builder(ABC):
    """
    Requires all classes to have a build function
    """
    @abstractmethod
    def build(self):
        pass