from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from collective.cart.core.adapter.base import BaseAdapter
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok


class ShoppingSite(BaseAdapter):
    """Adapter to provide shopping site."""

    grok.provides(IShoppingSite)

    @property
    def shop(self):
        """Returns Shop Site Root object."""
        context = aq_inner(self.context)
        chain = aq_chain(context)
        shops = [obj for obj in chain if IShoppingSiteRoot.providedBy(obj)]
        if shops:
            return shops[0]

    @property
    def cart_container(self):
        """Returns Cart Container object located directly under Shop Site Root."""
        if self.shop:
            path = '/'.join(self.shop.getPhysicalPath())
            return self.get_object(interface=ICartContainer, path=path, depth=1)

    @property
    def cart(self):
        """Returns current cart in session."""
        session_data_manager = getToolByName(self.context, 'session_data_manager')
        session = session_data_manager.getSessionData(create=False)
        if session:
            return session.get('collective.cart.core')

    @property
    def cart_articles(self):
        """List of ordered dictionary of cart articles in session."""
        if self.cart:
            return self.cart.get('articles')

    @property
    def cart_article_listing(self):
        """List of cart articles in session for views."""
        res = []
        articles = self.cart_articles
        if articles:
            for key in articles:
                res.append(articles[key])
        return res

    def get_cart_article(self, uuid):
        if self.cart_articles:
            return self.cart_articles.get(uuid)

    def remove_cart_articles(self, uuids):
        """Remove articles of uuids from current cart.

        :param uuids: List of uuids or  in string.
        :type uuids: list or str
        """
        articles = self.cart_articles
        if articles:
            if isinstance(uuids, str):
                uuids = [uuids]
            deleted = []
            for uuid in uuids:
                deleting = articles.pop(uuid, None)
                if deleting is not None:
                    deleted.append(deleting)
            if deleted:
                session_data_manager = getToolByName(self.context, 'session_data_manager')
                session = session_data_manager.getSessionData(create=False)
                cart = session.get('collective.cart.core')
                cart['articles'] = articles
                session.set('collective.cart.core', cart)

    # CartContainer related methods comes here::

    def get_cart(self, cart_id):
        """Get cart by its id."""
        if self.cart_container:
            return self.cart_container.get(cart_id)

    def update_next_cart_id(self):
        """Update next cart ID for the cart container."""
        if self.cart_container:
            ICartContainerAdapter(self.cart_container).update_next_cart_id()

    # def create_cart(self):
    #     """Create cart instance from cart in session"""
    #     container = self.cart_container
    #     if self.cart_container:
    #         oid = str(container.next_cart_id)
    #         cart = createContentInContainer(
    #             container, 'collective.cart.core.Cart', id=oid, checkConstraints=False)
    #         modified(cart)
    #         self.update_next_cart_id()
    #         # self._create_cart_article(cart, '1', **kwargs)
