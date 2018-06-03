__author__ = 'PERVasive'

import collections
import statistics
import random

random.seed()

# h is the half life of water consumed before it gets absorbed, in minutes
h = float(30)
# default_capacity is 500 mL, the accepted figure for human bladder size
# this is known to be low for Omo players, but it is better to err low
default_capacity = 500
# after asking permission, we cannot ask again until bladder has increased
# by fullness_quantum. Should probably be something like 150-300 mL
fullness_quantum = 150


class Permission(collections.namedtuple('Permission', ['time', 'permission'])):
    pass


class Drink(collections.namedtuple('Drink', ['time', 'amount'])):
    def unabsorbed(self, t):
        if t > self.time:
            return (2 ** ((self.time - t) / h)) * self.amount
        else:
            return self.amount


class Release(collections.namedtuple('Release', ['time', 'amount', 'permission'])):
    pass


class Drinker(object):
    def __init__(self):
        self._history = []
        self._permission = Permission(None, False)

    @property
    def history(self):
        return self._history[:]

    @history.setter
    def history(self, value):
        self._history = sorted(value, key=lambda el: el.time)

    @property
    def drinks(self):
        return [el for el in self._history if isinstance(el, Drink)]

    @property
    def releases(self):
        return [el for el in self._history if isinstance(el, Release)]

    @property
    def accidents(self):
        return [el for el in self._history if isinstance(el, Release) and not el.permission]

    @property
    def capacity(self):
        if self.accidents:
            new_cap = statistics.mean(el.amount for el in self.accidents)
            return new_cap if new_cap else default_capacity
        else:
            return default_capacity

    def absorbed(self, t):
        return sum(el.amount - el.unabsorbed(t) for el in self.drinks)

    def bladder(self, t):
        return self.absorbed(t) - sum(el.amount for el in
                                      self.releases if el.time <= t)

    def add_drink(self, t, amount):
        self.history += [Drink(t, amount)]

    def add_release(self, t, permission):
        self.history += [Release(t, self.bladder(t), permission)]

    def desperation(self, t):
        # Normalize holding over capacity down to 1.0
        # So that permission is always possible
        fullness = self.bladder(t)/float(self.capacity)
        return 1.0 if fullness > 1.0 else fullness

    @property
    def permission(self):
        return self._permission.permission

    def roll_allowed(self, t):
        if not self._permission.time:
            return True
        else:
            return self.bladder(t) - self.bladder(self._permission.time) > fullness_quantum

    def roll_for_permission(self, t):
        # 10% chance of guaranteed yes or no
        roll = random.random()*1.2 - 0.1
        answer = roll > self.desperation(t)
        self._permission = Permission(t, answer)
        return answer
