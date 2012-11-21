from Products.CMFCore.utils import getToolByName
from collective.cart.core.browser.interfaces import ICollectiveCartCoreLayer
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok


grok.templatedir('templates')


class BaseView(grok.View):
    """Base class for View"""
    grok.baseclass()
    grok.context(IShoppingSiteRoot)
    grok.layer(ICollectiveCartCoreLayer)
    grok.require('zope2.View')


class CartView(BaseView):
    """Cart View"""
    grok.name('cart')
    grok.template('cart')

    def update(self):
        self.request.set('disable_border', True)
        super(CartView, self).update()

    @property
    def cart_articles(self):
        """List of CartArticles within cart."""
        return IShoppingSite(self.context).cart_articles


class OrdersView(BaseView):
    grok.name('orders')
    grok.require('collective.cart.core.ViewCartContent')
    grok.template('orders')

    def update(self):
        self.request.set('disable_plone.leftcolumn', True)
        self.request.set('disable_plone.rightcolumn', True)

    @property
    def cart_container(self):
        if ICartContainer.providedBy(self.context):
            return self.context
        return IShoppingSite(self.context).cart_container

    def carts(self):
        if self.cart_container:
            result = []
            workflow = getToolByName(self.context, 'portal_workflow')
            adapter = ICartContainerAdapter(self.cart_container)
            for item in adapter.get_content_listing(ICart):
                res = {
                    'id': item.getId(),
                    'title': item.Title(),
                    'url': item.getURL(),
                    'state_title': workflow.getTitleForStateOnType(item.review_state(), item.portal_type),
                    'modified': adapter.localized_time(item),
                    'owner': item.Creator(),
                }
                result.append(res)
            return result


class CartContainerView(OrdersView):
    """View for CartContainer."""
    grok.context(ICartContainer)
    grok.name('view')


class CartContentView(BaseView):
    """View for CartContent"""
    grok.context(ICart)
    grok.name('view')
    grok.require('collective.cart.core.ViewCartContent')
    grok.template('cart-content')
