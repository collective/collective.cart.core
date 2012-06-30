from collective.cart.core import _
from collective.cart.core.vocabulary import numbering_methods
from collective.cart.core.vocabulary import quantity_methods
from plone.directives import form
from zope.interface import Attribute
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import Int


class IArticle(form.Schema):
    """Schema for Article content type."""


class ICartContainer(form.Schema):
    """Schema for CartContainer content type."""

    numbering_method = Choice(
        title=_(u'Cart ID Numbering Method'),
        vocabulary=numbering_methods,
        default=u'incremental')

    next_cart_id = Int(
        title=_(u'Next Cart ID'),
        default=1,
        min=1)

    random_digits = Int(
        title=_(u'Random Digits Numer'),
        description=_(u'If Random Cart ID is selected, give integer digits here.'),
        default=5,
        required=False,
        min=1)

    quantity_method = Choice(
        title=_(u'Quantity Method'),
        description=_(u'Select one method, Select or Input to determine how to put products into cart.'),
        vocabulary=quantity_methods,
        default=u'select')


class ICart(form.Schema):
    """Schema for Cart content type."""


class ICartArticle(form.Schema):
    """Schema for CartArticle content type."""


class IShoppingSite(Interface):
    """Marker interface for shopping site."""


class IShoppingSiteRoot(Interface):
    """Interface for Shopping Site Root."""

    shop = Attribute("Returns Shop Site Root object.")  # pragma: no cover
    cart_container = Attribute("Returns Cart Container object of Shop Site Root.")  # pragma: no cover
