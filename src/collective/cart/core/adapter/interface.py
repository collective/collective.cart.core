from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
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
        # return self._member_cart
        session_data_manager = getToolByName(self.context, 'session_data_manager')
        session = session_data_manager.getSessionData(create=False)
        if session:
            return session.get('collective.cart.core')

    # @property
    # def _member_cart(self):
    #     """Returns member Cart object."""
    #     container = self.cart_container
    #     if container:
    #         portal_state = getMultiAdapter(
    #             (self.context, self.context.REQUEST), name=u"plone_portal_state")
    #         member = portal_state.member()
    #         path = '/'.join(container.getPhysicalPath())
    #         brains = self.get_brains(ICart, path=path, depth=1, Creator=member.id, review_state='created')
    #         if brains:
    #             return brains[0].getObject()

    @property
    def cart_articles(self):
        """List of ordered dictionary of cart articles."""
        if self.cart:
            return self.cart.get('articles')

    @property
    def cart_article_listing(self):
        """List of cart articles for views."""
        res = []
        articles = self.cart_articles
        for key in articles:
            res.append(articles[key])
        return res

    def get_cart(self, cart_id):
        """Get cart by its id."""
        if self.cart_container:
            return self.cart_container.get(cart_id)

    def get_cart_article(self, uuid):
        if self.cart_articles:
            return self.cart_articles.get(uuid)

    def update_next_cart_id(self):
        """Update next cart ID for the cart container."""
        ICartContainerAdapter(self.cart_container).update_next_cart_id()

    def remove_cart_articles(self, uuids):
        """Remove articles of uuids from current cart.

        :param uuids: List of uuids or  in string.
        :type uuids: list or str
        """
        if self.cart_articles:
            if isinstance(uuids, str):
                uuids = [uuids]
            articles = self.cart_articles
            for uuid in uuids:
                del articles[uuid]
            session_data_manager = getToolByName(self.context, 'session_data_manager')
            session = session_data_manager.getSessionData(create=False)
            cart = session.get('collective.cart.core')
            cart['articles'] = articles
            session.set('collective.cart.core', cart)
