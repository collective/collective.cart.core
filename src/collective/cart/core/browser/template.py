from Products.CMFCore.utils import getToolByName
from collective.cart.core.browser.interfaces import ICollectiveCartCoreLayer
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import ICartContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok
from zope.lifecycleevent import modified


grok.templatedir('templates')


class BaseView(grok.View):
    """Base class for View"""
    grok.baseclass()
    grok.context(IShoppingSiteRoot)
    grok.layer(ICollectiveCartCoreLayer)
    grok.require('zope2.View')


class BaseCheckOutView(BaseView):
    """Base class for check out view"""
    grok.baseclass()

    def update(self):
        self.request.set('disable_border', True)

        articles = self.cart_articles
        if articles:
            number_of_articles = len(articles)
            for key in articles:
                if not self.shopping_site.get_brain(UID=key):
                    del articles[key]

            if len(articles) != number_of_articles:
                session_data_manager = getToolByName(self.context, 'session_data_manager')
                session = session_data_manager.getSessionData(create=False)
                session.set('collective.cart.core', {'articles': articles})

    @property
    def shopping_site(self):
        return IShoppingSite(self.context)

    @property
    def cart_articles(self):
        """List of CartArticles within cart."""
        return self.shopping_site.cart_articles

    # @property
    # def has_cart_articles(self):
    #     if self.cart_articles:
    #         import pdb; pdb.set_trace()
    #         return len(self.cart_articles)


class CartView(BaseCheckOutView):
    """Cart View"""
    grok.name('cart')
    grok.template('cart')


class OrdersView(BaseView):
    grok.name('orders')
    grok.require('collective.cart.core.ViewCartContent')
    grok.template('orders')

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
            for item in adapter.get_content_listing(ICart, sort_on="modified", sort_order="descending"):
                res = {
                    'id': item.getId(),
                    'title': item.Title(),
                    'url': item.getURL(),
                    'state_title': workflow.getTitleForStateOnType(item.review_state(), item.portal_type),
                    'modified': adapter.localized_time(item),
                    'owner': item.Creator(),
                    'transitions': self.transitions(item),
                    'is_canceled': item.review_state() == 'canceled',
                }
                result.append(res)
            return result

    def transitions(self, item):
        workflow = getToolByName(self.context, 'portal_workflow')
        obj = item.getObject()
        res = []
        for trans in workflow.getTransitionsFor(obj):
            available = True
            if item.review_state() == 'created' and trans['id'] != 'canceled':
                available = False
            res.append({
                'id': trans['id'],
                'name': trans['name'],
                'available': available,
            })
        return res

    def update(self):
        self.request.set('disable_plone.leftcolumn', True)
        self.request.set('disable_plone.rightcolumn', True)

        form = self.request.form
        if form.get('form.buttons.ClearCreated', None) is not None:
            return ICartContainerAdapter(self.cart_container).clear_created()

        value = form.get('form.buttons.ChangeState')
        cart_id = form.get('cart-id')

        if value is not None and cart_id is not None:
            cart = IShoppingSite(self.context).get_cart(cart_id)
            if cart:
                workflow = getToolByName(self.context, 'portal_workflow')
                workflow.doActionFor(cart, value)
                modified(cart)

        elif form.get('form.buttons.RemoveCart') is not None and cart_id is not None:
            self.cart_container.manage_delObjects([cart_id])


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
