# -*- coding: utf-8 -*-
"""A module of potentially useful class types"""
import inspect
import threading

__all__ = ['Dict', 'immutableobject', 'Singleton', 'ThreadedSingleton']
__author__ = 'Jon Nappi'


class Dict(dict):
    """A *dict* builtin subclass. Currently the only additional functionality
    that this class provides is the addition of the __iadd__ method, which
    provides += functionality to dictionaries. ie:
    ::
        >>> d1 = Dict(one=1, two=2)
        >>> d2 = Dict(three=3, four=4)
        >>> d1 += d2
        >>> d1
        ... {'one': 1, 'three': 3, 'two': 2, 'four': 4}

    It's important to note that keys in the right-most dictionary will take
    precedence over keys in the left-most one. ie, if the same key exists in
    d2 as d1, then the value for d1 will be overriden on +='ing them together
    """
    def __iadd__(self, other):
        if not isinstance(other, dict):
            pass
        for key, val in other.items():
            self[key] = val
        return self


# noinspection PyPep8Naming
class immutableobject:
    """This classtype provides a means through which to create a class with
    immutable attributes. That is, once this class has been instanciated, you
    can no longer update the values of this class's attributes.
    ::
        >>> class Foo(immutableobject):
        ...     def __init__(self, x, y):
        ...         self.x = x
        ...         self.y = y
        ...         super(Foo, self).__init__()
        >>> f = Foo(1, 2)
        >>> f.x
        ... 1
        >>> f.x = 5
        >>> f.x
        ... 1

    You can optionally specify the `fail_quietly` flag in `immutableobject`'s
    __init__method to False. This will then raise TypeError's when a user
    attempts to update the value for an immutable attribute. Please note that
    this TypeError convention was adopted from the way builtin tuples'
    immutability behaves.
    """
    __initialized = False

    def __init__(self, fail_quietly=True):
        self._fail_quietly = fail_quietly
        self.__initialized = True

    def __setattr__(self, key, value):
        if not self.__initialized:
            super(immutableobject, self).__setattr__(key, value)
        elif not self._fail_quietly:
            try:
                name = str(self.__class__).split('.')[-1][:-2]
            except:
                name = 'immutableobject'
            msg = '{} object does not support item assignment'
            raise TypeError(msg.format(name))


class _Singleton(type):
    """A metaclass for providing singleton-type functionality to all instances
    of this type.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        _key = inspect.getmro(cls)
        if _key not in cls._instances:
            # super(_Singleton, cls) evaluates to type; *args/**kwargs get
            # passed to class __init__ method via type.__call__
            cls._instances[_key] = \
                super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[_key]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    """A Singleton type for ensuring that only one type of any given object
    exists at any given time. For example
    ::
        >>> class Foo(Singleton):
        ...     def __init__(self, x):
        ...         super(Foo, self).__init__()
        ...         self.x = x
        >>> f = Foo(5)
        >>> f.x
        ... 5
        >>> f = Foo(8675309)
        >>> f.x
        ... 5
    """
    pass


class ThreadedSingleton(_Singleton('SingletonMeta', (object,), {})):
    """An additional, slightly less strict Singleton implementation. Here you
    can use threads to isolate various singleton instances within their own
    threads. Or, to put it simply, each thread can have it's own singleton
    instance
    """
    def __call__(cls, *args, **kwargs):
        _key = inspect.getmro(cls)
        cur_thread = threading.current_thread()
        if _key not in cls._instances:
            cls._instances[_key] = {
                # super(_Singleton, cls) evaluates to type; *args/**kwargs get
                # passed to class __init__ method via type.__call__
                cur_thread: super(_Singleton, cls).__call__(*args, **kwargs)
            }
        elif _key in cls._instances and cur_thread not in cls._instances[_key]:
            cls._instances[_key][cur_thread] = \
                super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[_key][cur_thread]
