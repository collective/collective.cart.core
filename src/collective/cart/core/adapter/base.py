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

    @property
    @memoize
    def _catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_brains(self, interface=None, **query):
        if interface:
            query['object_provides'] = interface.__identifier__
        path = query.get('path')
        if path is None:
            path = '/'.join(aq_inner(self.context).getPhysicalPath())
        if query.get('depth') is not None:
            path = {'query': path, 'depth': query.pop('depth')}
        query['path'] = path
        return self._catalog(query)

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
