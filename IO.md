# IO Applicative

Conceptually, an IO Applicative is fairly simple. It provides the context for input and output. As an applicative<sup>[1](#applicative)</sup>, it can map a function over one or more arguments. Why would we need an IO Applicative? I/O is considered impure in functional programming. An IO type represents side effects (I/O actions). Using an IO type makes possible side effects explicit.

Creating an IO Applicative is pretty straightforward.

```python
from fptools.types import Applicative

class IO(Applicative): pass
```

The following example shows how user input can be transformed to a user object while signing into an account.

```python
from fptools.functions import curry, liftA2

def getVal(key):
    # Get form post data, e.g. request.form
    # For this example we return a hardcoded
    # IO wrapped form value
    form = {
        'email': 'john.doe@foo.com',
        'password': '$eCr3T'
    }
    return IO(form.get(key))

@curry
def signIn(username, password):
    # Get user object and compare passwords
    # For this example we just return a plain
    # dictionary object
    return {
        'id': 42,
        'name': 'John Doe',
        'email': 'john.doe@foo.com'
    }

# Sign-in with email and password
user = IO(signIn).apply(getVal('email')).apply(getVal('password'))

# Or using liftA2 (lift Applicative with 2 arguments)
user = liftA2(signIn, getVal('email'), getVal('password'))

print(repr(user))
# IO({'id': 42, 'name': 'John Doe', 'email': 'john.doe@foo.com'})
```

The above example can be extended to handle invalid input, by wrapping user input in a [Maybe](Maybe.md) context before lifting it into an I/O context.

----
**Footnotes:**

<a name="applicative">1.</a> An Applicative Functor allows us to wrap (lift) a function into a context where it can be applied to multiple arguments, while preserving the context (wrapper). The benefit of an Applicative over a plain Functor is that it can lift functions of arbitrary arity, whereas `fmap` can only lift a unary function.