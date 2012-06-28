from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok
from zope.interface import Interface


class ShoppingSiteRoot(grok.Adapter):
    """Adapter to provice Shopping Site Root."""

    grok.context(Interface)
    grok.provides(IShoppingSiteRoot)

    @property
    def shop(self):
        context = aq_inner(self.context)
        chain = aq_chain(context)
        chain.sort()
        shops = [obj for obj in chain if IShoppingSite.providedBy(obj)]
        if shops:
            return shops[0]

    @property
    def cart_container(self):
        if self.shop:
            query = {
                'object_provides': ICartContainer.__identifier__,
                'path': {
                    'query': '/'.join(self.shop.getPhysicalPath()),
                    'depth': 1,
                },
            }
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog(query)
            if brains:
                return brains[0].getObject()
