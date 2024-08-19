from abc import ABC, abstractmethod

class ExtractionStrategy(ABC):
    @abstractmethod
    def extract_data(self, text):
        pass
