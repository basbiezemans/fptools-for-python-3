## Maybe monad

Let's say we want to do a sequence of operations on a value but it's possible that this value becomes `None` during any one operation. A None value isn't very useful to us and can potentially break our code. To avoid this problem we decide to treat a value as "maybe just a value, or nothing".

We can implement this as follows:

```python
from typing import Any, Callable
from types import Monad

class Just(Monad):
    pass

class Nothing(Monad):
    # Override
    def map(self, f: Callable[[Any], Any]) -> Functor:
        return self
    # Override
    def bind(self, f: Callable[[Any], Monad]) -> Monad:
        return self

# Constructor function
def Maybe(value):
    return Nothing() if value is None else Just(value)

def isNothing(maybe):
    return isinstance(maybe, Nothing)

def fromMaybe(default, maybe):
    return default if isNothing(maybe) else maybe._value

# Scenario 1: value is 6
x = Maybe(6)
y = x.bind(lambda x: Maybe(x ** 2))
print(repr(x))                          # Just(6)
print(repr(y))                          # Just(36)
print('value: ' + str(fromMaybe(0, y))) # value: 36

# Scenario 2: value is None
x = Maybe(None)
y = x.bind(lambda x: Maybe(x ** 2))
print(repr(x))                          # Nothing(None)
print(repr(y))                          # Nothing(None)
print('value: ' + str(fromMaybe(0, y))) # value: 0
```