# Functional Programming tools for Python 3

Python 3 has functools and itertools modules with many handy functions. This library contains a few more building blocks for functional programming in Python 3.

**Types**

* DataType (base type)
* Functor
* Applicative Functor
* Monad

*Type Examples*

* [Either functor](Either.md)
  <small>The Either functor can be used when a computation might error.</small>

* [IO applicative](IO.md)
  <small>The IO applicative can be used to make side effects explicit.</small>

* [Maybe monad](Maybe.md)
  <small>The Maybe monad can be used when a computation might return nothing.</small>

* [Writer monad](Writer.md)
  <small>The Writer monad can be used to pass side information alongside the return value.</small>
  
* Reader monad
  <small>The Reader monad can be used to share a common environment between  computations.</small>

**Functions**

* pipe, compose
* curry (decorator)
* fmap, apply, bind
* liftA, liftA2, liftA3
* transduce, tmap, tfilter
* iterate, take, drop

