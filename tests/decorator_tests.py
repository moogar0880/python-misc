# -*- coding: utf-8 -*-
import unittest

from misc import classproperty

__author__ = 'Jon Nappi'


class ClassPropertyDecoratorTests(unittest.TestCase):
    """Unit level tests for the classproperty type"""
    def setUp(self):
        class Example:
            _x = 0
            _y = 0

            @classproperty
            def x(cls):
                return cls._x

            @x.setter
            def x(cls, value):
                cls._x = value

            @classmethod
            def get_y(cls):
                return cls._y

            @classmethod
            def set_y(cls, value):
                cls._y = value

            y = classproperty(get_y, set_y)
        self.klass = Example

    def test_getter(self):
        """Validate classproperty get functionality"""
        self.assertEqual(self.klass._x, self.klass.x)
        self.assertEqual(self.klass._y, self.klass.y)

    def test_setter(self):
        """Validate classproperty set functionality"""
        self.assertEqual(self.klass._x, self.klass.x)
        self.klass.x = 5
        self.assertEqual(self.klass._x, self.klass.x)

        self.assertEqual(self.klass._y, self.klass.y)
        self.klass.y = 5
        self.assertEqual(self.klass._y, self.klass.y)

    def test_inheritance(self):
        """Validate that classproperties can be successfully inherited and
        overriden
        """
        class Foo(self.klass):
            pass

        self.assertEqual(Foo._x, Foo.x)
