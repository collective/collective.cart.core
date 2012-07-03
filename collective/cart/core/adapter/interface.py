from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok
from zope.component import getMultiAdapter
from zope.interface import Interface


class ShoppingSite(grok.Adapter):
    """Adapter to provide Shopping Site Root."""

    grok.context(Interface)
    grok.provides(IShoppingSite)

    @property
    def shop(self):
        context = aq_inner(self.context)
        chain = aq_chain(context)
        chain.sort()
        shops = [obj for obj in chain if IShoppingSiteRoot.providedBy(obj)]
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

    def update_next_cart_id(self):
        """Update next cart ID for the cart container."""
        ICartContainerAdapter(self.cart_container).update_next_cart_id()

    @property
    def member_cart(self):
        """Returns member cart."""
        container = self.cart_container
        if container:
            portal_state = getMultiAdapter(
                (self.context, self.context.REQUEST), name=u"plone_portal_state")
            member = portal_state.member()
            query = {
                'path': {
                    'query': '/'.join(container.getPhysicalPath()),
                    'depth': 1,
                },
                'object_provides': ICart.__identifier__,
                'Creator': member.id,
                'review_state': 'created',
            }
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog(query)
            if brains:
                return brains[0].getObject()
