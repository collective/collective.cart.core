from collective.cart.core.tests.base import IntegrationTestCase
from plone.dexterity.utils import createContentInContainer
from zope.lifecycleevent import modified

import unittest


class ICartArticleTestCase(unittest.TestCase):

    def test_subclass(self):
        from plone.directives import form
        from collective.cart.core.interfaces import ICartArticle
        self.assertTrue(issubclass(ICartArticle, form.Schema))

    def get_field(self, name):
        """Get field(attribute) based on name.

        :param name: Name of field(attribute).
        :type name: str"""
        from collective.cart.core.interfaces import ICartArticle
        return ICartArticle.get(name)

    def test_orig_uuid(self):
        self.assertEqual(self.get_field('orig_uuid').getDoc(),
            'Original UUID')


class CartArticleTestSetup(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def create_instance(self):
        instance = createContentInContainer(self.portal, 'collective.cart.core.CartArticle',
            id='1', orig_uuid=u'UUID', checkConstraints=False)
        modified(instance)
        return instance

    def test_instance(self):
        from plone.dexterity.content import Container
        instance = self.create_instance()
        self.assertIsInstance(instance, Container)

    def test_verifyObject(self):
        from collective.cart.core.interfaces import ICartArticle
        instance = self.create_instance()
        self.assertTrue(ICartArticle, instance)

    def test_id(self):
        instance = self.create_instance()
        self.assertEqual(instance.id, '1')

    def test_orig_uuid(self):
        instance = self.create_instance()
        self.assertEqual(instance.orig_uuid, u'UUID')
