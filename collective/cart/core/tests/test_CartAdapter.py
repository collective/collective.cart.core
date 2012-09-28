from collective.cart.core.tests.base import IntegrationTestCase
from plone.dexterity.utils import createContentInContainer
from zope.lifecycleevent import modified

import unittest


class ICartAdapterTestCase(unittest.TestCase):

    def test_subclass(self):
        from zope.interface import Interface
        from collective.cart.core.interfaces import ICartAdapter
        self.assertTrue(issubclass(ICartAdapter, Interface))

    def test_articles(self):
        from collective.cart.core.interfaces import ICartAdapter
        self.assertEqual(ICartAdapter.get('articles').getDoc(),
            'List of brains of CartArticle.')


class CartAdapterTestSetup(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def test_subclass__CartAdapter(self):
        from collective.cart.core.adapter.cart import CartAdapter
        from five import grok
        self.assertTrue(issubclass(CartAdapter, grok.Adapter))

    def create_cart(self):
        """Create cart."""
        # Create cart.
        cart = createContentInContainer(self.portal, 'collective.cart.core.Cart', id='1',
            checkConstraints=False)
        modified(cart)
        return cart

    def test_instance(self):
        from collective.cart.core.adapter.cart import CartAdapter
        from collective.cart.core.interfaces import ICartAdapter
        cart = self.create_cart()
        self.assertIsInstance(ICartAdapter(cart), CartAdapter)

    def test_articles__None(self):
        """Test property: articles when there are no articles in the cart."""
        from collective.cart.core.interfaces import ICartAdapter
        cart = self.create_cart()
        self.assertEqual(len(ICartAdapter(cart).articles), 0)

    def test_articles__Two(self):
        """Test property: articles when there are two articles in the cart."""
        from collective.cart.core.interfaces import ICartAdapter
        cart = self.create_cart()
        article1 = createContentInContainer(cart, 'collective.cart.core.CartArticle',
            id='article1', checkConstraints=False)
        modified(article1)
        article2 = createContentInContainer(cart, 'collective.cart.core.CartArticle',
            id='article2', checkConstraints=False)
        modified(article2)
        self.assertEqual(len(ICartAdapter(cart).articles), 2)
