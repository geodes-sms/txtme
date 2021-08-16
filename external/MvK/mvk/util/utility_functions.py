'''
Created on 3-mrt.-2014

@author: Simon
'''
from mvk.impl.python.datavalue import BooleanValue, SequenceValue
import mvk.interfaces.datavalue
from mvk.util.logger import get_logger


logger = get_logger('utility_functions')


def lists_eq_items(l1, l2, name_based=BooleanValue(True)):
    assert isinstance(l1, mvk.interfaces.datavalue.SequenceValue), logger.debug('l1 is not a SequenceValue')
    assert isinstance(l2, mvk.interfaces.datavalue.SequenceValue), logger.debug('l2 is not a SequenceValue')
    assert isinstance(name_based, mvk.interfaces.datavalue.BooleanValue), logger.debug('name_based is not a BooleanValue')
    return BooleanValue(internal_lists_eq_items(l1.get_value(), l2.get_value(), name_based.get_value()))

def internal_lists_eq_items(l1, l2, name_based=True):
    if len(l1) != len(l2):
        assert logger.debug('l1.len (%s) != l2.len (%s)' % (len(l1), len(l2)))
        return False
    l1_map = {}
    l2_map = {}
    if name_based:
        for next_it1, next_it2 in zip(l1, l2):
            if not (isinstance(next_it1, mvk.interfaces.element.NamedElement) and
                    isinstance(next_it2, mvk.interfaces.element.NamedElement)):
                name_based = False
                break
            else:
                l1_map.setdefault(next_it1.get_name(), []).append(next_it1)
                l2_map.setdefault(next_it2.get_name(), []).append(next_it2)

    if name_based:
        for k, v in l1_map.iteritems():
            if not k in l2_map:
                assert logger.debug('key %s not in l2_map' % k)
                return False
            if not internal_lists_eq_items(v, l2_map[k], name_based=False):
                assert logger.debug('lists with key %s not equal' % k)
                return False
    else:
        for next_it in l1:
            if not next_it in l2:
                assert logger.debug('item %s not in l2' % next_it.get_name() if isinstance(next_it, mvk.interfaces.element.NamedElement) else next_it)
                return False
    return True
