from Acquisition import aq_inner
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser import BrowserView
from collective.cart.core.interfaces import IShoppingSite
from collective.cart.core.interfaces import IShoppingSiteRoot
from plone.dexterity.utils import createContentInContainer
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.lifecycleevent import modified


class Miscellaneous(BrowserView):

    def make_shopping_site(self):
        """Make context shopping site if it is folder."""
        context = aq_inner(self.context)
        alsoProvides(context, IShoppingSiteRoot)
        context.reindexObject(idxs=['object_provides'])

        if not IShoppingSite(context).cart_container:
            container = createContentInContainer(
                context, 'collective.cart.core.CartContainer', id="cart-container", title="Cart Container", checkConstraints=False)
            modified(container)

        url = context.absolute_url()
        return self.request.response.redirect(url)

    def unmake_shopping_site(self):
        """Unmake context shopping site."""
        noLongerProvides(self.context, IShoppingSiteRoot)
        self.context.reindexObject(idxs=['object_provides'])
        url = self.context.absolute_url()
        return self.request.response.redirect(url)

    def is_shopping_site(self):
        return IFolderish.providedBy(
            self.context) and IShoppingSiteRoot.providedBy(self.context)

    def not_shopping_site(self):
        return IFolderish.providedBy(
            self.context) and not IShoppingSiteRoot.providedBy(self.context)

    # def potentially_addable_but_not_addable_to_cart(self):
    #     context = aq_inner(self.context)
    #     return IPotentiallyAddableToCart.providedBy(context) and not IAddableToCart.providedBy(context)

    # def addable_to_cart(self):
    #     context = aq_inner(self.context)
    #     return IPotentiallyAddableToCart.providedBy(context) and IAddableToCart.providedBy(context)

    # def make_addable_to_cart(self):
    #     context = aq_inner(self.context)
    #     if IPotentiallyAddableToCart.providedBy(context):
    #         alsoProvides(context, IAddableToCart)
    #         url = '%s/@@edit-product' % context.absolute_url()
    #         IAnnotations(context)['collective.cart.core'] = ProductAnnotations()
    #         return self.request.response.redirect(url)

    # def make_not_addable_to_cart(self):
    #     context = aq_inner(self.context)
    #     noLongerProvides(context, IAddableToCart)
    #     url = context.absolute_url()
    #     del IAnnotations(context)['collective.cart.core']
    #     return self.request.response.redirect(url)

    # def products(self):
    #     context = aq_inner(self.context)
    #     cart = IPortal(context).cart
    #     if cart is not None:
    #         products = ICart(cart).products
    #         if products:
    #             properties = getToolByName(context, 'portal_properties')
    #             pcp = IPortalCartProperties(properties)
    #             res = []
    #             for product in products:
    #                 cproduct = ICartProduct(product)
    #                 item = dict(
    #                     uid=product.uid,
    #                     title=product.title,
    #                     quantity=product.quantity,
    #                     url=cproduct.product.url,
    #                     price_with_currency=pcp.price_with_currency(cproduct.price),
    #                     html_quantity=cproduct.html_quantity,
    #                     subtotal_with_currency=pcp.price_with_currency(cproduct.subtotal),
    #                 )
    #                 res.append(item)
    #             return res

    # def cart_id(self):
    #     context = aq_inner(self.context)
    #     cart = IPortal(context).cart
    #     if cart:
    #         return cart.id

    # def set_info(self, items):
    #     context = aq_inner(self.context)
    #     IPortal(context).cart.info = items

    # def total_cost(self):
    #     context = aq_inner(self.context)
    #     cart = IPortal(context).cart
    #     if cart:
    #         return str(ICart(cart).total_cost)

    # def next_step(self):
    #     context = aq_inner(self.context)
    #     cfolder = IPortal(context).cart_folder
    #     form = cfolder.getNext_form()
    #     if form is not None:
    #         self.request.response.redirect(form.absolute_url())
    #     else:
    #         context.restrictedTraverse('test-step')

    # def test_step(self):
    #     """Method to provide test step."""

    # def make_cart_aware(self):
    #     context = aq_inner(self.context)
    #     alsoProvides(context, ICartAware)
    #     parent = aq_parent(context)
    #     alsoProvides(parent, ICartAware)
    #     url = context.absolute_url()
    #     return self.request.response.redirect(url)

    # def make_not_cart_aware(self):
    #     context = aq_inner(self.context)
    #     noLongerProvides(context, ICartAware)
    #     parent = aq_parent(context)
    #     noLongerProvides(parent, ICartAware)
    #     url = context.absolute_url()
    #     return self.request.response.redirect(url)

    # def is_cart_aware(self):
    #     context = aq_inner(self.context)
    #     return ICartAware.providedBy(context)
