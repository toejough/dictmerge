'''A library for pymerge'''


# [ Type Checkers ]
def is_tuple(thing):
    '''Check if the thing is a tuple'''
    return isinstance(thing, tuple)


def is_list(thing):
    '''Check if the thing is a list'''
    return isinstance(thing, list)


def is_set(thing):
    '''Check if the thing is a set'''
    return isinstance(thing, set)


def is_dict(thing):
    '''Check if the thing is a dict'''
    return isinstance(thing, dict)


# [ Coercion ]
def tuplify(thing):
    '''Make the thing a tuple if it isn't already'''
    t = thing
    if not is_tuple(t):
        if not hasattr(t, '__iter__') or is_dict(t):
            # not iterable, or is a dictionary
            t = (t,)
        else:
            # not a dictionary, is iterable
            t = tuple(t)
    return t


