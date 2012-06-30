from plone.directives import form
from zope.interface import Attribute
from zope.interface import Interface


class IArticle(form.Schema):
    """Schema for Article content type."""


class ICartContainer(form.Schema):
    """Schema for CartContainer content type."""


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
