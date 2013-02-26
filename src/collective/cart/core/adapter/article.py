from Products.CMFCore.utils import getToolByName
from collective.behavior.salable.interfaces import ISalable
from collective.cart.core.adapter.base import BaseAdapter
from collective.cart.core.interfaces import IArticle
from collective.cart.core.interfaces import IArticleAdapter
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.session_cart import SessionCart
from five import grok
from plone.uuid.interfaces import IUUID


class ArticleAdapter(BaseAdapter):
    """Adapter to handle Article."""

    grok.context(IArticle)
    grok.provides(IArticleAdapter)

    @property
    def addable_to_cart(self):
        """True if the Article is addable to cart."""
        return IShoppingSite(self.context).shop and ISalable(self.context).salable

    def _update_existing_cart_article(self, items, **kwargs):
        """Update cart article which already exists in current cart.
        """

    def add_to_cart(self, **kwargs):
        """Add Article to Cart."""
        articles = IShoppingSite(self.context).cart_articles
        if not articles:
            session = self.getSessionData(create=True)
            articles = SessionCart()
        else:
            session = self.getSessionData(create=False)

        uuid = IUUID(self.context)

        if uuid in articles:
            items = articles[uuid]
            self._update_existing_cart_article(items, **kwargs)

        else:
            items = {
                # 'id': self.context.getId(),
                'id': uuid,
                'title': self.context.Title(),
                'description': self.context.Description(),
                'url': self.context.absolute_url(),
                # 'uuid': uuid,
            }
            items.update(kwargs)

        articles[uuid] = items
        session.set('collective.cart.core', {'articles': articles})
