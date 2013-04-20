from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cart.core.interfaces import IOrder
from collective.cart.core.interfaces import IOrderContainer
from collective.cart.core.interfaces import IOrderContainerAdapter
from collective.cart.core.interfaces import IShoppingSite
from zope.lifecycleevent import modified


class BaseCheckOutView(BrowserView):
    """Base view for check out"""

    def __call__(self):
        self.request.set('disable_border', True)

        IShoppingSite(self.context).clean_articles_in_cart()

        cart_url = '{}/@@cart'.format(self.context.absolute_url())
        current_base_url = self.context.restrictedTraverse("plone_context_state").current_base_url()
        if cart_url != current_base_url:
            return self.request.response.redirect(cart_url)

    def cart_articles(self):
        return IShoppingSite(self.context).cart_articles()


class CartView(BaseCheckOutView):
    """view for cart"""

    template = ViewPageTemplateFile('templates/cart.pt')

    def __call__(self):
        super(CartView, self).__call__()
        return self.template()


class OrdersView(BrowserView):
    """View for orders"""

    template = ViewPageTemplateFile('templates/orders.pt')

    def order_container(self):
        if IOrderContainer.providedBy(self.context):
            return self.context
        return IShoppingSite(self.context).order_container()

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

    def orders(self):
        container = self.order_container()
        result = []
        if container:
            workflow = getToolByName(self.context, 'portal_workflow')
            adapter = IOrderContainerAdapter(container)
            toLocalizedTime = self.context.restrictedTraverse('@@plone').toLocalizedTime
            for item in adapter.get_content_listing(IOrder, depth=1, sort_on="modified", sort_order="descending"):
                res = {
                    'id': item.getId(),
                    'title': item.Title(),
                    'url': item.getURL(),
                    'state_title': workflow.getTitleForStateOnType(item.review_state(), item.portal_type),
                    'modified': toLocalizedTime(item.ModificationDate()),
                    'owner': item.Creator(),
                    'transitions': self.transitions(item),
                    'is_canceled': item.review_state() == 'canceled',
                }
                result.append(res)
        return result

    def __call__(self):
        self.request.set('disable_plone.leftcolumn', True)
        self.request.set('disable_plone.rightcolumn', True)

        form = self.request.form
        value = form.get('form.buttons.ChangeState')
        order_id = form.get('order_id')

        if value is not None and order_id is not None:
            order = IShoppingSite(self.context).get_order(order_id)
            if order:
                workflow = getToolByName(self.context, 'portal_workflow')
                workflow.doActionFor(order, value)
                modified(order)

        elif form.get('form.buttons.RemoveCart') is not None and order_id is not None:
            self.order_container().manage_delObjects([order_id])

        return self.template()


class OrderView(BrowserView):
    """View for order"""

    __call__ = ViewPageTemplateFile('templates/order.pt')
