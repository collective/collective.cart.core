from Acquisition import aq_chain
from Acquisition import aq_inner
from collective.cart.core.adapter.base import BaseAdapter
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartAdapter
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok
from zope.component import getMultiAdapter
from zope.interface import Interface


class ShoppingSite(BaseAdapter):
    """Adapter to provide Shopping Site Root."""

    grok.context(Interface)
    grok.provides(IShoppingSite)

    @property
    def shop(self):
        """Returns Shop Site Root object."""
        context = aq_inner(self.context)
        chain = aq_chain(context)
        chain.sort()
        shops = [obj for obj in chain if IShoppingSiteRoot.providedBy(obj)]
        if shops:
            return shops[0]

    @property
    def cart_container(self):
        """Returns Cart Container object of Shop Site Root."""
        if self.shop:
            path = '/'.join(self.shop.getPhysicalPath())
            brains = self.get_brains(ICartContainer, path=path, depth=1)
            if brains:
                return brains[0].getObject()

    @property
    def cart(self):
        """Returns current Cart object."""
        return self._member_cart

    @property
    def _member_cart(self):
        """Returns member Cart object."""
        container = self.cart_container
        if container:
            portal_state = getMultiAdapter(
                (self.context, self.context.REQUEST), name=u"plone_portal_state")
            member = portal_state.member()
            path = '/'.join(container.getPhysicalPath())
            brains = self.get_brains(ICart, path=path, depth=1, Creator=member.id, review_state='created')
            if brains:
                return brains[0].getObject()

    @property
    def cart_articles(self):
        if self.cart:
            return ICartAdapter(self.cart).articles

    def get_cart(self, cart_id):
        """Get cart by its id."""
        if self.cart_container:
            return self.cart_container.get(cart_id)

    def get_cart_article(self, cid):
        if self.cart_articles:
            return ICartAdapter(self.cart).get_article(cid)

    def update_next_cart_id(self):
        """Update next cart ID for the cart container."""
        ICartContainerAdapter(self.cart_container).update_next_cart_id()

    def remove_cart_articles(self, ids):
        """Remove articles of ids from current cart.

        :param ids: List of ids or id in string.
        :type ids: list or str
        """
        if self.cart:
            if isinstance(ids, str):
                ids = [ids]
            for oid in ids:
                del self.cart[oid]
