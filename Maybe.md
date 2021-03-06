## Maybe monad

Let's say we want to do a sequence of operations on a value but it's possible that this value becomes `None` during any one operation. A None value isn't very useful to us and can potentially break our code. To avoid this problem we decide to treat a value as "maybe nothing, or just a value".

We can implement this as follows:

```python
from typing import Callable
from fptools.types import Monad

class Just(Monad):
    pass

class Nothing(Monad):
    # Override
    def bind(self, f: Callable):
        return self

# Constructor function
def maybe(value):
    return Nothing() if value is None else Just(value)

def isNothing(maybe):
    return isinstance(maybe, Nothing)

def fromMaybe(default, maybe):
    return default if isNothing(maybe) else maybe.value()
```

Now that we have a Maybe monad, let's see how it can be used in practice. The following example shows how to safely do a stepwise calculation, even when a step returns a None value.

```python
from functools import partial
from fptools.functions import compose, bind

# Functions f and g represent our calculation
# It looks like function f will fail when the
# input is a number equal or greater than 7
f = lambda x: maybe(x ** 2 if x < 7 else None)
g = lambda x: maybe(x + 6)
calc = compose(bind(g), bind(f))

# Unwrap a Maybe value and cast it to a string
show = compose(str, partial(fromMaybe, 0))

# Scenario 1
x = Just(6)
y = calc(x)
print(repr(x))                    # Just(6)
print(repr(y))                    # Just(42)
print('result:', show(y))         # result: 42

# Scenario 2
x = Just(9)
y = calc(x)
print(repr(x))                    # Just(9)
print(repr(y))                    # Nothing(None)
print('result:', show(y))         # result: 0
```

