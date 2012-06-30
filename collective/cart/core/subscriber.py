from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.statusmessages.interfaces import IStatusMessage
from collective.cart.core import _
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import IShoppingSiteRoot
from five import grok
from zope.interface import noLongerProvides
from zope.lifecycleevent.interfaces import IObjectRemovedEvent


@grok.subscribe(ICartContainer, IObjectRemovedEvent)
def unmake_shopping_site(container, event):
    assert container == event.object
    parent = aq_parent(aq_inner(container))
    noLongerProvides(parent, IShoppingSiteRoot)
    parent.reindexObject(idxs=['object_provides'])
    message = _(u"This container is no longer a shopping site.")
    IStatusMessage(container.REQUEST).addStatusMessage(message, type='info')
