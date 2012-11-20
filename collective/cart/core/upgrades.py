from Products.CMFCore.utils import getToolByName

import logging


PROFILE_ID = 'profile-collective.cart.core:default'


def reimport_workflows(context, logger=None):
    """Reimport workflows"""
    if logger is None:
        logger = logging.getLogger(__name__)
    setup = getToolByName(context, 'portal_setup')
    logger.info('Reimporting workflows.')
    setup.runImportStepFromProfile(
        PROFILE_ID, 'workflow', run_dependencies=False, purge_old=False)
