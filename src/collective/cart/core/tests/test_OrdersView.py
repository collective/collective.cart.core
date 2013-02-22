# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import IShoppingSiteRoot
from collective.cart.core.tests.base import IntegrationTestCase
from plone.dexterity.utils import createContentInContainer
from zope.lifecycleevent import modified
from zope.publisher.browser import TestRequest
from zope.interface import alsoProvides


import mock


class TestOrdersView(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        alsoProvides(self.portal, IShoppingSiteRoot)
        self.portal.reindexObject()
        container = createContentInContainer(self.portal, 'collective.cart.core.CartContainer', checkConstraints=False,
                id='cart-container', title='Cärt Cöntäiner', description='Descriptiön of Cärt Cöntäiner')
        modified(container)

    def test_subclass(self):
        from collective.cart.core.browser.template import BaseView
        from collective.cart.core.browser.template import OrdersView
        self.assertTrue(issubclass(OrdersView, BaseView))

    def create_view(self, context=None):
        from collective.cart.core.browser.template import OrdersView
        request = TestRequest()
        request.set = mock.Mock()
        if context is None:
            context = self.portal
        return OrdersView(context, request)

    def create_carts(self):
        for num in range(1, 3):
            oid = '{}'.format(num)
            cart = createContentInContainer(
                self.portal['cart-container'], 'collective.cart.core.Cart', checkConstraints=False, id=oid)
            modified(cart)

    def test_instance__name(self):
        instance = self.create_view()
        self.assertEqual(getattr(instance, 'grokcore.component.directive.name'), 'orders')

    def test_instance__require(self):
        instance = self.create_view()
        self.assertEqual(getattr(instance, 'grokcore.security.directive.require'), ['collective.cart.core.ViewCartContent'])

    def test_instance__template(self):
        instance = self.create_view()
        self.assertEqual(getattr(instance, 'grokcore.view.directive.template'), 'orders')

    def test_cart_container(self):
        instance = self.create_view()
        self.assertEqual('/'.join(instance.cart_container.getPhysicalPath()), '/plone/cart-container')

    def test_cart_container_not_shopping_site(self):
        from zope.interface import noLongerProvides
        noLongerProvides(self.portal, IShoppingSiteRoot)
        instance = self.create_view(context=self.portal['cart-container'])
        self.assertEqual('/'.join(instance.cart_container.getPhysicalPath()), '/plone/cart-container')

    def test_transitions(self):
        instance = self.create_view()
        self.create_carts()
        from collective.cart.core.interfaces import IBaseAdapter
        from collective.cart.core.interfaces import ICart
        for item in IBaseAdapter(self.portal).get_content_listing(ICart):
            self.assertEqual(instance.transitions(item), [
                {'available': True, 'id': 'canceled', 'name': 'Canceled'},
                {'available': False, 'id': 'ordered', 'name': 'Ordered'}])

    def test_carts__zero(self):
        instance = self.create_view()
        self.assertEqual(len(instance.carts), 0)

    @mock.patch('collective.cart.core.browser.template.getMultiAdapter')
    def test_carts__two(self, getMultiAdapter):
        getMultiAdapter().toLocalizedTime.return_value = u'DATE'
        instance = self.create_view()
        self.create_carts()
        instance.transitions = mock.Mock(return_value="TRANSITIONS")
        self.assertEqual(sorted(instance.carts), [{
            'owner': 'test_user_1_',
            'state_title': 'Created',
            'is_canceled': False,
            'title': '',
            'url': 'http://nohost/plone/cart-container/1',
            'transitions': 'TRANSITIONS',
            'id': '1',
            'modified': u'DATE'
        }, {
            'owner': 'test_user_1_',
            'state_title': 'Created',
            'is_canceled': False,
            'title': '',
            'url': 'http://nohost/plone/cart-container/2',
            'transitions': 'TRANSITIONS',
            'id': '2',
            'modified': u'DATE'
        }])

    def test_update(self):
        instance = self.create_view()
        instance.update()
        self.assertEqual(instance.request.set.call_args_list, [
            (('disable_plone.leftcolumn', True),), (('disable_plone.rightcolumn', True),)])

        self.create_carts()
        cart1 = self.portal['cart-container']['1']
        cart2 = self.portal['cart-container']['2']
        workflow = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(workflow.getInfoFor(cart1, 'review_state'), 'created')
        self.assertEqual(workflow.getInfoFor(cart2, 'review_state'), 'created')

        instance.request.form = {'form.buttons.ChangeState': 'paid'}
        instance.update()
        self.assertEqual(workflow.getInfoFor(cart1, 'review_state'), 'created')
        self.assertEqual(workflow.getInfoFor(cart2, 'review_state'), 'created')

        instance.request.form = {'cart-id': '1'}
        instance.update()
        self.assertEqual(workflow.getInfoFor(cart1, 'review_state'), 'created')
        self.assertEqual(workflow.getInfoFor(cart2, 'review_state'), 'created')

        instance.request.form = {'form.buttons.ChangeState': 'ordered', 'cart-id': '1'}
        instance.update()
        self.assertEqual(workflow.getInfoFor(cart1, 'review_state'), 'ordered')
        self.assertEqual(workflow.getInfoFor(cart2, 'review_state'), 'created')

        instance.request.form = {'form.buttons.RemoveCart': 'ordered', 'cart-id': '1'}
        instance.update()
        with self.assertRaises(KeyError):
            self.portal['cart-container']['1']
        self.assertEqual(workflow.getInfoFor(cart2, 'review_state'), 'created')
