from Products.CMFCore.utils import getToolByName
from collective.behavior.salable.interfaces import ISalable
from collective.cart.core.interfaces import IArticle
from collective.cart.core.interfaces import ICartArticleAdapter
from collective.cart.core.interfaces import ICartArticle
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from five import grok
from plone.dexterity.utils import createContentInContainer
from plone.uuid.interfaces import IUUID
from zope.lifecycleevent import modified


class CartArticleAdapter(grok.Adapter):
    """Adapter to handle CartArticle."""

    grok.context(ICartArticle)
    grok.provides(ICartArticleAdapter)

    @property
    def orig_article(self):
        """Returns riginar Article object."""
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'UID': self.context.orig_uuid}
        brains = catalog(query)
        if brains:
            return brains[0].getObject()