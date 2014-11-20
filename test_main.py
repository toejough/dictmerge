'''Tests for pymerge'''


# [ Imports ]
# [ -Python- ]
# [ -Third-party- ]
# [ -Project- ]
from pymerge import merge


# [ Tests ]
# [ -Basic- ]
def test_numbers():
    # expect numbers to combine into a tuple
    assert merge(1, 2) == (1, 2)


def test_strings():
    # expect strings to combine into a tuple
    assert merge('hello', 'there') == ('hello', 'there')


def test_tuple():
    # expect tuples to combine into a single tuple
    assert merge((1, 2), ('a', 'b')) == (1, 2, 'a', 'b')
    # expect this to be the same as adding tuples
    assert merge((1, 2), ('a', 'b')) == (1, 2) + ('a', 'b')


def test_list():
    # expect lists to combine into a single list
    assert merge(['a', 'b', 'c'], [4]) == ['a', 'b', 'c', 4]
    # expect this to be the same as adding lists
    assert merge(['a', 'b', 'c'], [4]) == ['a', 'b'] + ['c', 4]


def test_set():
    # expect sets to combine into a single set
    assert merge({1, 2, 3}, {4, 5}) == {1, 2, 3, 4, 5}
    # expect this to be the same as OR-ing sets
    assert merge({1, 2, 3}, {4, 5}) == {1, 2, 3} | {4, 5}


def test_dictionary():
    # expect dictionaries to combine into a single dictionary
    first = {'foo': 'FOO', 'bar':'BAR'}
    second = {'baz':'BAZ'}
    assert merge(first, second) == {
        'foo': 'FOO',
        'bar': 'BAR',
        'baz': 'BAZ'
    }
    # expect this to be the same as merging items
    assert merge(first, second) == dict(first.items() + second.items())


# [ -Content Overlap- ]
# def test_set_overlap():
# def test_dictionary_overlap():
# [ -Mixed Types- ]
# def test_scalar_tuple():
# def test_scalar_list():
# def test_scalar_set():
# def test_scalar_dictionary():
# def test_tuple_list():
# def test_tuple_set():
# def test_tuple_dictionary():
# def test_list_set():
# def test_list_dictionary():
# def test_set_dictionary():
# [ -Recursive Merge- ]
# def test_nested_tuple():
# def test_nested_list():
# def test_nested_set():
# def test_nested_dictionary():
# def test_nested_overlapping_mix():
# [ -Iterator Wrapping- ]
# def test_unknown_iterator():
# expectation is that a new iterator will be created, which calls the first till empty, then the second
# def test_set_iterator():
# def test_list_iterator():
# def test_dictionary_iterator():
# [ -Type Overrides- ]
# def test_dictionary_override():
# def test_set_override():
# def test_custom_override():
