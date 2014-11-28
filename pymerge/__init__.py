'''pymerge - merge all the things'''


# [ Imports ]
# [ -Python- ]
from functools import partial
from collections import OrderedDict
from itertools import combinations
# [ -Project- ]
import pymerge.types as types
import pymerge.mergers as mergers


# [ Classes ]
class BaseMerge(object):
    '''Base class for custom merge functions'''
    # [ Private Functions ]
    def __init__(self):
        '''Create the internal data necessary to function'''
        self._types = OrderedDict()
        self._mergers = {}
        self.set_rule('default', 'default', mergers.tuple_merge)

    def type(self, thing):
        '''Identifies the type of the thing passed in'''
        thing_type = 'default'
        for name, test in self._types.items():
            if test(thing):
                thing_type = name
                break
        print "{} - {}".format(thing, thing_type)
        return thing_type

    def __call__(self, a, b):
        '''Call this instance as a function - merge a and b'''
        a_type = self.type(a)
        b_type = self.type(b)
        try:
            merge_func = self._mergers[(a_type, b_type)]
        except KeyError:
            merge_func = self._mergers[('default', 'default')]
        return merge_func(a, b)

    def __reinsert_type(self, key):
        '''Remove and reinsert the key/item pair at the end of the types list'''
        # Remove the key/predicate
        predicate = self._types[key]
        del self._types[key]
        # Add it back in at the end
        self._types[key] = predicate

    # [ Public API ]
    def set_rule(self, type_a, type_b, merge_function, commutative=True):
        '''Set a new merge rule based on the types'''
        # Type checking
        if not isinstance(type_a, basestring):
            raise TypeError("type_a must be a string (was {})".format(type(type_a)))
        if not isinstance(type_b, basestring):
            raise TypeError("type_b must be a string (was {})".format(type(type_b)))
        if not hasattr(merge_function, '__call__'):
            raise TypeError("merge_function must be a callable")
        # Now set the rule
        self._mergers[(type_a, type_b)] = merge_function
        if commutative:
            self._mergers[(type_b, type_a)] = merge_function

    def delete_rule(self, type_a, type_b, commutative=True):
        '''delete the rule'''
        key = (type_a, type_b)
        if key in self._mergers:
            del self._mergers[key]
        if commutative:
            key = (type_b, type_a)
            if key in self._mergers:
                del self._mergers[key]

    def define_type(self, label, predicate):
        '''A thing will be considered to be of type <label> if <predicate>(thing)'''
        # first, get the current ordering
        current_order = self.list_types()
        # next, add the predicate
        if hasattr(predicate, '__call__'):
            self._types[label] = lambda x: bool(predicate(x))
        else:
            raise TypeError("Predicate ({}) must be callable to be used as a type-checker".format(predicate))
        # Now reorder - the most recent predicate takes precedence
        self.reorder_types([label] + current_order)

    def list_types(self):
        '''List the defined types'''
        return self._types.keys()

    def reorder_types(self, new_order):
        '''
        Reorder the types by the new_order.

        Keys not in the list go to the end, in the same order they're in.
        Keys in the list, but not in the dictionary, are skipped.
        '''
        # make sure the new order is a list
        new_order = list(new_order)
        print new_order
        # First, the keys in the list
        for key in new_order:
            if key in self._types:
                self.__reinsert_type(key)
            else:
                # ignore keys which are not in the dict
                pass
        # Now move the keys that are not in the list to the end
        for key in self.list_types():
            if key not in new_order:
                self.__reinsert_type(key)

    def remove_type(self, label):
        '''Remove a type definition'''
        del self._types[label]


# [ Other Helpers ]
def define_default_types(merge):
    '''Define the default types'''
    # default - if nothing else, it's default type
    merge.define_type('list', types.is_list)
    merge.define_type('tuple', types.is_tuple)
    merge.define_type('set', types.is_set)
    merge.define_type('dict', types.is_dict)


def set_default_rules(merge):
    '''Set the default rules'''
    # Matching Sets
    merge.set_rule('dict', 'dict', partial(mergers.dict_merge, conflict_handler=merge))
    merge.set_rule('tuple', 'tuple', mergers.tuple_merge)
    merge.set_rule('list', 'list', mergers.list_merge)
    merge.set_rule('set', 'set', mergers.set_merge)
    # Not matching sets
    for a, b in combinations(['default', 'dict', 'tuple', 'list', 'set'], 2):
        merge.set_rule(a, b, mergers.tuple_merge)


# [ Main merge ]
class Merge(BaseMerge):
    '''A Merge class with defaults'''
    def __init__(self):
        super(Merge, self).__init__()
        define_default_types(self)
        set_default_rules(self)
