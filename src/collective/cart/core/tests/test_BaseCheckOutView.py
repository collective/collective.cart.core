# -*- coding: utf-8 -*-
from collective.cart.core.browser.template import BaseCheckOutView
from collective.cart.core.tests.base import IntegrationTestCase

import mock


class BaseCheckOutViewTestCase(IntegrationTestCase):
    """TestCase for BaseCheckOutView"""

    def test_subclass(self):
        from Products.Five import BrowserView
        self.assertTrue(issubclass(BaseCheckOutView, BrowserView))

    @mock.patch('collective.cart.core.browser.template.IShoppingSite')
    def test___call__(self, IShoppingSite):
        instance = self.create_view(BaseCheckOutView)
        instance.request = mock.Mock()
        self.assertIsNotNone(instance())
        instance.request.set.assert_called_with('disable_border', True)
        self.assertEqual(IShoppingSite().clean_articles_in_cart.call_count, 1)
        instance.request.response.redirect.assert_called_with('http://nohost/plone/@@cart')
        self.assertEqual(instance.request.response.redirect.call_count, 1)

        instance.context.restrictedTraverse = mock.Mock()
        instance.context.restrictedTraverse().current_base_url.return_value = 'http://nohost/plone/@@cart'
        self.assertIsNone(instance())
        self.assertEqual(IShoppingSite().clean_articles_in_cart.call_count, 2)
        self.assertEqual(instance.request.response.redirect.call_count, 1)
