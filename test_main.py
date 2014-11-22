'''Tests for pymerge'''


# [ Imports ]
# [ -Python- ]
# [ -Third-party- ]
# [ -Project- ]
from pymerge import Merge


# [ Globals ]
merge = Merge()


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
def test_set_overlap():
    # expect sets to combine into a single set
    assert merge({1, 2, 3}, {3, 4, 5}) == {1, 2, 3, 4, 5}
    # expect this to be the same as OR-ing sets
    assert merge({1, 2, 3}, {3, 4, 5}) == {1, 2, 3} | {4, 5}


def test_dictionary_overlap():
    # expect dictionaries to combine into a single dictionary
    first = {'foo': 'FOO', 'bar':'BAR'}
    second = {'foo': 'foo', 'baz':'BAZ'}
    assert merge(first, second) == {
        'foo': ('FOO', 'foo'),
        'bar': 'BAR',
        'baz': 'BAZ'
    }
    # expect this NOT to be the same as merging items
    assert merge(first, second) != dict(first.items() + second.items())


# [ -Mixed Types- ]
def test_scalar_tuple():
    # expect to combine into a single tuple
    assert merge(1, ('a', 'b')) == (1, 'a', 'b')
    assert merge((1, 2), 'a') == (1, 2, 'a')


def test_scalar_list():
    # expect to combine into a single list
    assert merge(['a', 'b', 'c'], 4) == ('a', 'b', 'c', 4)
    assert merge('a', ['b', 'c', 4]) == ('a', 'b', 'c', 4)


def test_scalar_set():
    # expect to combine into a single set
    assert merge({1, 2, 3}, 4) == (1, 2, 3, 4)
    assert merge(1, {2, 3, 4}) == (1, 2, 3, 4)


def test_scalar_dictionary():
    # expect to combine into a tuple
    first = {'foo': 'FOO', 'bar':'BAR'}
    second = 'baz'
    assert merge(first, second) == ({
        'foo': 'FOO',
        'bar': 'BAR',
    }, 'baz')
    assert merge(second, first) == ('baz', {
        'foo': 'FOO',
        'bar': 'BAR',
    })


def test_tuple_list():
    # expect to combine into a single list
    assert merge(('a', 'b', 'c'), [4]) == ('a', 'b', 'c', 4)
    assert merge(['a', 'b', 'c'], (4,)) == ('a', 'b', 'c', 4)


def test_tuple_set():
    # expect to combine into a single set
    assert merge({1, 2, 3}, (4, 5)) == (1, 2, 3, 4, 5)
    assert merge((1, 2, 3), {4, 5}) == (1, 2, 3, 4, 5)


def test_tuple_dictionary():
    # expect to combine into a tuple
    first = {'foo': 'FOO', 'bar':'BAR'}
    second = ('baz', 'quux')
    assert merge(first, second) == ({
        'foo': 'FOO',
        'bar': 'BAR',
    }, 'baz', 'quux')
    assert merge(second, first) == ('baz', 'quux', {
        'foo': 'FOO',
        'bar': 'BAR',
    })


def test_list_set():
    # expect to combine into a single set
    assert merge({1, 2, 3}, [4, 5]) == (1, 2, 3, 4, 5)
    assert merge([1, 2, 3], {4, 5}) == (1, 2, 3, 4, 5)


def test_list_dictionary():
    # expect to combine into a list
    first = {'foo': 'FOO', 'bar':'BAR'}
    second = ['baz', 'quux']
    assert merge(first, second) == ({
        'foo': 'FOO',
        'bar': 'BAR',
    }, 'baz', 'quux')
    assert merge(second, first) == ('baz', 'quux', {
        'foo': 'FOO',
        'bar': 'BAR',
    })


def test_set_dictionary():
    # expect to combine into a set
    first = {'foo': 'FOO', 'bar':'BAR'}
    second = {'baz', 'quux'}
    assert merge(first, second) == ({
        'foo': 'FOO',
        'bar': 'BAR',
    }, 'baz', 'quux') or merge(first, second) == ({
        'foo': 'FOO',
        'bar': 'BAR',
    }, 'quux', 'baz')
    assert merge(second, first) == ('baz', 'quux', {
        'foo': 'FOO',
        'bar': 'BAR',
    }) or merge(second, first) == ('quux', 'baz', {
        'foo': 'FOO',
        'bar': 'BAR',
    })


# [ -Recursive Merge- ]
def test_nested_dictionary():
    a = {
        'foo': { 1, 2, 3},
        'bar': 'BAR',
        'baz': 'BAZ',
    }
    b = {
        'foo': { 2, 3, 4},
        'bar': ['B', 'A', 'R'],
        'quux': 'quux'
    }
    assert merge(a, b) == {
        'foo': {1, 2, 3, 4},
        'bar': ('BAR', 'B', 'A', 'R'),
        'baz': 'BAZ',
        'quux': 'quux',
    }


# [ -Type Overrides- ]
def test_set_override():
    merge.set_rule('set', 'set', lambda a, b: a & b)
    assert merge({1, 2, 3, 4}, {3, 4, 5, 6}) == {3, 4}


def test_custom_override():
    # test adding support for generators
    import types
    merge.define_type('generator', lambda x: isinstance(x, types.GeneratorType))
    def merge_generators(a, b):
        for item in a:
            yield item
        for item in b:
            yield item
    merge.set_rule('generator', 'generator', merge_generators)
    assert list(merge([1, 2, 3], ['a', 'b'])) == [1, 2, 3, 'a', 'b']