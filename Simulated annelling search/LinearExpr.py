class LinearExpr:
    """Create linear express"""

    def __init__(self):
        self.__terms = [[], []]
        self.__value = 0

    def add_term(self, coefficient, d_var):
        """
        Add a term to expression
        :param coefficient:
        :param d_var:
        :return: None
        """
        self.__terms[0].append(coefficient)
        self.__terms[1].append(d_var)

    @property
    def d_vars(self):
        """
        :return: a list of decision variables in the expression
        """
        return self.__terms[1]

    @property
    def curr_value(self):
        """
        :return: current value of expression
        """
        self.__value = 0

        for i in range(len(self.__terms[0])):
            self.__value += self.__terms[0][i] * self.__terms[1][i].curr_value

        return self.__value
