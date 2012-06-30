from collective.cart.core.interfaces.adapter import ICart
from collective.cart.core.interfaces.adapter import ICartFolder
from collective.cart.core.interfaces.adapter import ICartProduct
from collective.cart.core.interfaces.adapter import ICartProduct
from collective.cart.core.interfaces.adapter import IPortal
from collective.cart.core.interfaces.adapter import IPortalCartProperties
from collective.cart.core.interfaces.adapter import IProduct
from collective.cart.core.interfaces.adapter import IProductAnnotationsAdapter
from collective.cart.core.interfaces.content_type import ICartContentType
from collective.cart.core.interfaces.content_type import ICartFolderContentType
from collective.cart.core.interfaces.content_type import ICartProductContentType
from collective.cart.core.interfaces.event import IUpdateCart
from collective.cart.core.interfaces.event import IUpdateCartTotal
from collective.cart.core.interfaces.marker import IAddableToCart
from collective.cart.core.interfaces.marker import ICartAware
from collective.cart.core.interfaces.marker import IPotentiallyAddableToCart
from collective.cart.core.interfaces.marker import IProductAnnotations
from collective.cart.core.interfaces.utility import IDecimalPlaces
from collective.cart.core.interfaces.utility import IPrice
from collective.cart.core.interfaces.utility import IPriceInString
from collective.cart.core.interfaces.utility import IPriceWithCurrency
from collective.cart.core.interfaces.utility import IRandomDigits
from collective.cart.core.interfaces.utility import IRegularExpression
from collective.cart.core.interfaces.utility import ISelectRange
from collective.cart.core.interfaces.viewlet_manager import ICartConfigViewletManager
from collective.cart.core.interfaces.viewlet_manager import ICartTotalsViewletManager
from collective.cart.core.interfaces.viewlet_manager import ICartViewletManager
from collective.cart.core.interfaces.viewlet_manager import IEditProductViewletManager
from collective.cart.core.interfaces.viewlet_manager import IFixedInfoViewletManager
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


class ICartContainer(Interface):
    """Marker interface for cart container."""


class IShoppingSiteRoot(Interface):
    """Interface for Shopping Site Root."""

    shop = Attribute("Returns Shop Site Root object.")  # pragma: no cover
    cart_container = Attribute("Returns Cart Container object of Shop Site Root.")  # pragma: no cover
