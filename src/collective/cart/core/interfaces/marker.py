from zope.interface import Interface


class ICartAware(Interface):
    """Marker interface to solve TypeError"""


class IPotentiallyAddableToCart(Interface):
    """Marker interface to solve TypeError"""
