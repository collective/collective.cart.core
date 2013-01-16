from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.statusmessages.interfaces import IStatusMessage
from collective.behavior.stock.interfaces import IStock
from collective.cart.core import _
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartAdapter
from collective.cart.core.interfaces import ICartArticleAdapter
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import IMakeShoppingSiteEvent
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok
from plone.dexterity.utils import createContentInContainer
from zope.interface import noLongerProvides
from zope.lifecycleevent import modified
from zope.lifecycleevent.interfaces import IObjectRemovedEvent


@grok.subscribe(ICartContainer, IObjectRemovedEvent)
def unmake_shopping_site(container, event):
    if container == event.object:
        parent = aq_parent(aq_inner(container))
        noLongerProvides(parent, IShoppingSiteRoot)
        parent.reindexObject(idxs=['object_provides'])
        message = _(u"This container is no longer a shopping site.")
        IStatusMessage(container.REQUEST).addStatusMessage(message, type='warn')


@grok.subscribe(IMakeShoppingSiteEvent)
def add_cart_container(event):
    context = event.context
    if not IShoppingSite(context).cart_container:
        container = createContentInContainer(
            context, 'collective.cart.core.CartContainer',
            id="cart-container", title="Cart Container", checkConstraints=False)
        modified(container)


@grok.subscribe(ICart, IActionSucceededEvent)
def return_stock_to_original(context, event):
    if event.action == 'canceled':
        for carticle in ICartAdapter(context).articles:
            obj = carticle['obj']
            article = ICartArticleAdapter(obj).orig_article
            if article:
                IStock(article).add_stock(obj.quantity)
                modified(article)
