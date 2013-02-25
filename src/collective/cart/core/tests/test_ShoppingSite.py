from Testing import ZopeTestCase as ztc
from collective.cart.core.tests.base import IntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

import mock


class TestShoppingSite(IntegrationTestCase):

    def setUp(self):
        ztc.utils.setupCoreSessions(self.layer['app'])
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_subclass(self):
        from collective.cart.core.adapter.base import BaseAdapter
        from collective.cart.core.adapter.interface import ShoppingSite
        self.assertTrue(issubclass(ShoppingSite, BaseAdapter))
        from collective.cart.core.interfaces import IBaseAdapter
        from collective.cart.core.interfaces import IShoppingSite
        self.assertTrue(issubclass(IShoppingSite, IBaseAdapter))

    def test_instance(self):
        from collective.cart.core.adapter.interface import ShoppingSite
        from collective.cart.core.interfaces import IShoppingSite
        self.assertIsInstance(IShoppingSite(self.portal), ShoppingSite)

    def test_instance__provides(self):
        from collective.cart.core.interfaces import IShoppingSite
        self.assertEqual(getattr(IShoppingSite(self.portal), 'grokcore.component.directive.provides'), IShoppingSite)

    def create_folder(self, context=None, oid=None):
        if context is None:
            context = self.portal
        if oid is None:
            oid = 'folder'
        folder = context[context.invokeFactory('Folder', oid)]
        folder.reindexObject()
        return folder

    def test_shop(self):
        from collective.cart.core.interfaces import IShoppingSite
        from collective.cart.core.interfaces import IShoppingSiteRoot
        from zope.interface import alsoProvides
        folder1 = self.create_folder(oid='folder1')
        folder2 = self.create_folder(folder1, 'folder2')
        folder3 = self.create_folder(folder2, 'folder3')
        alsoProvides(folder1, IShoppingSiteRoot)
        self.assertIsNone(IShoppingSite(self.portal).shop)
        self.assertEqual(IShoppingSite(folder1).shop, folder1)
        self.assertEqual(IShoppingSite(folder2).shop, folder1)
        self.assertEqual(IShoppingSite(folder3).shop, folder1)

        alsoProvides(folder2, IShoppingSiteRoot)
        self.assertIsNone(IShoppingSite(self.portal).shop)
        self.assertEqual(IShoppingSite(folder1).shop, folder1)
        self.assertEqual(IShoppingSite(folder2).shop, folder2)
        self.assertEqual(IShoppingSite(folder3).shop, folder2)

    def test_cart_container(self):
        from collective.cart.core.interfaces import IShoppingSite
        from collective.cart.core.interfaces import IShoppingSiteRoot
        from plone.dexterity.utils import createContentInContainer
        from zope.interface import alsoProvides
        from zope.interface import noLongerProvides
        from zope.lifecycleevent import modified
        self.assertIsNone(IShoppingSite(self.portal).cart_container)

        folder = self.create_folder()
        self.assertIsNone(IShoppingSite(folder).cart_container)

        alsoProvides(folder, IShoppingSiteRoot)
        self.assertIsNone(IShoppingSite(folder).cart_container)

        container = createContentInContainer(
            folder, 'collective.cart.core.CartContainer', id='container', checkConstraints=False)
        modified(container)
        self.assertEqual(IShoppingSite(folder).cart_container, container)

        noLongerProvides(folder, IShoppingSiteRoot)
        self.assertIsNone(IShoppingSite(folder).cart_container)

    def test_cart(self):
        from collective.cart.core.interfaces import IShoppingSite
        shopping_site = IShoppingSite(self.portal)
        self.assertIsNone(shopping_site.cart)

        session = shopping_site.getSessionData(create=True)
        session.set('collective.cart.core', 'CART')
        self.assertEqual(shopping_site.cart, 'CART')

    def test_cart_articles(self):
        from collective.cart.core.interfaces import IShoppingSite
        shopping_site = IShoppingSite(self.portal)
        self.assertIsNone(shopping_site.cart_articles)

        session = shopping_site.getSessionData(create=True)
        session.set('collective.cart.core', {})
        self.assertIsNone(shopping_site.cart_articles)

        session.set('collective.cart.core', {'articles': 'ARTICLES'})
        self.assertEqual(shopping_site.cart_articles, 'ARTICLES')

    def test_cart_article_listing(self):
        from collective.cart.core.interfaces import IShoppingSite
        shopping_site = IShoppingSite(self.portal)
        self.assertEqual(shopping_site.cart_article_listing, [])

        session = shopping_site.getSessionData(create=True)
        session.set('collective.cart.core', {'articles': {'1': 'ARTICLE1', '2': 'ARTICLE2'}})
        self.assertEqual(shopping_site.cart_article_listing, ['ARTICLE1', 'ARTICLE2'])

    def test_get_cart_article(self):
        from collective.cart.core.interfaces import IShoppingSite
        shopping_site = IShoppingSite(self.portal)
        self.assertIsNone(shopping_site.get_cart_article('1'))

        session = shopping_site.getSessionData(create=True)
        session.set('collective.cart.core', {'articles': {'1': 'ARTICLE1', '2': 'ARTICLE2'}})

        self.assertIsNone(shopping_site.get_cart_article('3'))
        self.assertEqual(shopping_site.get_cart_article('2'), 'ARTICLE2')

    def test_remove_cart_articles(self):
        from collective.cart.core.interfaces import IShoppingSite
        shopping_site = IShoppingSite(self.portal)
        session = shopping_site.getSessionData(create=True)
        session.set('collective.cart.core', {'articles': {'1': 'ARTICLE1', '2': 'ARTICLE2', '3': 'ARTICLE3'}})

        shopping_site.remove_cart_articles('4')
        self.assertEqual(shopping_site.cart_articles, {'1': 'ARTICLE1', '2': 'ARTICLE2', '3': 'ARTICLE3'})

        shopping_site.remove_cart_articles(['2', '3'])
        self.assertEqual(shopping_site.cart_articles, {'1': 'ARTICLE1'})

        shopping_site.remove_cart_articles('1')
        self.assertEqual(shopping_site.cart_articles, {})

    # CartContainer related methods

    def test_get_cart(self):
        from collective.cart.core.interfaces import IShoppingSite
        from collective.cart.core.interfaces import IShoppingSiteRoot
        from plone.dexterity.utils import createContentInContainer
        from zope.interface import alsoProvides
        from zope.lifecycleevent import modified
        self.assertIsNone(IShoppingSite(self.portal).get_cart('1'))

        folder = self.create_folder()
        alsoProvides(folder, IShoppingSiteRoot)
        container = createContentInContainer(
            folder, 'collective.cart.core.CartContainer', id='container', checkConstraints=False)
        modified(container)
        self.assertIsNone(IShoppingSite(folder).get_cart('1'))

        cart1 = createContentInContainer(
            container, 'collective.cart.core.Cart', id='1', checkConstraints=False)
        modified(cart1)
        self.assertIsNone(IShoppingSite(folder).get_cart('2'))
        self.assertEqual(IShoppingSite(folder).get_cart('1'), cart1)

    @mock.patch('collective.cart.core.adapter.interface.ICartContainerAdapter')
    def test_update_next_cart_id(self, ICartContainerAdapter):
        from collective.cart.core.interfaces import IShoppingSite
        from collective.cart.core.interfaces import IShoppingSiteRoot
        from plone.dexterity.utils import createContentInContainer
        from zope.interface import alsoProvides
        from zope.lifecycleevent import modified

        folder = self.create_folder()
        alsoProvides(folder, IShoppingSiteRoot)

        IShoppingSite(folder).update_next_cart_id()
        self.assertFalse(ICartContainerAdapter.called)

        container = createContentInContainer(
            folder, 'collective.cart.core.CartContainer', id='container', checkConstraints=False)
        modified(container)

        IShoppingSite(folder).update_next_cart_id()
        self.assertTrue(ICartContainerAdapter.called)
