# -*- coding: utf-8 -*-
import unittest

from misc import Dict, immutableobject, Singleton

__author__ = 'Jon Nappi'


class DictTests(unittest.TestCase):
    def test_append(self):
        d1 = Dict(one=1, two=2)
        d2 = Dict(three=3, four=4)
        d1 += d2
        self.assertIn('three', d1)
        self.assertIn('four', d1)
        self.assertEqual(len(d1), 4)


class ImmutableObjectTests(unittest.TestCase):
    def setUp(self):
        class Foo(immutableobject):
            def __init__(self, x, *args, **kwargs):
                self.x = x
                super(Foo, self).__init__(*args, **kwargs)
        self.foo = Foo(5)

    def test_access(self):
        self.assertEqual(self.foo.x, 5)

    def test_immutability(self):
        self.foo.x = 12
        self.assertEqual(self.foo.x, 5)

    def test_type_error(self):
        class Bar(self.foo.__class__):
            def __init__(self, *args, **kwargs):
                super(Bar, self).__init__(*args, fail_quietly=False, **kwargs)
        b = Bar(5)
        with self.assertRaises(TypeError):
            b.x = 15


@unittest.skip
class SingletonTests(unittest.TestCase):
    pass
