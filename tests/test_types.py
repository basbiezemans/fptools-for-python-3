from unittest import TestCase
from fptools.types import *

class TestTypes(TestCase):

    def test_datatype(self):
        self.assertTrue(True if DataType(42) else False)
        self.assertFalse(True if DataType(None) else False)

    def test_datatype_equality(self):
        a = DataType(42)
        b = DataType(24)
        self.assertEqual(a, DataType(42))
        self.assertNotEqual(a, b)

    def test_functor(self):
        m = """
            Functors should preserve composition of morphisms

            F.map(compose(g, f)) == F.map(f).map(g)
            """
        f = lambda x: x ** 2
        g = lambda x: x + 6
        a = Functor(6).map(compose(g, f))
        b = Functor(6).map(f).map(g)
        self.assertEqual(repr(a), repr(b), m)

    def test_applicative(self):
        m = """
            Applicatives should be interchangeable

            F.map(f) == F(f).apply(F)
            """
        f = lambda x: x ** 2
        a = Applicative(6).map(f)
        b = Applicative(f).apply(Applicative(6))
        self.assertEqual(repr(a), repr(b), m)

    def test_applicative_value_error(self):
        with self.assertRaises(ValueError):
            Applicative(1).apply(Applicative(6))

    def test_monad(self):
        m = """
            Monads should preserve associativity

            M.bind(f).bind(g) == M((f).bind(g)).join()
            """
        f = lambda x: Monad(x ** 2)
        g = lambda x: Monad(x + 6)
        a = Monad(6).bind(f).bind(g)
        b = Monad(f(6).bind(g)).join()
        self.assertEqual(repr(a), repr(b), m)
