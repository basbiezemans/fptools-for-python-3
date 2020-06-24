# Writer Monad

The Writer monad allows us to compose functions that return their result values as well as a concatenation of the logs from each function application. It can be used to keep track of any kind of information. One good use could be to profile functions by always returning the execution time via a Writer instance. Another common use is to track debug messages.

In order to implement a Writer monad, we first need to create two functions that are each other's inverse. One function returns a Writer given a value and some output. The other returns a result value and  concatenated output, given a Writer monad.

```python
# Construct a writer computation from a (result, output) pair
def writer(result, output = ''):
    return Writer(lambda: (result, (output,)))

# Unwrap a writer computation as a (result, output) pair
def runWriter(w, final = lambda x: x):
    run = w.value()
    return final(run())
```

With the above functions, a Writer monad can be implemented as follows (`map` and `apply` are omitted in this example).

```python
from typing import Callable
from fptools.types import Monad

class Writer(Monad):
    # Override
    def bind(self, f: Callable):
        def binder():
            result, o1 = runWriter(self)
            result, o2 = runWriter(f(result))
            return (result, o1 + o2)
        return Writer(binder)
```

The benefits of a Writer monad are demonstrated in the following example. We calculate the Golden Ratio while also logging the separate steps.

```python
from math import sqrt
from pprint import pprint
from fptools.functions import compose, bind

# Functions for each step of the computation
sqRoot = lambda x: writer(sqrt(x), f'square root: {sqrt(x)}')
addOne = lambda x: writer(x + 1,   f'add one: {x + 1}')
divTwo = lambda x: writer(x / 2,   f'divide by two: {x / 2}')

# Golden ratio = (1 + sqrt(5)) / 2
computation = compose(bind(divTwo), bind(addOne), bind(sqRoot))
goldenRatio = computation(writer(5, 'initial value: 5'))

result, output = runWriter(goldenRatio)

print(f'The Golden Ratio is: {result}')
pprint(output)

# The Golden Ratio is: 1.618033988749895
# ('initial value: 5',
#  'square root: 2.23606797749979',
#  'add one: 3.23606797749979',
#  'divide by two: 1.618033988749895')
```

The result and output from a writer computation can also be extracted with the functions `fst` and `snd` in case you just need one of them.

```python
from operator import itemgetter

fst = itemgetter(0)
snd = itemgetter(1)

# Run Writer w with fst/snd
result = runWriter(w, fst)
output = runWriter(w, snd)
```
