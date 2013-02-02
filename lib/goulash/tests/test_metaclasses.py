""" goulash.tests.test_metaclasses
"""
from inspect import isclass
from unittest import TestCase, main

from goulash.mixin import Mixin
from goulash.metaclasses import ClassAlgebra, supports_class_algebra
from goulash.tests.data import TestObject as _TestObject


class TestClassAlgebrae(TestCase):

    def setUp(self):
        class TestObject(_TestObject):
            __metaclass__ = ClassAlgebra

        #@Mixin.template_from
        class RandomMixinClass(object):
            random_mixin_class = 1

        self.obj = TestObject()
        self.TestObject = TestObject
        self.RandomMixinClass = RandomMixinClass

    def test_lshift(self,tobject = None):
        tobject = tobject or self.TestObject
        tmp = tobject<<self.RandomMixinClass
        self.assertTrue(isclass(tmp))
        self.assertEqual((self.RandomMixinClass, tobject), tmp.__bases__)

    def test_rshift(self):
        tmp = self.TestObject>>self.RandomMixinClass
        self.assertTrue(isclass(tmp))
        self.assertEqual((self.TestObject, self.RandomMixinClass), tmp.__bases__)

    def test_supports_class_algebra1(self):
        # failing!
        @supports_class_algebra
        class Testing(self.RandomMixinClass):
            pass
        self.assertTrue(Testing.__metaclass__==ClassAlgebra)
        self.test_lshift(Testing)

    def test_supports_class_algebra2(self):
        @supports_class_algebra
        class Testing(object):
            pass
        self.assertTrue(Testing.__metaclass__==ClassAlgebra)
        self.test_lshift(Testing)

    def test_subclass(self,tobject=None):
        tobject = tobject or self.TestObject
        tmp = tobject.subclass(new_variable='new_variable',
                                  class_variable='overriding_foo')
        self.assertTrue(isclass(tmp))
        self.assertEqual(tmp.class_variable, 'overriding_foo')
        self.assertTrue(hasattr(tmp, 'new_variable'))
        self.assertFalse(hasattr(tobject, 'new_variable'))

    def test_template_from(self):
        tmp = self.TestObject.template_from(self.RandomMixinClass)
        self.assertTrue(isclass(tmp))
        self.assertTrue(tmp.__bases__==(self.RandomMixinClass,self.TestObject))
        self.assertTrue(self.RandomMixinClass.__name__ in tmp.__name__)
        self.assertTrue(self.TestObject.__name__ in tmp.__name__)

if __name__=='__main__':
    main()

""" TODO: convert this
from unittest import TestCase

from cortex.core.agent import Agent
from cortex.tests import uniq

class MetaclassesTest(TestCase):
    def test_uniq(self):
        A = Agent.subclass()
        B = Agent.subclass()
        self.assertTrue( A != B )
        B.foo='bar'
        self.assertTrue( not hasattr(A,'foo') )

    def test_collide(self):
        class A(Agent.subclass(name='ProtoA')): pass
        B = Agent.subclass(name='B', foo='bar')
        C = Agent.subclass(bar='foo')
        self.assertTrue(not hasattr(Agent, 'foo'))
        #from IPython import Shell; Shell.IPShellEmbed(argv=['-noconfirm_exit'])()
        self.assertTrue(A!=B)
        self.assertTrue(not hasattr(A, 'foo'))
        self.assertTrue(not hasattr(C, 'foo'))
        self.assertTrue(hasattr(B,'foo'))

    def test_subclasses_empty(self):
        x = Agent.subclass(); self.assertTrue(issubclass(x, Agent))

    def test_subclasses_name(self,name=None):
        name = name or uniq()
        x = Agent.subclass(name); self.assertTrue(issubclass(x, Agent))
        self.assertTrue(x.__name__==name)

    def test_subclasses_dct(self, name=None):
        name = name or uniq()
        x = Agent.subclass(); self.assertTrue(issubclass(x, Agent))
        x = Agent.subclass(name , dict(foo=3));
        self.assertTrue(x.__name__==name)
        self.assertTrue(x.foo==3)

    def test_subclasses_dct2(self, name=None):
        name = name or uniq()
        x = Agent.subclass(); self.assertTrue(issubclass(x, Agent))
        x = Agent.subclass(name, foo=3);
        self.assertTrue(x.__name__==name)
        self.assertTrue(x.foo==3)

    def test_subclasses_multiple(self):
        x = Agent.subclass();
        y = Agent.subclass();
        self.assertTrue(issubclass(x, Agent))
        self.assertTrue(issubclass(y, Agent))
        self.assertTrue(not issubclass(y, x))
        self.assertTrue(not issubclass(x, y))
"""
