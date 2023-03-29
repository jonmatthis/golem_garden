from abc import ABC, abstractmethod

class BaseDatabase(ABC):
    @abstractmethod
    def add_user_message(self, user_id, golem_id, message):
        pass

    @abstractmethod
    def add_golem_response(self, user_id, golem_id, response):
        pass

    @abstractmethod
    def get_history(self, user_id, golem_id, this_session_only:bool=True):
        pass
