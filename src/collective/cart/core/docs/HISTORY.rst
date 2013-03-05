Change log
----------

0.5.3 (2013-02-05)
==================

- Updated cart to use session. [taito]
- Covered tests. [taito]
- Added dependency to collective.base. [taito]
- Added method: shop_path to ShoppingSite adapter. [taito]
- Added redirection from other check out url to cart url when cart is empty. [taito]

0.5.2.13 (2013-02-05)
=====================

- Automatically clean created, but not processed cart when visiting shop top. [taito]

0.5.2.12 (2013-01-31)
=====================

- Moved get_action method to function. [taito]

0.5.2.11 (2013-01-30)
=====================

- Moved subscriber: return_stock_to_original to collective.cart.shopping. [taito]

0.5.2.10 (2013-01-30)
=====================

- Made utility Price work. [taito]

0.5.2.9 (2013-01-16)
====================

- Updated workflows. [taito]
- Added event subscriber to return stock to the original article
  when state transit to cancel successfully. [taito]

0.5.2.8 (2012-12-20)
====================

- Updated dependencies. [taito]

0.5.2.7 (2012-12-12)
====================

- Updated translation. [taito]

0.5.2.6 (2012-11-23)
====================

- Removed unnecessary files. [taito]

0.5.2.5 (2012-11-23)
====================

- Added testing integration to Travis CI. [taito]

0.5.2.4 (2012-11-21)
====================

- Finnish translations updated. [taito]
- Added owner to cart container view. [taito]
- Updated workflows. [taito]

0.5.2 (2012-09-24)
==================

- Added permission for cart portlet. [taito]

0.5.1 (2012-09-20)
==================

- Added purge="False" to types_not_searched and metaTypesNotToList properties. [taito]

0.5 (2012-09-19)
================

- Use Dexterity. [taito]
- Tested with Plone-4.2.1. [taito]

0.4.1 (2011-10-03)
==================
- easy_install error fixed. [taito]

0.4 (2011-09-24)
================
- End of support for Plone-3.x.
- License updated from GPL to BSD.

0.3.2 (2011-05-14)
==================
- has_cart_folder method added.

0.3.1 (2011-04-25)
==================
- Some template fixes.

0.3.0 (2011-04-25)
==================
- Refactored for plugins.

0.2.0 (2011-04-23)
==================
- Input support for quantity method.
- Multiple cart folder support.

0.1.1 (2011-04-21)
==================
- Double registration of cart portlet fixed.

0.1.0 (2011-04-21)
==================
- Initial release
