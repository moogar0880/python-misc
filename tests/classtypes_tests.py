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


class SingletonTests(unittest.TestCase):
    """Unit level tests for Singletons"""
    def setUp(self):
        """Create an overly simple Singleton class to test with"""
        class MyTestSingleton(Singleton):
            def __init__(self, x):
                super(MyTestSingleton, self).__init__()
                self.x = x
        self.klass = MyTestSingleton

    def tearDown(self):
        """Iterate over all singleton instances and explictly call their
        class's delete method
        """
        self.klass._instances = {}
        self.klass = None

    def test_basic_singleton(self):
        """Verify basic Singleton functionality, ie, that when we try to create
        a second instance of a Singleton type, that we get back the true
        Singleton instance
        """
        s1 = self.klass(5)
        s2 = self.klass(12)
        self.assertIs(s1, s2)
        self.assertEqual(s2.x, 5)
        self.assertEqual(len(self.klass._instances), 1)

    def test_new(self):
        """Same test as `test_basic_singleton`, only while using the Singleton
        new method to override existing Singletons
        """
        s1 = self.klass.new(5)
        s2 = self.klass.new(12)
        self.assertIsNot(s1, s2)
        self.assertEqual(s2.x, 12)
        self.assertEqual(len(self.klass._instances), 1)

    def test_delete(self):
        """Validate that we can successfully delete a Singleton instance"""
        self.klass(5)
        self.klass.delete()
        self.assertEqual(len(self.klass._instances), 0)

    def test_multiple_singletons(self):
        """Validate that we can successfully have multiple types of Singletons
        floating around
        """
        class Foo(Singleton):
            def __init__(self, x, y):
                super(Foo, self).__init__()
                self.x = x
                self.y = y
        s1 = self.klass(5)
        s2 = Foo(1, 2)
        self.assertIsNot(s1, s2)
        self.assertEqual(len(self.klass._instances), 2)
