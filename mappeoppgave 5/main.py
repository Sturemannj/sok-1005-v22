import random

try:
    import numpy as np
except:
    pass


class BaseStrategy(object):
    """
    Grunnklasse for Blotto-strategi
    """

    def __init__(self, name):
        self.name = name
        self.num_fields = None
        self.num_runs = None

        self.opponent_allocations = []
        self.past_scores = []

    def __repr__(self):
        return "%s:%s" % (self.__class__.__name__, self.name)

    def initialise(self, num_fields, num_runs):
        """
        før kampen starter
        fjerner historikk registrert fra den siste motstanderen
        """
        self.num_fields = num_fields
        self.num_runs = num_runs
        self.opponent_allocations = []
        self.past_scores = []

    def soldiers_request(self, iteration):
        """
        Denne metoden vil bli kalt hver tur for å be om tildeling av soldater

        returner en liste over positive heltall med sum mindre enn eller lik 100
        """
        pass

    def post_results(self, score, soldiers_B, check_B):
        """
        Denne metoden vil bli kalt etter hvert enkelt spill er løst.
        Den forteller deg poengsummen (positivt du vant, negativt du tapte)
        Den forteller deg hva motstanderens soldattildeling va
        Den forteller deg om motstandernes tildeling ble ansett som gyldig
        """
        self.past_scores.append(score)
        self.opponent_allocations.append(soldiers_B)


class UsageError(Exception):
    pass


class RandomStyle(object):
    NUMBER = 0
    DRAW = 1
    DIRICHLET = 2
    UNIFORM = 3

    @classmethod
    def get_name(cls, num):
        for k, v in cls.__dict__.iteritems():
            if v == num:
                return k
        else:
            raise Exception("RandomStyle not found: %s" % num)


class RandomStrategy(BaseStrategy):
    def __init__(self, name, weightings=None, shuffle=False, style=None):
        super(RandomStrategy, self).__init__(name)
        if style is None:
            self.style = RandomStyle.NUMBER
        else:
            self.style = style

        if self.style != RandomStyle.UNIFORM:
            assert weightings is not None
            assert abs(sum(weightings) - 1.0) < 1e-6, "weightings: %s" % weightings
            self.weightings = weightings

        self.shuffle = shuffle

    def soldiers_request(self, iteration):
        if self.style == RandomStyle.NUMBER:
            strategy = random_number_allocation(weightings=self.weightings)

        elif self.style == RandomStyle.DRAW:
            strategy = random_draw_allocation(weightings=self.weightings)

        elif self.style == RandomStyle.DIRICHLET:
            strategy = dirichlet_allocation(weightings=self.weightings)

        elif self.style == RandomStyle.UNIFORM:
            strategy = get_allocation_uniform(self.num_fields)

        else:
            raise UsageError("Style not recognised: %s" % RandomStyle.get_name(self.style))

        if self.shuffle:
            return sorted(strategy, key=lambda k: random.random())
        else:
            return strategy


def random_draw_allocation(weightings, number=100):
    """ setter en soldat i et tilfeldig felt 100 ganger, ifølge vektingene """
    assert abs(sum(weightings) - 1.0) < 1e-6
    result = [0.0 for _ in weightings]
    for _ in range(number):
        result[weighted_draw(weightings)] += 1

    return result


def random_number_allocation(weightings, number=100):
    """
    Tildeler soldater til felt i henhold til den relative størrelsen på flere tilfeldige tall
    Gjennomsnittet i hvert felt vil være i forhold til de beståtte vektingene
    """
    assert abs(sum(weightings) - 1.0) < 1e-6
    result = []
    for w in weightings:
        result.append(random.random() * w)
    result = [int(number * r / sum(result)) for r in result]

    while sum(result) != number:
        if sum(result) > number:
            result[weighted_draw(weightings)] -= 1
        else:
            result[weighted_draw(weightings)] += 1
    return result


def dirichlet_allocation(weightings, number=100):
    """
    Tildeler soldater til felt etter dirichletfordeling
    Vekting er gjennomsnittlig andel soldater i hvert felt

    """
    assert abs(sum(weightings) - 1.0) < 1e-6
    result = [int(r) for r in np.random.dirichlet(weightings) * number]

    while sum(result) != number:
        if sum(result) > number:
            result[weighted_draw(weightings)] -= 1
        else:
            result[weighted_draw(weightings)] += 1
    return result


def get_allocation_uniform(num_fields, num_soldiers=100):
    """ får en tildeling jevnt fra alle mulige tildelinger."""
    dividers = sorted(random.sample(range(1, num_soldiers + num_fields), num_fields - 1))
    return [a - b - 1 for a, b in zip(dividers + [num_soldiers + num_fields], [0] + dividers)]


def weighted_draw(weightings):
    """
    Tegn et tall fra 0->(N-1)
    i henhold til vektene som er gitt (length N)
    """
    assert abs(1.0 - sum(weightings)) < 0.00001, "%s sum: %s" % (weightings, sum(weightings))
    r = random.random()
    for i, w in enumerate(weightings):
        if r <= w:
            return i
        r -= w
