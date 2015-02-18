'''dictmerge - merge dictionaries'''


# [ Imports ]
# [ -Python- ]
# [ -Project- ]


# [ Exceptions ]
class KeyConflictError(KeyError):
    '''for use when two dictionaries have the same key, but not the same value'''
    pass


# [ Helpers ]
def default_resolver(key, value_1, value_2):
    '''
    Return a merged dictionary as the value if both values are dictionaries,
    return one of the two values as the value if they are equivalent,
    otherwise raise KeyConflictError
    '''
    # if the values are both dictionaries, recursively merge
    if isinstance(value_1, dict) and isinstance(value_2, dict):
        return {key: merge(value_1, value_2, default_resolver)}
    # if the values are equivalent, return one.
    elif value_1 == value_2:
        return {key: value_1}
    raise KeyConflictError("Conflicting non-dictionary value(s) ({} != {}) found for {} in dictionaries to be merged.".format(
        value_1, value_2, key
    ))


# [ Core ]
def merge(d1, d2, resolve=default_resolver):
    '''Merge two dictionaries'''
    # basic type checking
    if not isinstance(d1, dict):
        raise TypeError("d1 must be a dictionary (not a {})".format(type(d1)))
    if not isinstance(d2, dict):
        raise TypeError("d2 must be a dictionary (not a {})".format(type(d2)))
    if not hasattr(resolve, '__call__') and resolve is not None:
        raise TypeError("resolve must be callable");
    # build a new dictionary
    d_new = {}
    # fill it with the items from the first dictionary
    for key, value in d1.items():
        d_new[key] = value
    # try to add items from the second dictionary
    for key, value in d2.items():
        # if a key is already present, need to resolve the conflict
        if key in d_new:
            # remove the key
            del d_new[key]
            # resolve the conflict and merge the result
            if resolve is None:
                raise KeyConflictError(
                    "Both dictionaries have the same key {} and no resolver is defined.".format(
                    key))
            d_result = resolve(key, d1[key], d2[key])
            d_new = merge(d_new, d_result, resolve)
        # otherwise, just add the key/value pair
        else:
            d_new[key] = value
    return d_new
