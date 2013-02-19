# -*- coding: utf-8 -*-
from Testing import ZopeTestCase as ztc
from collective.cart.core.tests.base import IntegrationTestCase
from plone.dexterity.utils import createContentInContainer
from zope.lifecycleevent import modified
from zope.publisher.browser import TestRequest

import mock


class TestBaseCheckOutView(IntegrationTestCase):

    def setUp(self):
        ztc.utils.setupCoreSessions(self.layer['app'])
        self.portal = self.layer['portal']

        for num in range(1, 3):
            oid = 'article{}'.format(num)
            title = 'Ärticle{}'.format(num)
            description = "Descriptiön of Ärticle{}".format(num)
            article = createContentInContainer(self.portal, 'collective.cart.core.Article', checkConstraints=False,
                id=oid, title=title, description=description)
            modified(article)

    def test_subclass(self):
        from collective.cart.core.browser.template import BaseView
        from collective.cart.core.browser.template import BaseCheckOutView
        self.assertTrue(issubclass(BaseCheckOutView, BaseView))

    def create_view(self):
        from collective.cart.core.browser.template import BaseCheckOutView
        request = TestRequest()
        request.set = mock.Mock()
        return BaseCheckOutView(self.portal, request)

    def test_instance__baseclass(self):
        instance = self.create_view()
        self.assertTrue(getattr(instance, 'martian.martiandirective.baseclass'))

    def test_shopping_site(self):
        from collective.cart.core.adapter.interface import ShoppingSite
        instance = self.create_view()
        self.assertIsInstance(instance.shopping_site, ShoppingSite)

    def test_cart_articles(self):
        from collective.cart.core.adapter.article import IArticleAdapter
        instance = self.create_view()
        self.assertIsNone(instance.cart_articles)

        article1 = self.portal['article1']
        IArticleAdapter(article1).add_to_cart()
        self.assertEqual(len(instance.cart_articles), 1)

    def test_update(self):
        from collective.cart.core.adapter.article import IArticleAdapter
        from plone.uuid.interfaces import IUUID
        instance = self.create_view()

        article1 = self.portal['article1']
        IArticleAdapter(article1).add_to_cart()
        article2 = self.portal['article2']
        IArticleAdapter(article2).add_to_cart()
        instance.update()
        instance.request.set.assert_called_with('disable_border', True)
        self.assertEqual(len(instance.cart_articles), 2)

        # Remove article1
        self.portal.manage_delObjects(['article1'])
        instance.update()
        instance.request.set.assert_called_with('disable_border', True)
        self.assertEqual(instance.cart_articles.keys(), [IUUID(article2)])
