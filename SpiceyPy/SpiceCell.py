__author__ = 'Apollo117'
from collections import UserList


class SpiceCell(UserList):
    _isSet = True

    def scard(self, card):
        pass

    def ssize(self, size):
        pass

    def appndx(self, item):
        self.append(item)
        self.sort()

    def card(self):
        return self.__len__()

    @property
    def isSet(self):
        test = self.__len__() == len(set(self))
        if self._isSet != test:
            self._isSet = test
        return self._isSet