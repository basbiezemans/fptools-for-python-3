# Either Functor

A functional version of an if-then-else statement is the concept of Either. Either is a so-called Union type. It is either this or that. The naming convention for *this* is Left and *that* is Right. In Python we can describe the Either type as follows:

```python
from typing import Union, TypeVar

Left = TypeVar('Left')
Right = TypeVar('Right')
Either = Union[Left, Right] # Either Left or Right
```

Depending on our use case, Either can be implemented as a Functor, Applicative or Monad.

```python
from fptools.types import Functor

class Either(Functor): pass
class Left(Either): pass
class Right(Either): pass
```

The above code can be extended to implement error handling. For this purpose we use an `either` function. It works like this: if Either is Left then map function f, if Either is Right then map function g. The convention is that Left contains an error message and Right a correct value.

```python
from fptools.functions import curry

def isLeft(either: Either):
    return isinstance(either, Left)

@curry
def either(f, g, e: Either):
    either = e.map(f if isLeft(e) else g)
    return either.value()
```

Now imagine a scenario where you query a schema-less database that returns JSON documents. We can not rely on a consistent schema and it's likely that documents have missing fields. In which case it's nice to show a default value or a message saying that the information is missing.

The following code shows how `either` handles missing values in an elegant way. Function `pluck` tries to get a document field and returns either Left or Right, depending on the situation. Function `either` applies a function to the result of `pluck` and returns its value. We use an `identity` function to return Left in case of a missing value.

```python
from datetime import date, timedelta
from fptools.functions import compose, curry

# The documents which we receive from the database
people = [
    {'name': 'John Doe', 'birthday': '1990-12-01'},
    {'name': 'Jane Doe', 'phone': '555-0199'}
]

@curry
def pluck(key: str, document: dict) -> Either:
    value = document.get(key)
    error = f'No {key} available'
    return Right(value) if value else Left(error)

# An identity function just returns its input
identity = lambda x: x

# Convert an ISO date string to a date object
toDate = lambda s: date(*map(int, s.split('-')))

# Convert to upper case
toUpper = lambda s: s.upper()

# Calculate the age based on date of birth
def getAge(bdate):
    days = date.today() - toDate(bdate)
    return days // timedelta(days=365.2425)

ageOf = compose(either(identity, getAge), \
                pluck('birthday'))

nameOf = compose(either(identity, toUpper), \
                 pluck('name'))

for person in people:
    print(nameOf(person), ':', ageOf(person))

# JOHN DOE : 29
# JANE DOE : No birthday available
```

