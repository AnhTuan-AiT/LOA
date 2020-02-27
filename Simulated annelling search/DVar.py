class DVar:
    """Decision variable"""

    def __init__(self, manager, min_value, max_value, name):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.__manager = manager
        self.__value = min_value

    @property
    def curr_value(self):
        """
        :return: current value of decision variable
        """

        return self.__value

    @curr_value.setter
    def curr_value(self, new_value):
        if (new_value < self.min_value or new_value > self.max_value):
            raise ValueError('Value out of domain')
        else:
            self.__value = new_value