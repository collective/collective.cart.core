# -*- coding: utf-8 -*-
from collective.cart.core.browser.interfaces import IBaseFormView
from collective.cart.core.browser.template import BaseFormView
from collective.cart.core.tests.base import IntegrationTestCase


class BaseFormViewTestCase(IntegrationTestCase):
    """TestCase for BaseFormView"""

    def test_subclass(self):
        from Products.Five import BrowserView
        self.assertTrue(issubclass(BaseFormView, BrowserView))
        from plone.app.layout.globals.interfaces import IViewView
        self.assertTrue(issubclass(IBaseFormView, IViewView))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_view(BaseFormView)
        self.assertTrue(verifyObject(IBaseFormView, instance))
