from collective.cart.core.tests.base import IntegrationTestCase
from zope.publisher.browser import TestRequest


class TestBaseView(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def test_templatedir(self):
        from collective.cart.core.browser import template
        self.assertEqual(getattr(template, 'grokcore.view.directive.templatedir'), 'templates')

    def test_subclass(self):
        from five.grok import View
        from collective.cart.core.browser.template import BaseView
        self.assertTrue(issubclass(BaseView, View))

    def create_view(self):
        from collective.cart.core.browser.template import BaseView
        return BaseView(self.portal, TestRequest())

    def test_instance__baseclass(self):
        instance = self.create_view()
        self.assertTrue(getattr(instance, 'martian.martiandirective.baseclass'))

    def test_instance__context(self):
        from collective.cart.core.interfaces import IShoppingSiteRoot
        instance = self.create_view()
        self.assertEqual(getattr(instance, 'grokcore.component.directive.context'), IShoppingSiteRoot)

    def test_instance__layer(self):
        from collective.cart.core.browser.interfaces import ICollectiveCartCoreLayer
        instance = self.create_view()
        self.assertEqual(getattr(instance, 'grokcore.view.directive.layer'), ICollectiveCartCoreLayer)

    def test_instance__require(self):
        instance = self.create_view()
        self.assertEqual(getattr(instance, 'grokcore.security.directive.require'), ['zope2.View'])
