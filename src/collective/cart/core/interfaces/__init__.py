from collective.cart.core import _
from plone.directives import form
from zope.interface import Attribute
from zope.interface import Interface
from zope import schema


class IArticle(form.Schema):
    """Schema for Article content type."""


class ICartContainer(form.Schema):
    """Schema for CartContainer content type."""

    next_cart_id = schema.Int(
        title=_(u'Next Cart ID'),
        default=1,
        min=1)

    def update_next_cart_id():  # pragma: no cover
        """Update next_cart_id"""

    def clear_created(minutes):  # pragma: no cover
        """Clear cart state with created if it is older than minutes"""


class ICart(form.Schema):
    """Schema for Cart content type."""

    description = schema.Text(
        title=_(u'Description'),
        required=False)


class IBaseAdapter(Interface):
    """Base interface for adapters"""

    def get_brains(self, interface, **query):
        """Get brains which provides interface under the context."""

    def get_content_listing(self, interface, **query):
        """Get ContentListing from brains gotten from get_brains method."""

    def localized_time(item, long_format=False):
        """Returns localized time."""


class ICartAdapter(IBaseAdapter):
    """Adapter interface for Cart."""

    articles = Attribute('List of brains of CartArticle.')

    def get_article(oid):
        """Get CartArticle form cart by ID."""


class ICartArticle(form.Schema):
    """Schema for CartArticle content type."""

    orig_uuid = Attribute('Original UUID')


class IShoppingSiteRoot(form.Schema):
    """Marker interface for Shopping Site Root."""


class IShoppingSite(IBaseAdapter):
    """Adapter Interface for Shopping Site."""

    shop = Attribute("Shop Site Root object.")
    cart_container = Attribute("Cart Container object of Shop Site Root.")
    cart = Attribute('Current Cart object.')
    cart_articles = Attribute('List of cart articles within current cart.')

    def get_cart(cart_id):  # pragma: no cover
        """Get cart by its id."""

    def get_cart_article(cid):  # pragma: no cover
        """Get cart article by cid."""

    def update_next_cart_id():  # pragma: no cover
        """Update next cart ID for the cart container."""

    def remove_cart_articles(ids):  # pragma: no cover
        """Remove articles of ids from current cart."""


class ICartContainerAdapter(IBaseAdapter):
    """Adapter Interface for CartContainer."""

    def update_next_cart_id():  # pragma: no cover
        """Update next_cart_id based on numbering_method."""


class IArticleAdapter(Interface):
    """Adapter Interface for Article."""

    addable_to_cart = Attribute('True if the Article is addable to cart.')
    cart_articles = Attribute('Cart Article brains which is originally from this Article.')

    def add_to_cart():  # pragma: no cover
        """Add Article to Cart."""


class ICartArticleAdapter(IBaseAdapter):
    """Adapter Interface for CartArticle."""

    orig_article = Attribute('Originar Article object.')


class IMakeShoppingSiteEvent(Interface):
    """An event making shopping site."""


class IUnmakeShoppingSiteEvent(Interface):
    """An event unmaking shopping site."""


class IPrice(Interface):
    """Utility interface for price."""
