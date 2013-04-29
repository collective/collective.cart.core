from plone.app.layout.globals.interfaces import IViewView
from zope.interface import Attribute
from zope.interface import Interface
from zope.viewlet.interfaces import IViewlet
from zope.viewlet.interfaces import IViewletManager


# Browser layer

class ICollectiveCartCoreLayer(Interface):
    """Interface for browserlayer."""


# Viewlet manager

class IBaseFormViewletManager(IViewletManager):
    """Viewlet manager interface for base form"""


class IOrderViewletManager(IViewletManager):
    """Viewlet manager interface for order"""


# View

class IBaseFormView(IViewView):
    """View interface for base form"""

    title = Attribute('Title of context')
    description = Attribute('Description of context')


class ICheckOutView(IBaseFormView):
    """View interface for check out"""


class ICartView(ICheckOutView):
    """View interface for cart"""


class IOrderListingView(IBaseFormView):
    """View interface for order listing"""

    def order_container():
        """Returns order container"""


class IOrderView(IViewView):
    """View interface for order"""


# Viewlet


class IBaseViewlet(IViewlet):
    """Base viewlet interface to override method: render"""

    def render():
        """"""


class IAddToCartViewlet(IBaseViewlet):
    """Viewlet interface for AddToCartViewlet"""

    def available():
        """Returns True if availabel else False"""


class ICartArticleListingViewlet(IBaseViewlet):
    """Viewlet interface for CartArticleListingViewlet"""

    def articles():
        """Returns list of articles in cart"""


class IOrderListingViewlet(IBaseViewlet):
    """Viewlet interface for OrderListingViewlet"""

    def container():
        """Returns order container object

        :rtype: collective.cart.core.Ordercontainer
        """

    def orders():
        """Returns list of oders

        :rtype: list
        """


class IOrderArticleListingViewlet(IBaseViewlet):
    """Viewlet interface for OrderArticleListingViewlet"""
