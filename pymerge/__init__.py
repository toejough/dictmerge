'''pymerge - merge all the things'''


# [ Imports ]
# [ -Python- ]
from functools import partial


# [ Merge Functions ]
def merge_to_tuple(a, b):
    '''merge scalars into a tuple'''
    return (a, b)


def set_or(a, b):
    '''Set merge via the | operator'''
    return a | b


def merge_dictionaries(a, b, conflict_handler):
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


def concatenate(a, b):
    '''concatenate the arguments via the + operator'''
    return a + b


# [ Type Functions ]
def identify_type(thing):
    '''Identify the type of the thing'''
    # default the type to scalar
    thing_type = 'scalar'
    # try python type checking
    python_type = type(thing).__name__
    if python_type in ['set', 'tuple', 'list', 'dict']:
        thing_type = python_type
    # return the type
    return thing_type


def get_type_merge(thing_type):
    '''Get a type-specific merge function'''
    global MERGE_FUNCTIONS
    return MERGE_FUNCTIONS.get(thing_type, None)


def identify_merge_function(type1, type2):
    '''Identify and return the appropriate merge function for the types'''
    if type1 != type2:
        merge_function = merge_to_tuple
    else:
        merge_function = get_type_merge(type1)
    return merge_function


# [ Main merge ]
def merge(thing1, thing2):
    '''
    Merge the args, regardless of type, and do so intelligently.

    When presented with:
        different types, merge to a tuple.
        two of the same type, merge with type-specific merge function.
        recursive types, recurse.
    '''
    # Identify types
    type1 = identify_type(thing1)
    type2 = identify_type(thing2)
    # Identify best merge function based on the rules
    merge_function = identify_merge_function(type1, type2)
    # Run combiner function
    merged = merge_function(thing1, thing2)
    # Return result
    return merged


# [ Globals ]
# Merge function dictionary
# needs to be after the merge functions.  Ugly.
MERGE_FUNCTIONS = {
    'scalar': merge_to_tuple,
    'set': set_or,
    'tuple': concatenate,
    'list': concatenate,
    'dict': partial(merge_dictionaries, conflict_handler=merge),
}
