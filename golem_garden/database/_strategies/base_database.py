from abc import ABC, abstractmethod

class BaseDatabase(ABC):
    @abstractmethod
    def add_message(self, subject_id, golem_id, message):
        pass

    @abstractmethod
    def add_response(self, subject_id, golem_id, response):
        pass

    @abstractmethod
    def get_history(self, query_dict):
        pass
