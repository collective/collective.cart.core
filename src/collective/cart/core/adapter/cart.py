from collective.base.adapter import BaseAdapter
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartArticle
from collective.cart.core.interfaces import ICartAdapter
from five import grok


class CartAdapter(BaseAdapter):
    """Adapter for Cart"""

    grok.context(ICart)
    grok.provides(ICartAdapter)

    @property
    def articles(self):
        """List of CartArticle brains."""
        return self.get_brains(ICartArticle)

    def get_article(self, oid):
        """Get CartArticle brain form cart by ID."""
        return self.get_object(ICartArticle, id=oid)
