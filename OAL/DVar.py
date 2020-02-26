from OAL.Manager import Manager
class DVar:
    '''Decision variable'''

    def __init__(self, manager, min_value, max_value, name):
        self.name = name
        self.__manager = manager
        self.min_value = min_value
        self.max_value = max_value
        self.__value = self.min_value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if (new_value < self.min_value or new_value > self.max_value):
            raise ValueError('Value out of bound')
        else:
            self.__value = new_value