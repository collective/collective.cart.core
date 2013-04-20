from collective.cart.core.browser.template import CartView
from collective.cart.core.tests.base import IntegrationTestCase

import mock


class CartViewTestCase(IntegrationTestCase):
    """TestCase for CartView"""

    def test_subclass(self):
        from collective.cart.core.browser.template import BaseCheckOutView
        self.assertTrue(issubclass(CartView, BaseCheckOutView))

    def test_template(self):
        instance = self.create_view(CartView)
        self.assertEqual(instance.template.filename.split('/')[-1], 'cart.pt')

    @mock.patch('collective.cart.core.browser.template.BaseCheckOutView.__call__')
    def test___call__(self, __call__):
        instance = self.create_view(CartView)
        template = mock.Mock()
        instance.template = template
        self.assertEqual(instance(), template())
        self.assertTrue(__call__.called)
