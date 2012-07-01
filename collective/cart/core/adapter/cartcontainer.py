from collective.cart.core.error import InfiniteLoopError
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IRandomDigits
from five import grok
from zope.component import getUtility


class CartContainerAdapter(grok.Adapter):
    """Adapter to provide methods for CartContainer."""

    grok.context(ICartContainer)
    grok.provides(ICartContainerAdapter)

    def update_next_cart_id(self):
        """Update next_cart_id"""
        cid = self.context.next_cart_id
        while str(cid) in self.context.objectIds():
            cid += 1
        self.context.next_cart_id = cid
