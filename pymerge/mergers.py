'''Merge functions for default types defined by pymerge.types'''


# [ Imports ]
# [ -Project- ]
import pymerge.merge_types as merge_types


# [ Exceptions ]
class KeyConflictError(KeyError):
    '''for use when two dictionaries have the same key, but not the same value'''
    pass


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
            d[key] = conflict_handler(d[key], value, key)
    return d


def pedantic_dict_conflict_handler(a, b, key):
    '''Throw an error if the values are not the same'''
    # raise in conflict
    if a != b:
        raise KeyConflictError("Conflicting values ({} != {}) found for {} in dictionaries to be merged.".format(
            a, b, key
        ))
    # return one if they are equal
    return a
