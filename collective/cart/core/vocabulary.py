from collective.cart.core import _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


numbering_methods = SimpleVocabulary([
    SimpleTerm(value=u'incremental', title=_(u'Incremental')),
    SimpleTerm(value=u'random', title=_(u'Random'))])

quantity_methods = SimpleVocabulary([
    SimpleTerm(value=u'select', title=u'Select'),
    SimpleTerm(value=u'input', title=u'Input')])
