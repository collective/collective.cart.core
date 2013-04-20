# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from collective.cart.core.browser.template import OrdersView
from collective.cart.core.interfaces import IOrder
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from collective.cart.core.tests.base import IntegrationTestCase
from zope.interface import alsoProvides

import mock


class OrdersViewTestCase(IntegrationTestCase):
    """TestCase for Orders"""

    def test_subclass(self):
        from Products.Five import BrowserView
        self.assertTrue(issubclass(OrdersView, BrowserView))

    def test_template(self):
        instance = self.create_view(OrdersView)
        self.assertEqual(instance.template.filename.split('/')[-1], 'orders.pt')

    @mock.patch('collective.cart.core.browser.template.IShoppingSite')
    def test_order_container(self, IShoppingSite):
        instance = self.create_view(OrdersView)
        self.assertEqual(instance.order_container(), IShoppingSite().order_container())

        from collective.cart.core.interfaces import IOrderContainer
        alsoProvides(self.portal, IOrderContainer)
        self.assertEqual(instance.order_container(), self.portal)

    def test_transitions(self):
        alsoProvides(self.portal, IShoppingSiteRoot)
        container = self.create_content('collective.cart.core.OrderContainer')
        instance = self.create_view(OrdersView)
        self.create_content('collective.cart.core.Order', container, id='1')
        self.create_content('collective.cart.core.Order', container, id='2')
        for item in IShoppingSite(self.portal).get_content_listing(IOrder):
            self.assertEqual(instance.transitions(item), [
                {'available': True, 'id': 'canceled', 'name': 'Canceled'},
                {'available': False, 'id': 'ordered', 'name': 'Ordered'}])

    @mock.patch('Products.CMFPlone.browser.ploneview.Plone.toLocalizedTime')
    @mock.patch('collective.cart.core.browser.template.getToolByName')
    def test_orders(self, getToolByName, toLocalizedTime):
        alsoProvides(self.portal, IShoppingSiteRoot)
        instance = self.create_view(OrdersView)
        self.assertEqual(instance.orders(), [])

        container = self.create_content('collective.cart.core.OrderContainer')
        self.assertEqual(instance.orders(), [])

        self.create_content('collective.cart.core.Order', container, id='1', title="Örder1")
        self.create_content('collective.cart.core.Order', container, id='3', title="Örder3")
        self.create_content('collective.cart.core.Order', container, id='2', title="Örder2")
        transitions = mock.Mock()
        instance.transitions = transitions
        self.assertEqual(len(instance.orders()), 3)

    def test___call__(self):
        alsoProvides(self.portal, IShoppingSiteRoot)
        container = self.create_content('collective.cart.core.OrderContainer')
        order1 = self.create_content('collective.cart.core.Order', container, id='1')
        order2 = self.create_content('collective.cart.core.Order', container, id='2')
        instance = self.create_view(OrdersView)
        self.assertEqual(len(container.objectIds()), 2)
        workflow = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(workflow.getInfoFor(order1, 'review_state'), 'created')
        self.assertEqual(workflow.getInfoFor(order2, 'review_state'), 'created')

        template = mock.Mock()
        instance.template = template
        instance.request.set = mock.Mock()
        self.assertEqual(instance(), template())
        self.assertEqual(instance.request.set.call_args_list, [
            (('disable_plone.leftcolumn', True),),
            (('disable_plone.rightcolumn', True),)])
        self.assertEqual(len(container.objectIds()), 2)
        self.assertEqual(workflow.getInfoFor(order1, 'review_state'), 'created')
        self.assertEqual(workflow.getInfoFor(order2, 'review_state'), 'created')

        instance.request.form = mock.MagicMock()
        instance.request.form = {'form.buttons.ChangeState': 'ordered'}
        self.assertEqual(instance(), template())
        self.assertEqual(len(container.objectIds()), 2)
        self.assertEqual(workflow.getInfoFor(order1, 'review_state'), 'created')
        self.assertEqual(workflow.getInfoFor(order2, 'review_state'), 'created')

        instance.request.form = {'form.buttons.ChangeState': 'ordered', 'order_id': '1'}
        self.assertEqual(instance(), template())
        self.assertEqual(len(container.objectIds()), 2)
        self.assertEqual(workflow.getInfoFor(order1, 'review_state'), 'ordered')
        self.assertEqual(workflow.getInfoFor(order2, 'review_state'), 'created')

        instance.request.form = {'form.buttons.RemoveCart': 'ordered', 'order_id': '1'}
        self.assertEqual(instance(), template())
        self.assertEqual(container.objectIds(), ['2'])
        self.assertEqual(workflow.getInfoFor(order2, 'review_state'), 'created')
