from collective.cart.core import _
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

    next_cart_id = Int(
        title=_(u'Next Cart ID'),
        default=1,
        min=1)

    quantity_method = Choice(
        title=_(u'Quantity Method'),
        description=_(u'Select one method, Select or Input to determine how to put products into cart.'),
        vocabulary=quantity_methods,
        default=u'select')

    def update_next_cart_id():  # pragma: no cover
        """Update next_cart_id"""


class ICart(form.Schema):
    """Schema for Cart content type."""


class ICartArticle(form.Schema):
    """Schema for CartArticle content type."""

    orig_uuid = Attribute('Original UUID for the article.')


class IShoppingSiteRoot(Interface):
    """Marker interface for Shopping Site Root."""


class IShoppingSite(Interface):
    """Adapter Interface for Shopping Site."""

    shop = Attribute("Returns Shop Site Root object.")  # pragma: no cover
    cart_container = Attribute("Returns Cart Container object of Shop Site Root.")  # pragma: no cover

    def update_next_cart_id():  # pragma: no cover
        """Update next cart ID for the cart container."""

    def member_cart():  # pragma: no cover
        """Returns member cart."""


class ICartContainerAdapter(Interface):
    """Adapter Interface for CartContainer."""

    def update_next_cart_id():  # pragma: no cover
        """Update next_cart_id based on numbering_method."""


class IArticleAdapter(Interface):
    """Adapter Interface for Article."""

    def add_to_cart():
        """Add Article to Cart."""
