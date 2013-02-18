from collections import OrderedDict
from collective.cart.core.interfaces import ISessionCart
from zope.interface import implements


class SessionCart(OrderedDict):
    implements(ISessionCart)
