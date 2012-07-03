from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import IArticle
from collective.cart.core.interfaces import IArticleAdapter
from collective.cart.core.interfaces import ICartArticle
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from five import grok
from plone.dexterity.utils import createContentInContainer
from plone.uuid.interfaces import IUUID
from zope.lifecycleevent import modified


class ArticleAdapter(grok.Adapter):
    """Adapter to handle Article."""

    grok.context(IArticle)
    grok.provides(IArticleAdapter)

    def _create_cart_article(self, cart, oid):
        """Create CartArticle

        :param cart: Cart object.
        :type cart: collective.cart.core.Cart

        :param oid: CartArticle ID.
        :type oid: str

        :rtype: collective.cart.core.CartArticle
        """
        carticle = createContentInContainer(
            cart, 'collective.cart.core.CartArticle', id=oid,
            checkConstraints=False, orig_uuid=IUUID(self.context))
        modified(carticle)
        return carticle

    def _add_first_time_to_cart(self):
        """Add first time to cart creates cart."""
        container = IShoppingSite(self.context).cart_container
        if container:
            oid = str(container.next_cart_id)
            cart = createContentInContainer(
                container, 'collective.cart.core.Cart', id=oid, checkConstraints=False)
            modified(cart)
            ICartContainerAdapter(container).update_next_cart_id()
            self._create_cart_article(cart, '1')

    def _add_to_existing_cart(self, cart):
        """Add to existing cart."""
        query = {
            'path': {
                'query': '/'.join(cart.getPhysicalPath()),
                'depth': 1,
            },
            'object_provides': ICartArticle.__identifier__,
            'orig_uuid': IUUID(self.context),
        }
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(query)
        if brains:
            pass
        else:
            oid = str(int(max(set(cart.objectIds()))) + 1)
            self._create_cart_article(cart, oid)

    def add_to_cart(self):
        """Add Article to Cart."""
        cart = IShoppingSite(self.context).member_cart
        if cart:
            self._add_to_existing_cart(cart)
        else:
            self._add_first_time_to_cart()
