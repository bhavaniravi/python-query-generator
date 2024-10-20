from abc import ABC, abstractmethod


class BaseQueryGenerator(ABC):
    @abstractmethod
    def generate_query(self, config):
        pass
