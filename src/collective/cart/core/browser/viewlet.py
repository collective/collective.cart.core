from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cart.core.interfaces import IArticleAdapter
from collective.cart.core.interfaces import IShoppingSite
from plone.app.layout.viewlets.common import ViewletBase
from zExceptions import Forbidden


class AddToCartViewlet(ViewletBase):
    """Viewlet to display add to cart form for article"""

    index = ViewPageTemplateFile('viewlets/add-to-cart.pt')

    def update(self):
        form = self.request.form
        if form.get('form.buttons.AddToCart', None) is not None:

            authenticator = self.context.restrictedTraverse('@@authenticator')
            if not authenticator.verify():
                raise Forbidden()

            IArticleAdapter(self.context).add_to_cart()
            context_state = self.context.restrictedTraverse('@@plone_context_state')
            return self.request.response.redirect(context_state.current_base_url())

    def available(self):
        return IArticleAdapter(self.context).addable_to_cart()


class CartArticlesViewlet(ViewletBase):
    """Viewlet to display articles in cart"""

    index = ViewPageTemplateFile('viewlets/cart-articles.pt')

    def articles(self):
        return IShoppingSite(self.context).cart_article_listing()

    def update(self):
        form = self.request.form
        uuid = form.get('form.buttons.RemoveArticle', None)

        if uuid is not None:

            authenticator = self.context.restrictedTraverse('@@authenticator')
            if not authenticator.verify():
                raise Forbidden()

            shopping_site = IShoppingSite(self.context)
            shopping_site.remove_cart_articles(uuid)
            if not shopping_site.cart_articles():
                current_base_url = self.context.restrictedTraverse("plone_context_state").current_base_url()
                return self.request.response.redirect(current_base_url)


class OrderArticlesViewlet(ViewletBase):
    """Viewlet to display articles in order"""
    index = ViewPageTemplateFile('viewlets/order-articles.pt')
