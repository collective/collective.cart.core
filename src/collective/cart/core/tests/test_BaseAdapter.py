from collective.cart.core.tests.base import IntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

import mock


class TestBaseAdapter(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_instance(self):
        from collective.cart.core.interfaces import IBaseAdapter
        from collective.cart.core.adapter.base import BaseAdapter
        self.assertIsInstance(IBaseAdapter(self.portal), BaseAdapter)

    def test_instance__provides(self):
        from collective.cart.core.interfaces import IBaseAdapter
        self.assertEqual(getattr(IBaseAdapter(self.portal), 'grokcore.component.directive.provides'), IBaseAdapter)

    def test_instance__context(self):
        from collective.cart.core.interfaces import IBaseAdapter
        from zope.interface import Interface
        self.assertEqual(getattr(IBaseAdapter(self.portal), 'grokcore.component.directive.context'), Interface)

    def create_doc(self, context=None, oid=None):
        if context is None:
            context = self.portal
        if oid is None:
            oid = 'doc'
        doc = context[context.invokeFactory('Document', oid)]
        doc.reindexObject()
        return doc

    def create_folder(self, context=None, oid=None):
        if context is None:
            context = self.portal
        if oid is None:
            oid = 'folder'
        folder = context[context.invokeFactory('Folder', oid)]
        folder.reindexObject()
        return folder

    def test__catalog(self):
        self.create_doc()
        from collective.cart.core.interfaces import IBaseAdapter
        catalog = IBaseAdapter(self.portal)._catalog()
        self.assertEqual(catalog(id='doc')[0].id, 'doc')

    def test_get_brains__zero(self):
        from collective.cart.core.interfaces import IBaseAdapter
        self.assertEqual(len(IBaseAdapter(self.portal).get_brains(id='someid')), 0)

    def test_get_brains(self):
        self.create_doc()
        from collective.cart.core.interfaces import IBaseAdapter
        self.assertTrue(len(IBaseAdapter(self.portal).get_brains()) >= 1)

    def test_get_brains__interface_IATFolder(self):
        self.create_doc()
        self.create_folder()
        from collective.cart.core.interfaces import IBaseAdapter
        from Products.ATContentTypes.interfaces.folder import IATFolder
        ids = [brain.id for brain in IBaseAdapter(self.portal).get_brains(interface=IATFolder)]
        self.assertIn('folder', ids)
        self.assertNotIn('doc', ids)

    def test_get_brains__path_folder(self):
        folder1 = self.create_folder(oid='folder1')
        path = '/'.join(folder1.getPhysicalPath())
        self.create_doc(context=folder1)
        folder2 = self.create_folder(folder1, 'folder2')
        folder3 = self.create_folder(folder2, 'folder3')
        from collective.cart.core.interfaces import IBaseAdapter
        from Products.ATContentTypes.interfaces.folder import IATFolder
        base = IBaseAdapter(self.portal)
        ids = [brain.id for brain in base.get_brains(path=path)]
        self.assertIn('folder1', ids)
        self.assertIn('folder2', ids)
        self.assertIn('doc', ids)
        self.assertIn('folder3', ids)


        ids = [brain.id for brain in base.get_brains(path=path, depth=0)]
        self.assertIn('folder1', ids)
        self.assertNotIn('folder2', ids)
        self.assertNotIn('doc', ids)
        self.assertNotIn('folder3', ids)

        ids = [brain.id for brain in base.get_brains(path=path, depth=1)]
        self.assertNotIn('folder1', ids)
        self.assertIn('folder2', ids)
        self.assertIn('doc', ids)
        self.assertNotIn('folder3', ids)

        ids = [brain.id for brain in base.get_brains(interface=IATFolder, path=path, depth=1)]
        self.assertNotIn('folder1', ids)
        self.assertIn('folder2', ids)
        self.assertNotIn('doc', ids)
        self.assertNotIn('folder3', ids)

        base._catalog = mock.Mock()
        base.get_brains(interface=IATFolder, path=path, depth=1, sort_order="descending")
        base._catalog().assert_called_with({
            'object_provides': IATFolder.__identifier__,
            'path': {'query': '/plone/folder1', 'depth':1},
            'sort_order': 'descending'
        })

    def test_get_brain__None(self):
        from collective.cart.core.interfaces import IBaseAdapter
        self.assertIsNone(IBaseAdapter(self.portal).get_brain(id='someid'))

    def test_get_brain_id_doc(self):
        from collective.cart.core.interfaces import IBaseAdapter
        self.create_doc()
        self.assertEqual(IBaseAdapter(self.portal).get_brain(id='doc').id, 'doc')

    def test_get_object__None(self):
        from collective.cart.core.interfaces import IBaseAdapter
        self.assertIsNone(IBaseAdapter(self.portal).get_object(id='someid'))

    def test_get_object_id_doc(self):
        from collective.cart.core.interfaces import IBaseAdapter
        doc = self.create_doc()
        self.assertEqual(IBaseAdapter(self.portal).get_object(id='doc'), doc)

    def test_get_content_listing__None(self):
        from collective.cart.core.interfaces import IBaseAdapter
        from plone.app.contentlisting.contentlisting import ContentListing
        content_listing = IBaseAdapter(self.portal).get_content_listing(id='someid')
        self.assertEqual(len(content_listing), 0)
        self.assertIsInstance(content_listing, ContentListing)

    def test_get_content_listing_id_doc(self):
        from collective.cart.core.interfaces import IBaseAdapter
        from plone.app.contentlisting.contentlisting import ContentListing
        doc = self.create_doc()
        content_listing = IBaseAdapter(self.portal).get_content_listing(id='doc')
        self.assertEqual(len(content_listing), 1)
        self.assertIsInstance(content_listing, ContentListing)
        self.assertEqual([item.getObject() for item in content_listing][0], doc)
