from typing import Any, Callable
from .functions import compose

class DataType():
    """ Base type
    """
    def __init__(self, value = None):
        self.__value = value

    def value(self):
        return self.__value

    def __eq__(self, other: 'DataType'):
        return self.__value == other.value()

    def __bool__(self):
        return self.__value is not None

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.__value)

class Functor(DataType):
    """ Functor type which can map between two categories.
    """
    def map(self, f: Callable[[Any], Any]) -> 'Functor':
        return type(self)(f(self.value()))

class Applicative(Functor):
    """ Applicative type which can apply functors to each other.
    """
    def apply(self, functor: 'Applicative') -> 'Applicative':
        if callable(self.value()):
            return functor.map(self.value())
        raise ValueError('Cannot map a non function')

class Monad(Functor):
    """ Monad type which can bind two monads while mapping between categories.
    """
    def join(self) -> 'Monad':
        if isinstance(self.value(), Monad):
            return self.value()
        else:
            return type(self)(self.value())

    def bind(self, f: Callable[[Any], 'Monad']) -> 'Monad':
        return self.map(f).join()
