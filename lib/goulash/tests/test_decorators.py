""" goulash.tests.test_decorators
"""

from unittest import TestCase, main
from goulash.decorators import arg_types

class TestArgTypesDecorator(TestCase):
    def setUp(self):
        self.fxn = lambda x: x

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

if __name__=='__main__':
    main()
