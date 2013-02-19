from collective.cart.core.browser.interfaces import ICollectiveCartCoreLayer
# from collective.cart.core.browser.base import BaseListingObject
from collective.cart.core.interfaces import IArticle
from collective.cart.core.interfaces import IArticleAdapter
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IBelowContentTitle
from plone.app.viewletmanager.manager import OrderedViewletManager


grok.templatedir('viewlets')


class AddToCartViewlet(grok.Viewlet):
    """Viewlet to show add to cart form for salable article."""
    grok.context(IArticle)
    grok.layer(ICollectiveCartCoreLayer)
    grok.name('collective.cart.core.add.to.cart')
    grok.require('zope2.View')
    grok.template('add-to-cart')
    grok.view(IViewView)
    grok.viewletmanager(IBelowContentTitle)

    def update(self):
        form = self.request.form
        if form.get('form.addtocart', None) is not None:
            IArticleAdapter(self.context).add_to_cart()
            return self.render()

    def available(self):
        return IArticleAdapter(self.context).addable_to_cart


class CartViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Viewlet manager for cart view."""
    grok.context(IShoppingSiteRoot)
    grok.layer(ICollectiveCartCoreLayer)
    grok.name('collective.cart.core.cartviewletmanager')


class CartArticlesViewlet(grok.Viewlet):
    """Cart Articles Viewlet Class."""
    grok.context(IShoppingSiteRoot)
    grok.layer(ICollectiveCartCoreLayer)
    grok.name('collective.cart.core.cartarticles')
    grok.require('zope2.View')
    grok.template('cart-articles')
    grok.viewletmanager(CartViewletManager)

    def update(self):
        form = self.request.form
        uuid = form.get('form.delete.article', None)
        if uuid is not None:
            IShoppingSite(self.context).remove_cart_articles(uuid)
            if self.view.cart_articles:
                return self.render()
            else:
                return self.request.response.redirect(self.view.url())

    @property
    def articles(self):
        """Returns list of articles to show in cart."""
        return IShoppingSite(self.context).cart_article_listing


class CartContentViewletManager(OrderedViewletManager, grok.ViewletManager):
    """Viewlet manager for cart view."""
    grok.context(ICart)
    grok.layer(ICollectiveCartCoreLayer)
    grok.name('collective.cart.core.cartcontentviewletmanager')


# class CartContentViewlet(grok.Viewlet, BaseListingObject):
class CartContentViewlet(grok.Viewlet):
    """Viewlet to show cart content in cart container."""
    grok.context(ICart)
    grok.layer(ICollectiveCartCoreLayer)
    grok.name('collective.cart.core.cart-content')
    grok.require('zope2.View')
    grok.template('cart-content')
    grok.viewletmanager(CartContentViewletManager)

    # @property
    # def articles(self):
    #     """List of CartArticles within cart."""
    #     result = []
    #     for item in self._listing(ICartArticle):
    #         res = {
    #             'id': item.getId(),
    #             'title': item.Title(),
    #             'url': None,
    #             'modification': self._localized_time(item),
    #         }
    #         obj = item.getObject()
    #         article = ICartArticleAdapter(obj).orig_article
    #         if article:
    #             res['url'] = article.absolute_url()
    #         result.append(res)
    #     return result
