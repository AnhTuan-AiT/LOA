from OAL.DVar import DVar

class LinearExpr:
    '''Create linear express'''

    def __init__(self):
        self.__terms = [[], []]

    def add_term(self, coefficient, dvar):
        self.__terms[0].append(coefficient)
        self.__terms[1].append(dvar)

    @property
    def dvar(self):
        return self.__terms[1]
    @property
    def curr_value(self):
        curr_value = 0

        for i in range(len(self.__terms[0])):
            curr_value += (self.__terms[0][i]) * (self.__terms[1][i].value)

        return curr_value