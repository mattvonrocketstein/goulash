""" goulash.tests.test_decorators
"""
import unittest
from unittest import TestCase

from goulash.decorators import (
    require_module, arg_types,
    memoized_property, classproperty)

class TestClass(object):
    @classproperty
    def test(kls): return 3

class TestClassProperty(TestCase):
    def test_classproperty(self):
        self.assertEqual(TestClass.test, 3)

class TestArgTypesDecorator(TestCase):
    def setUp(self):
        self.fxn = lambda x: x

    def test_require_module_good(self):
        @require_module('sys')
        def f():
            pass
        f()

    def test_require_module_bad(self):
        @require_module('zdfasdasd')
        def f():
            pass
        self.assertRaises(ImportError, f)

    def test_require_module_bad_msg(self):
        @require_module('doesntexist',msg='ohno')
        def f():
            pass
        try:
            f()
        except ImportError, e:
            self.assertEqual(e.message, 'ohno')
        else:
            self.fail("require_module failed to rewrite exception with custom mmsg")

    def test_ignores_kargs(self):
        @arg_types(int)
        def fxn(*args, **kargs):
            return kargs
        fxn(1, 2, 3, foo='bar')

    def test_one_type_bad(self):
        tmp = arg_types(int)(self.fxn)
        self.assertRaises(
            arg_types.ArgTypeError,
            lambda: tmp('3'))

    def test_two_types_bad(self):
        tmp = arg_types(int,list)(self.fxn)
        self.assertRaises(
            arg_types.ArgTypeError,
            lambda: tmp('3'))

    def test_good_two_types(self):
        tmp = arg_types(int, list)(self.fxn)
        tmp(42)

    def test_good_one_type(self):
        tmp = arg_types(list)(self.fxn)
        tmp([])

class TestMemoizedProperty(TestCase):
    def setUp(self):
        self.call_count = 0
        class ExampleClass(object):
            @memoized_property
            def example(himself):
                self.call_count += 1
                return 3
        self.kls = ExampleClass

    def test_memoized_property(self):
        tmp1 = self.kls()
        tmp2 = self.kls()
        self.assertEqual(tmp1.example, 3)
        self.assertEqual(self.call_count, 1)
        self.assertEqual(tmp1.example, 3)
        self.assertEqual(self.call_count, 1)
        #note: different instances *should* get fresh calls
        self.assertEqual(tmp2.example, 3)
        self.assertEqual(self.call_count, 2)
        self.assertEqual(tmp1.example, 3)
        self.assertEqual(tmp2.example, 3)
        self.assertEqual(self.call_count, 2)
if __name__=='__main__':
    unittest.main()
