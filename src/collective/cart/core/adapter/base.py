from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import IBaseAdapter
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.memoize.instance import memoize
from zope.interface import Interface


class BaseAdapter(grok.Adapter):
    """Base class for adapters"""

    grok.context(Interface)
    grok.provides(IBaseAdapter)

    @memoize
    def _catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_brains(self, interface=None, **query):
        if interface:
            query['object_provides'] = interface.__identifier__
        path = query.get('path')
        if path is None:
            path = '/'.join(aq_inner(self.context).getPhysicalPath())
        depth = query.get('depth')
        if depth:
            path = {'query': path, 'depth': depth}
        query['path'] = path
        return self._catalog()(query)

    def get_brain(self, interface=None, **query):
        brains = self.get_brains(interface=interface, **query)
        if brains:
            return brains[0]

    def get_object(self, interface=None, **query):
        brain = self.get_brain(interface=interface, **query)
        if brain:
            return brain.getObject()

    def get_content_listing(self, interface=None, **query):
        return IContentListing(self.get_brains(interface, **query))

    @memoize
    def _ulocalized_time(self):
        """Return ulocalized_time method.

        :rtype: method
        """
        translation_service = getToolByName(self.context, 'translation_service')
        return translation_service.ulocalized_time

    def localized_time(self, item, long_format=False):
        ulocalized_time = self._ulocalized_time()
        return ulocalized_time(item.ModificationDate(),
            long_format=long_format, context=self.context)
