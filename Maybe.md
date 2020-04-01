## Maybe monad

Let's say we want to do a sequence of operations on a value but it's possible that this value becomes `None` during any one operation. A None value isn't very useful to us and can potentially break our code. To avoid this problem we decide to treat a value as "maybe just a value, or nothing".

We can implement this as follows:

```python
from typing import Any, Callable
from fptools.types import Functor, Monad
from fptools.functions import curry

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

@curry
def fromMaybe(default, maybe):
    return default if isNothing(maybe) else maybe._value
```

Now that we have a Maybe monad, let's see how it works in practice. The following example shows how to safely do a stepwise calculation, even when a step returns a None value.

```python
from fptools.functions import compose

# Functions f and g represent our computations
f = lambda x: Maybe(x ** 2)
g = lambda x: Maybe(x + 6)

# Function show unwraps a Maybe value and casts it to a string
show = compose(str, fromMaybe(0))

# Scenario 1
x = Maybe(6)
y = x.bind(f).bind(g)
print(repr(x))                          # Just(6)
print(repr(y))                          # Just(42)
print('result: ' + show(y))             # result: 42

# Scenario 2
f = lambda x: Maybe(None)               # Oops!
x = Maybe(6)
y = x.bind(f).bind(g)
print(repr(x))                          # Just(6)
print(repr(y))                          # Nothing(None)
print('result: ' + show(y))             # result: 0
```

