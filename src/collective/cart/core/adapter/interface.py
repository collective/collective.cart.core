from Acquisition import aq_chain
from Acquisition import aq_inner
from collective.base.adapter import BaseAdapter
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok
from plone.dexterity.utils import createContentInContainer
from zope.lifecycleevent import modified


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
    def shop_path(self):
        if self.shop:
            return '/'.join(self.shop.getPhysicalPath())

    @property
    def cart_container(self):
        """Returns Cart Container object located directly under Shop Site Root."""
        if self.shop:
            return self.get_object(ICartContainer, path=self.shop_path, depth=1)

    @property
    def cart(self):
        """Returns current cart in session."""
        session = self.getSessionData(create=False)
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
                session = self.getSessionData(create=False)
                if session:
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

    def create_cart(self, cart_id=None):
        """Create cart instance from cart in session into cart container."""
        if self.cart_container and self.cart_articles:
            if cart_id is None:
                cart_id = str(self.cart_container.next_cart_id)
            cart = createContentInContainer(
                self.cart_container, 'collective.cart.core.Cart', id=cart_id, checkConstraints=False)
            modified(cart)
            self.update_next_cart_id()
            for uuid in self.cart_articles:
                carticle = createContentInContainer(cart, 'collective.cart.core.CartArticle', checkConstraints=False, **self.cart_articles[uuid])
                modified(carticle)

            return cart
