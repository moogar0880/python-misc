# -*- coding: utf-8 -*-
"""A medly of useful decorator utilities"""

__author__ = 'Jon Nappi'
__all__ = ['classproperty']


# noinspection PyPep8Naming
class classproperty(object):
    """A property for class level attributes

    fget is a function to be used for getting an attribute value, and likewise
    fset is a function for setting. Typical use is to define a managed
    attribute x:

    class Foo(object):
        _x = 0
        def getx(cls): return cls._x
        def setx(cls, value): cls._x = value
        x = classproperty(getx, setx, "I'm the 'x' property.")

    Decorators make defining new class properties or modifying existing ones
    easy:

    class Foo(object):
        _x = 0
        @classproperty
        def x(cls):
            "I am the 'x' property."
            return cls._x
        @x.setter
        def x(cls, value):
            cls._x = value
    """
    def __init__(self, fget=None, fset=None, doc=None):
        def is_class_method(f):
            """Determine if method *f* is a class or static method"""
            return isinstance(f, (classmethod, staticmethod))

        self.fget = fget if is_class_method(fget) else classmethod(fget)
        self.fset = fset if is_class_method(fset) else classmethod(fset)
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        if self.fget is None:
            raise AttributeError('unreadable attribute')
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def getter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fget = func
        return self

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self
