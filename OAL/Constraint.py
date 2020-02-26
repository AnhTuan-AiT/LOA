class Constraint(object):
    n_constraints = 0

    def __init__(self, name):
        Constraint.n_constraints += 1
        self.name = name if name is not '' else f'constraint {Constraint.n_constraints}'

class Eq(Constraint):
    '''Create equal constraint'''

    def __init__(self, linear_expr, const, name = ''):
        super().__init__(name)
        self.__const = const
        self.linear_expr = linear_expr
        self.id = 0

    @property
    def violation(self):
        return 0 if self.linear_expr.curr_value == self.__const else 1


class Le(Constraint):
    '''Create less or equal constraint'''

    def __init__(self, linear_expr, const, name = ''):
        super().__init__(name)
        self.__const = const
        self.linear_expr = linear_expr
        self.id = 0

    @property
    def violation(self):
        return 0 if self.linear_expr.curr_value <= self.__const else 1


class Ge(Constraint):
    '''Create greater or equal constraint'''

    def __init__(self, linear_expr, const, name = ''):
        super().__init__(name)
        self.__const = const
        self.linear_expr = linear_expr
        self.id = 0

    @property
    def violation(self):
        return 0 if self.linear_expr.curr_value >= self.__const else 1