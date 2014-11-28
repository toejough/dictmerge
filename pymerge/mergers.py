'''Merge functions for default types defined by pymerge.types'''


# [ Imports ]
# [ -Project- ]
import pymerge.merge_types as merge_types


# [ Type Mergers ]
def tuple_merge(a, b):
    '''Merge the arguments as tuples'''
    return merge_types.tuplify(a) + merge_types.tuplify(b)


def list_merge(a, b):
    '''Merge the arguments as lists'''
    return a + b


def set_merge(a, b):
    '''Merge the arguments as sets'''
    return a | b


def dict_merge(a, b, conflict_handler):
    '''
    dictionary merge

    Uses conflict_handler to deal with overlapping keys.
    conflict_handler is called like:
        result[key] = conflict_handler(a[key], b[key])
    '''
    d = {}
    for key, value in a.items():
        d[key] = value
    for key, value in b.items():
        if key not in d:
            d[key] = value
        else:
            d[key] = conflict_handler(d[key], value)
    return d


