from unittest import TestCase
from fptools.types import *
from fptools.functions import *

class TestFunctions(TestCase):

    def test_pipe(self):
        f = lambda x: x ** 2
        g = lambda x: x + 6
        self.assertEqual(pipe(f, g)(6), 42)

    def test_compose(self):
        f = lambda x: x ** 2
        g = lambda x: x + 6
        self.assertEqual(compose(g, f)(6), 42)

    def test_curry_decorator(self):
        @curry
        def add(a: int, b: int):
            return a + b
        self.assertEqual(add(2)(3), 5)

    def test_fmap(self):
        f = lambda x: x ** 2
        x = Functor(6)
        y = fmap(f, x)
        self.assertEqual(repr(y), 'Functor(36)')

    def test_apply(self):
        f = lambda x: x ** 2
        x = Applicative(6)
        y = apply(Applicative(f), x)
        self.assertEqual(repr(y), 'Applicative(36)')

    def test_bind(self):
        f = lambda x: Monad(x ** 2)
        x = Monad(6)
        y = bind(f, x)
        self.assertEqual(repr(y), 'Monad(36)')

    def test_liftA(self):
        e = lambda x: x ** 2
        f = lambda x: lambda y: e(x) + y * 3
        g = lambda x: lambda y: lambda z: f(x)(y) + z ** 3
        a = Applicative(6)
        b = Applicative(2)
        c = Applicative(3)
        self.assertEqual(repr(liftA(e, a)), 'Applicative(36)')
        self.assertEqual(repr(liftA2(f, a, b)), 'Applicative(42)')
        self.assertEqual(repr(liftA3(g, a, b, c)), 'Applicative(69)')

    def test_transduce(self):
        listCombine = lambda list, val: list + [val]
        isLongEnough = lambda s: len(s) >= 5
        isShortEnough = lambda s: len(s) <= 10
        transducer = compose(
            tmap(str.upper),
            tfilter(isLongEnough),
            tfilter(isShortEnough)
        )
        words = 'They have written something very interesting'.split(' ')
        result = ['WRITTEN', 'SOMETHING']
        self.assertEqual(result, transduce(transducer, listCombine, [], words))
