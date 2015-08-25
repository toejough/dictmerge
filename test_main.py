'''Tests for dictmerge'''


# [ Imports ]
# [ -Python- ]
# [ -Third-party- ]
import pytest
# [ -Project- ]
from dictmerge import merge, KeyConflictError


# [ Globals ]
BASE = {
    'foo': 'FOO',
    'bar': 'BAR'
}
NON_OVERLAPPING = {
    'baz': 'BAZ',
    'quux': 'QUUX'
}
BASE_NON_OVERLAPPING = {
    'foo': 'FOO',
    'bar': 'BAR',
    'baz': 'BAZ',
    'quux': 'QUUX'
}
OVERLAPPING_SAME = {
    'bar': 'BAR',
    'baz': 'BAZ',
    'quux': 'QUUX'
}
OVERLAPPING_DIFFERENT = {
    'bar': 'candy bar',
    'baz': 'BAZ',
    'quux': 'QUUX'
}
CONCAT_OVERLAPPING = {
    'foo': 'FOO',
    'bar': 'BARBAR',
    'baz': 'BAZ',
    'quux': 'QUUX'
}
DEL_OVERLAPPING = {
    'foo': 'FOO',
    'baz': 'BAZ',
    'quux': 'QUUX'
}


# [ Tests ]
def test_non_overlapping():
    # expect a straightforward merge
    assert merge(BASE, NON_OVERLAPPING) == BASE_NON_OVERLAPPING

def test_overlapping_same():
    # expect the overlap to resolve to a single copy of the overlapping key/value
    assert merge(BASE, OVERLAPPING_SAME) == BASE_NON_OVERLAPPING

def test_overlapping_different():
    # expect an exception
    with pytest.raises(KeyConflictError):
        merge(BASE, OVERLAPPING_DIFFERENT)

def test_overlapping_with_concat_resolver():
    # expect resolver to be called with the overlapping pairs
    non_local = { 'resolver called': False }
    def resolver(key, a_value, b_value):
        non_local['resolver called'] = True
        assert key == 'bar'
        assert a_value == 'BAR'
        assert b_value == 'BAR'
        return {key: b_value + a_value}
    assert merge(BASE, OVERLAPPING_SAME, resolver) == CONCAT_OVERLAPPING
    assert non_local['resolver called']

def test_overlapping_with_del_resolver():
    # expect resolver to be called with the overlapping pairs
    non_local = { 'resolver called': False }
    def resolver(key, a_value, b_value):
        non_local['resolver called'] = True
        assert key == 'bar'
        assert a_value == 'BAR'
        assert b_value == 'BAR'
        return {}
    assert merge(BASE, OVERLAPPING_SAME, resolver) == DEL_OVERLAPPING
    assert non_local['resolver called']

def test_overlapping_with_cascading_resolver():
    # expect resolver to be called with the overlapping pairs
    non_local = { 'resolver called': False }
    def resolver(key, a_value, b_value):
        non_local['resolver called'] = True
        return {'foo': a_value + b_value}
    cascade_overlapping = merge(BASE, OVERLAPPING_SAME, resolver)
    assert non_local['resolver called']
    assert 'FOO' in cascade_overlapping['foo']
    assert 'BARBAR' in cascade_overlapping['foo']

def test_recursive():
    # expect dictionaries to be combined recursively
    first = {
        'a': {'all': 'azure'},
        'b': {'boss': 'balance', 2: 22}
    }
    second = {
        'a': {1: 1},
        'b': {2:22},
        'c': {'carp': 'careen', 3:333, 'III': 'aye aye aye'}
    }
    combined = {
        'a': {'all': 'azure', 1: 1},
        'b': {'boss': 'balance', 2: 22},
        'c': {'carp': 'careen', 3:333, 'III': 'aye aye aye'}
    }
    assert merge(first, second) == combined

def test_wrong_types():
    '''expect actionable error messages'''
    with pytest.raises(TypeError):
        merge(1, dict())
    with pytest.raises(TypeError):
        merge(dict(), 2)
    with pytest.raises(TypeError):
        merge(dict(), dict(), 1)

def test_no_resolver():
    '''expect a KeyConflictError'''
    with pytest.raises(KeyConflictError):
        merge(BASE, OVERLAPPING_SAME, None)
