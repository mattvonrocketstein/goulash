""" namespaces.tests
"""

from unittest import TestCase, main
from namespaces import Namespace

class TestObject(object):
    class_variable = 'foo'
    def _private_method(self): pass

    @staticmethod
    def public_static_method(foo, bar): pass

class ComplexTestObject(TestObject):
    my_class_variable = 'foo'

class TestBasic(TestCase):
    def setUp(self):
        self.test_obj = TestObject()
        self.test_ns = Namespace(self.test_obj)

    def test_locals(self):
        pass

    def test_keys(self):
        diff = list(set(self.test_ns.keys()) - set(dir(self.test_obj)))
        self.assertFalse(diff)

    def test_clean(self):
        self.assertTrue('__class__' not in self.test_ns.nonprivate)
        self.assertTrue('_private_method' not in self.test_ns.nonprivate)

    def test_methods(self):
        self.assertTrue([self.test_obj._private_method],
                        self.test_ns.methods.values())

    def test_startswith(self):
        self.assertEqual(self.test_ns.startswith('pub').keys(),
                         ['public_static_method'])

    def test_private(self):
        diff = set(self.test_ns.keys()) - set(self.test_ns.private.keys())
        self.assertEqual(diff, set(['class_variable','public_static_method']))

    def test_functions(self):
        self.assertTrue([self.test_obj.public_static_method],
                        self.test_ns.functions.values())

    def test_class_variables(self):
        self.assertTrue(['class_variable'],
                        self.test_ns.class_variables.keys())

if __name__=='__main__':
    main()
