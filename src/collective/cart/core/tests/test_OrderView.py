# -*- coding: utf-8 -*-
from collective.cart.core.browser.interfaces import IOrderView
from collective.cart.core.browser.template import OrderView
from collective.cart.core.tests.base import IntegrationTestCase


class OrderViewTestCase(IntegrationTestCase):
    """TestCase for OrderView"""

    def test_subclass(self):
        from Products.Five import BrowserView
        self.assertTrue(issubclass(OrderView, BrowserView))
        from plone.app.layout.globals.interfaces import IViewView
        self.assertTrue(issubclass(IOrderView, IViewView))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_view(OrderView)
        self.assertTrue(verifyObject(IOrderView, instance))
