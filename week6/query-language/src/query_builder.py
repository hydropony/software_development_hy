from matchers import And, HasAtLeast, PlaysIn, Not, HasFewerThan, All, Or

class QueryBuilder:
    def __init__(self, matcher=All()):
        self.matcher = matcher

    def build(self):
        return self.matcher

    def plays_in(self, team: str):
        return QueryBuilder(And(PlaysIn(team), self.matcher))

    def has_at_least(self, value: int, attr: str):
        return QueryBuilder(And(HasAtLeast(value, attr), self.matcher))

    def has_fewer_than(self, value: int, attr: str):
        return QueryBuilder(And(HasFewerThan(value, attr), self.matcher))

    def one_of(self, *builders):
        return QueryBuilder(Or(*(b.matcher for b in builders)))