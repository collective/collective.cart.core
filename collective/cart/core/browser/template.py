from collective.cart.core.browser.base import BaseListingObject
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from collective.cart.core.browser.interfaces import ICollectiveCartCoreLayer
from five import grok


grok.templatedir('templates')


class CartView(grok.View):

    grok.context(IShoppingSiteRoot)
    grok.layer(ICollectiveCartCoreLayer)
    grok.name('cart')
    grok.require('zope2.View')
    grok.template('cart')

    def update(self):
        self.request.set('disable_border', True)
        super(CartView, self).update()

    @property
    def cart_articles(self):
        """List of CartArticles within cart."""
        return IShoppingSite(self.context).cart_articles


class BaseListingView(grok.View):
    grok.baseclass()
    grok.layer(ICollectiveCartCoreLayer)
    grok.name('view')
    grok.require('collective.cart.core.ViewCartContent')


class CartContainerView(BaseListingView, BaseListingObject):

    grok.context(ICartContainer)
    grok.template('cart-container')

    def update(self):
        self.request.set('disable_plone.leftcolumn', True)
        self.request.set('disable_plone.rightcolumn', True)

    @property
    def carts(self):
        result = []
        for item in self._listing(ICart):
            res = {
                'id': item.getId(),
                'title': item.Title(),
                'url': item.getURL(),
                'review_state': item.review_state(),
                'modified': self._localized_time(item),
                'owner': item.Creator(),
            }
            result.append(res)
        return result


class CartContentView(BaseListingView):

    grok.context(ICart)
    grok.template('cart-content')
