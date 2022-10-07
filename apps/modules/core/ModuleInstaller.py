from abc import ABC, abstractmethod

class ModuleInstaller(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_modules(self):
        pass

    @abstractmethod
    def install_modules(self, modules):
        pass