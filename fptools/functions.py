from typing import Any, Callable
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
