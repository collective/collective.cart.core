# -*- coding: utf-8 -*-
from collective.cart.core.browser.interfaces import IBaseViewlet

import unittest


class BaseViewletTestCase(unittest.TestCase):
    """TestCase for BaseViewlet"""

    def test_subclass(self):
        from zope.viewlet.interfaces import IViewlet
        self.assertTrue(IBaseViewlet, IViewlet)
