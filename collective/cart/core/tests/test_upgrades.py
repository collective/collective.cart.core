from Products.CMFCore.utils import getToolByName
from collective.cart.core.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for upgrade steps."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_reimport_workflows(self):
        workflow = getToolByName(self.portal, 'portal_workflow')
        workflow.setChainForPortalTypes(('collective.cart.core.Cart', ), '')
        self.assertEqual(workflow.getChainForPortalType('collective.cart.core.Cart'), ())

        from collective.cart.core.upgrades import reimport_workflows
        reimport_workflows(self.portal)

        self.assertEqual(workflow.getChainForPortalType('collective.cart.core.Cart'), ('cart_default_workflow',))
