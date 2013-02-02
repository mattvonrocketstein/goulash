""" goulash.tests.test_metaclasses
"""
from inspect import isclass
from unittest import TestCase, main

from goulash.metaclasses import META1
from goulash.tests.data import TestObject as _TestObject

class TestObject(_TestObject):
    __metaclass__ = META1

class RandomMixinClass(object):
    foo = 1

class TestClassAlgebrae(TestCase):
    def setUp(self):
        self.obj = TestObject()

    def test_lshift(self):
        tmp = TestObject<<RandomMixinClass
        self.assertTrue(isclass(tmp))
        self.assertEqual((RandomMixinClass, TestObject), tmp.__bases__)

    def test_rshift(self):
        tmp = TestObject>>RandomMixinClass
        self.assertTrue(isclass(tmp))
        self.assertEqual((TestObject, RandomMixinClass), tmp.__bases__)

    def test_subclass(self):
        tmp = TestObject.subclass(new_variable='new_variable',
                                  class_variable='overriding_foo')
        self.assertTrue(isclass(tmp))
        self.assertEqual(tmp.class_variable, 'overriding_foo')
        self.assertTrue(hasattr(tmp, 'new_variable'))
        self.assertFalse(hasattr(TestObject,'new_variable'))

    def test_template_from(self):
        tmp = TestObject.template_from(RandomMixinClass)
        self.assertTrue(isclass(tmp))
        self.assertTrue(tmp.__bases__==(RandomMixinClass,TestObject))
        self.assertTrue(RandomMixinClass.__name__ in tmp.__name__)
        self.assertTrue(TestObject.__name__ in tmp.__name__)

if __name__=='__main__':
    main()
