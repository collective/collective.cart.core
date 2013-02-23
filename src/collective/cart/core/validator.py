from collective.cart.core import _
from collective.cart.core.interfaces import IBaseAdapter
from collective.cart.core.interfaces import ICartContainer
from five import grok
from z3c.form.validator import SimpleFieldValidator
from z3c.form.validator import WidgetValidatorDiscriminators
from zope.interface import Invalid


class ValidateCartIDUniqueness(SimpleFieldValidator):
    """Validate uniqueness of  next cart ID within the cart container."""

    def validate(self, value):
        super(ValidateCartIDUniqueness, self).validate(value)

        if value is not None:
            brains = IBaseAdapter(self.context).get_brains(depth=1, id=str(value))
            if brains:
                raise Invalid(_(u'The cart ID is already in use.'))


WidgetValidatorDiscriminators(ValidateCartIDUniqueness, field=ICartContainer['next_cart_id'])

grok.global_adapter(ValidateCartIDUniqueness)
