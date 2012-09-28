from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartArticle
from collective.cart.core.interfaces import ICartAdapter
from five import grok


class CartAdapter(grok.Adapter):
    """Adapter for Cart"""

    grok.context(ICart)
    grok.provides(ICartAdapter)

    @property
    def articles(self):
        """List of CartArticles"""
        context = aq_inner(self.context)
        query = {
            'path': '/'.join(context.getPhysicalPath()),
            'object_provides': ICartArticle.__identifier__,
        }
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(query)
