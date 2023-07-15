from Database.baseStorage import BaseStorage


class MemoryStorage(BaseStorage):
    def __init__(self):
        self.dictionary = {}

    def get_data(self, table, param):
        if param in self.dictionary.keys():
            return self.dictionary[param]
        raise "Database error"

    def set_data(self, table, param, data):
        if param in self.dictionary.keys():
            raise "Database error"
        self.dictionary.update({param: data})

    def update_data(self, table, param, data):
        if param in self.dictionary.keys():
            self.dictionary.update({param: data})
        raise "Database error"


