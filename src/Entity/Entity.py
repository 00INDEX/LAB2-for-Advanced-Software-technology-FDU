from abc import ABCMeta, abstractmethod


class Entity(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass
