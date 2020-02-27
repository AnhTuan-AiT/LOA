class Constraint:
    n_constraints = 0

    def __init__(self, expr, const, name):
        Constraint.n_constraints += 1
        self.name = name if name is not '' else f'constraint {Constraint.n_constraints}'
        self.expr = expr
        self.id = 0
        self.const = const


class Eq(Constraint):
    """Create equal constraint"""

    def __init__(self, expr, const, name=''):
        super().__init__(expr, const, name)

    @property
    def violation(self):
        return 0 if self.expr.curr_value == self.const else 1


class Le(Constraint):
    """Create less or equal constraint"""

    def __init__(self, expr, const, name = ''):
        super().__init__(expr, const, name)

    @property
    def violation(self):
        return 0 if self.expr.curr_value <= self.const else 1


class Ge(Constraint):
    """Create greater or equal constraint"""

    def __init__(self, expr, const, name = ''):
        super().__init__(expr, const, name)

    @property
    def violation(self):
        return 0 if self.expr.curr_value >= self.const else 1
