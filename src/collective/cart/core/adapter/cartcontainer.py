from Products.CMFCore.utils import getToolByName
from Products.validation import validation
from collective.cart.core.adapter.base import BaseAdapter
from collective.cart.core.interfaces import ICart
from collective.cart.core.interfaces import ICartAdapter
from collective.cart.core.interfaces import ICartContainer
from collective.cart.core.interfaces import ICartContainerAdapter
from datetime import datetime
from five import grok


class CartContainerAdapter(BaseAdapter):
    """Adapter to provide methods for CartContainer."""

    grok.context(ICartContainer)
    grok.provides(ICartContainerAdapter)

    def update_next_cart_id(self):
        """Update next_cart_id"""
        cid = self.context.next_cart_id
        while str(cid) in self.context.objectIds():
            cid += 1
        self.context.next_cart_id = cid

    def clear_created(self, minutes=None):
        """Clear cart state with created if it is older than minutes"""
        workflow = getToolByName(self.context, 'portal_workflow')
        validate = validation.validatorFor('isInt')
        for item in self.get_content_listing(ICart, review_state='created'):
            if minutes is None or validate(str(minutes)) != 1:
                obj = item.getObject()
                workflow.doActionFor(obj, 'canceled')
            else:
                obj = item.getObject()
                modifieds = []
                for item in ICartAdapter(obj).get_content_listing():
                    modifieds.append(item.modified)
                if modifieds and (datetime.utcnow() - min(modifieds).utcdatetime()).total_seconds() / 60 >= minutes:
                    workflow.doActionFor(obj, 'canceled')
                elif (datetime.utcnow() - item.modified.utcdatetime()).total_seconds() / 60 >= minutes:
                    workflow.doActionFor(obj, 'canceled')
                else:
                    pass

        ids = [item.id for item in self.get_content_listing(ICart, review_state='canceled')]
        self.context.manage_delObjects(ids)
