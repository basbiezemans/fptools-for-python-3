from typing import Any, Callable
from functions import compose

class DataType():
    """ Default data type with semi-private _value property.
    """
    def __init__(self, value = None):
        self._value = value

    def __bool__(self):
        return self._value is not None

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self._value)

class Functor(DataType):
    """ Functor type which can map between two categories.
    """
    def map(self, f: Callable[[Any], Any]) -> 'Functor':
        return type(self)(f(self._value))

class Applicative(Functor):
    """ Applicative type which can apply functors to each other.
    """
    def apply(self, functor: 'Applicative') -> 'Applicative':
        if callable(self._value):
            return functor.map(self._value)
        raise ValueError('Cannot map a non function')

class Monad(Functor):
    """ Monad type which can bind two monads while mapping between categories.
    """
    def join(self) -> 'Monad':
        if isinstance(self._value, Monad):
            return self._value
        else:
            return type(self)(self._value)

    def bind(self, f: Callable[[Any], 'Monad']) -> 'Monad':
        return self.map(f).join()


if __name__ == '__main__':

    assert(True if DataType(42) else False)
    assert(False if DataType(None) else True)

    m = """
        Functors should preserve composition of morphisms

        F.map(compose(g, f)) == F.map(f).map(g)
        """
    f = lambda x: x ** 2
    g = lambda x: x + 6
    a = Functor(6).map(compose(g, f))
    b = Functor(6).map(f).map(g)
    assert(repr(a) == repr(b)), m

    m = """
        Applicatives should be interchangeable

        F.map(f) == F(f).apply(F)
        """
    f = lambda x: x ** 2
    a = Applicative(6).map(f)
    b = Applicative(f).apply(Applicative(6))
    assert(repr(a) == repr(b)), m

    m = """
        Monads should preserve associativity

        M.bind(f).bind(g) == M((f).bind(g)).join()
        """
    f = lambda x: Monad(x ** 2)
    g = lambda x: Monad(x + 6)
    a = Monad(6).bind(f).bind(g)
    b = Monad(f(6).bind(g)).join()
    assert(repr(a) == repr(b)), m
