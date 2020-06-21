from typing import Any, Iterator, Iterable, Callable, TypeVar
from inspect import signature
from functools import reduce
from itertools import islice

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

def curry(func: Callable, *a):
    """
    Decorator to transform a regular function into a curried function.
    """
    n = len(signature(func).parameters)
    def wrapper(*b):
        c = a + b
        c = c[:n] # ignore extra args
        if len(c) == n:
            return func(*c)
        else:
            return curry(func, *c)
    return wrapper

def iterate(func: Callable, x: Any) -> Iterator:
    """
    Create an infinite list of values f(x) starting with x.
    """
    while True:
        yield x
        x = func(x)

def take(n: int, xs: Iterable) -> Iterator:
    """
    Return the first n items of the iterable.
    """
    return islice(xs, n)

def drop(n: int, xs: Iterable) -> Iterator:
    """
    Return the part of the iterable after the first n items.
    """
    return islice(xs, n, None)

def transduce(transducer: Callable, combinator: Callable, initializer, iterable):
    """
    Transduce uses a transducer function to transform and reduce the items of a
    sequence to a single value.
    A transducer is a composable higher-order reducer. It takes a reducer as input,
    and returns another reducer.
    """
    reducer = transducer(combinator)
    return reduce(reducer, iterable, initializer)

@curry
def tmap(mapper: Callable, combinator: Callable):
    """
    Transducer map-reducer
    """
    def reducer(list, value):
        return combinator(list, mapper(value))
    return reducer

@curry
def tfilter(predicate: Callable, combinator: Callable):
    """
    Transducer filter-reducer
    """
    def reducer(list, value):
        if (predicate(value)):
            return combinator(list, value)
        return list
    return reducer

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
def apply(other: A, functor: A) -> A:
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
