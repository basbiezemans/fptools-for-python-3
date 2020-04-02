from unittest import TestCase
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