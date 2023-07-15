from abc import ABCMeta, abstractmethod


class BaseStorage:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self, table, param):
        """get data from db"""

    @abstractmethod
    def set_data(self, table, param, data):
        """set data to db"""

    @abstractmethod
    def update_data(self, table, param, data):
        """update data"""

