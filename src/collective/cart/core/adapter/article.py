from Products.CMFCore.utils import getToolByName
from collective.behavior.salable.interfaces import ISalable
from collective.cart.core.interfaces import IArticle
from collective.cart.core.interfaces import IArticleAdapter
from collective.cart.core.interfaces import ICartArticle
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.session_cart import SessionCart
from five import grok
from plone.dexterity.utils import createContentInContainer
from plone.uuid.interfaces import IUUID
from zope.lifecycleevent import modified


class ArticleAdapter(grok.Adapter):
    """Adapter to handle Article."""

    grok.context(IArticle)
    grok.provides(IArticleAdapter)

    # def _create_cart_article(self, cart, oid, **kwargs):
    #     """Create CartArticle

    #     :param cart: Cart object.
    #     :type cart: collective.cart.core.Cart

    #     :param oid: CartArticle ID.
    #     :type oid: str

    #     :rtype: collective.cart.core.CartArticle
    #     """
    #     carticle = createContentInContainer(
    #         cart, 'collective.cart.core.CartArticle', id=oid,
    #         checkConstraints=False, orig_uuid=IUUID(self.context),
    #         title=self.context.title, description=self.context.description)
    #     for key in kwargs:
    #         setattr(carticle, key, kwargs[key])
    #     modified(carticle)
    #     return carticle

    # def _add_first_time_to_cart(self, **kwargs):
    #     """Add first time to cart creates cart."""
    #     container = IShoppingSite(self.context).cart_container
    #     if container:
    #         oid = str(container.next_cart_id)
    #         cart = createContentInContainer(
    #             container, 'collective.cart.core.Cart', id=oid, checkConstraints=False)
    #         modified(cart)
    #         ICartContainerAdapter(container).update_next_cart_id()
    #         self._create_cart_article(cart, '1', **kwargs)

    # def _add_to_existing_cart(self, cart, **kwargs):
    #     """Add to existing cart."""
    #     query = {
    #         'path': {
    #             'query': '/'.join(cart.getPhysicalPath()),
    #             'depth': 1,
    #         },
    #         'object_provides': ICartArticle.__identifier__,
    #         'orig_uuid': IUUID(self.context),
    #     }
    #     catalog = getToolByName(self.context, 'portal_catalog')
    #     brains = catalog(query)
    #     if brains:
    #         obj = brains[0].getObject()
    #         self._update_existing_cart_article(obj, **kwargs)
    #     else:
    #         query = {
    #             'path': {
    #                 'query': '/'.join(cart.getPhysicalPath()),
    #                 'depth': 1,
    #             },
    #             'object_provides': ICartArticle.__identifier__,
    #         }
    #         brains = catalog(query)
    #         if brains:
    #             oid = str(int(max(set([brain.id for brain in brains]))) + 1)
    #         else:
    #             oid = '1'
    #         self._create_cart_article(cart, oid, **kwargs)

    def _update_existing_cart_article(self, items, **kwargs):
        """Update cart article which already exists in current cart.
        """

    @property
    def addable_to_cart(self):
        """True if the Article is addable to cart."""
        return IShoppingSite(self.context).shop and ISalable(self.context).salable

    @property
    def cart_articles(self, review_state=None):
        """Returns Cart Article brains which is originally from this Article.

        :param review_state: review_state for catalog query.
        :type review_state: str or list

        :rtype: list
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {
            'path': '/'.join(IShoppingSite(self.context).cart_container.getPhysicalPath()),
            'object_provides': ICartArticle.__identifier__,
            'orig_uuid': IUUID(self.context),
        }
        if review_state is not None:
            query['review_state'] = review_state
        return catalog(query)

    def add_to_cart(self, **kwargs):
        """Add Article to Cart."""
        articles = IShoppingSite(self.context).cart_articles
        session_data_manager = getToolByName(self.context, 'session_data_manager')
        if not articles:
            session = session_data_manager.getSessionData(create=True)
            articles = SessionCart()
        else:
            session = session_data_manager.getSessionData(create=False)

        uuid = IUUID(self.context)

        if uuid in articles:
            items = articles[uuid]
            self._update_existing_cart_article(items, **kwargs)

        else:
            items = {
                'id': self.context.getId(),
                'title': self.context.Title(),
                'description': self.context.Description(),
                'url': self.context.absolute_url(),
                'uuid': uuid,
            }
            items.update(kwargs)

        articles[uuid] = items
        session.set('collective.cart.core', {'articles': articles})
