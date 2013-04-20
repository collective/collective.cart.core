from collective.cart.core.content import Article
from collective.cart.core.content import OrderContainer
from collective.cart.core.content import Order
from collective.cart.core.content import OrderArticle
from plone.dexterity.content import Container

import unittest


class ArticleTestCase(unittest.TestCase):
    """TestCase for content type: collective.cart.core.Article"""

    def test_subclass(self):
        self.assertTrue(issubclass(Article, Container))

    def test_instance__verifyObject(self):
        from collective.cart.core.interfaces import IArticle
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(IArticle, Article()))


class OrderContainerTestCase(unittest.TestCase):
    """TestCase for content type: collective.cart.core.OrderContainer"""

    def test_subclass(self):
        self.assertTrue(issubclass(OrderContainer, Container))

    def test_instance__verifyObject(self):
        from collective.cart.core.interfaces import IOrderContainer
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(IOrderContainer, OrderContainer()))


class OrderTestCase(unittest.TestCase):
    """TestCase for content type: collective.cart.core.Order"""

    def test_subclass(self):
        self.assertTrue(issubclass(Order, Container))

    def test_instance__verifyObject(self):
        from collective.cart.core.interfaces import IOrder
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(IOrder, Order()))


class OrderArticleTestCase(unittest.TestCase):
    """TestCase for content type: collective.cart.core.OrderArticle"""

    def test_subclass(self):
        self.assertTrue(issubclass(OrderArticle, Container))

    def test_instance__verifyObject(self):
        from collective.cart.core.interfaces import IOrderArticle
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(IOrderArticle, OrderArticle()))
