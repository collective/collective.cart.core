from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class ICollectiveCartCoreLayer(Interface):
    """Marker interface for browserlayer."""


class ICartViewletManager(IViewletManager):
    """Viewlet manager interface for cart"""


class IOrderViewletManager(IViewletManager):
    """Viewlet manager interface for order"""
