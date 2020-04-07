from typing import Any, Callable, TypeVar
from functools import reduce

def pipe(*funs: [Callable[..., Any]]):
    """
    Combine a number of functions which will be called from left to right.
    Example: pipe(a, b, c)(x) == c(b(a(x)))
    """
    return lambda arg: reduce(lambda a, f: f(a), funs, arg)

def compose(*funs: [Callable[..., Any]]):
    """
    Combine a number of functions which will be called from right to left.
    Example: compose(a, b, c)(x) == a(b(c(x)))
    """
    return pipe(*reversed(funs))

def curry(f: Callable, *args):
    """
    Decorator to transform a regular function into a curried function.
    """
    def wrapper():
        try:
            return f(*args)
        except TypeError:
            return lambda *more: curry(f, *args, *more)
    return wrapper()

F = TypeVar('F', bound = 'Functor')
A = TypeVar('A', bound = 'Applicative')
M = TypeVar('M', bound = 'Monad')

@curry
def fmap(f: Callable[[Any], Any], functor: F) -> F:
    """
    Functor map a function.
    """
    return functor.map(f)

@curry
def apply(functor: A, other: A) -> A:
    """
    Apply one functor to another.
    """
    return functor.apply(other)

@curry
def bind(f: Callable[[Any], M], monad: M) -> M:
    """
    Bind a mapped monadic function.
    """
    return monad.bind(f)

@curry
def liftA(f: Callable, a: F) -> F:
    """
    Lift an unary function to actions.
    """
    return a.map(f)

@curry
def liftA2(f: Callable, a: A, b: A) -> A:
    """
    Lift a curried binary function to actions.
    """
    return a.map(f).apply(b)

@curry
def liftA3(f: Callable, a: A, b: A, c: A) -> A:
    """
    Lift a curried ternary function to actions.
    """
    return a.map(f).apply(b).apply(c)
