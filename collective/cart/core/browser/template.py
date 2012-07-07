from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from collective.cart.shopping.browser.interfaces import ICollectiveCartCoreLayer
from five import grok


grok.templatedir('templates')


class CartView(grok.View):

    grok.context(IShoppingSiteRoot)
    grok.layer(ICollectiveCartCoreLayer)
    grok.name('cart')
    grok.require('zope2.View')
    grok.template('cart')

    @property
    def cart_articles(self):
        """List of CartArticles within cart."""
        return IShoppingSite(self.context).cart_articles
